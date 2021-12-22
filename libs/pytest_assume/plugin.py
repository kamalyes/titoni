import inspect
import os.path
from functools import partial

try:
    # Pytest 6.x
    from _pytest.skipping import xfailed_key as evalxfail_key
    from _pytest.skipping import evaluate_xfail_marks as mark_eval
except ImportError:
    # Pytest 5.x
    from _pytest.mark.evaluate import MarkEvaluator

    mark_eval = partial(MarkEvaluator, name="xfail")
    try:
        from _pytest.skipping import evalxfail_key
    except ImportError:
        # And pytest 3-4.x
        evalxfail_key = ""

import pytest
from six import reraise as raise_

try:
    from py.io import saferepr
except ImportError:
    saferepr = repr

_FAILED_ASSUMPTIONS = []


class Assumption(object):
    __slots__ = ["entry", "tb", "locals"]

    def __init__(self, entry, tb, locals=None):
        self.entry = entry
        # TODO: trim the TB at init?
        self.tb = tb
        self.locals = locals

    def longrepr(self):
        output = [self.entry, "Locals:"]
        output.extend(self.locals)

        return "\n".join(output)

    def repr(self):
        return self.entry


class FailedAssumption(AssertionError):
    pass


class AssumeContextManager(object):
    """
    上下文管理器，其对象可用于“软断言”
    当用作上下文管理器时::
        with pytest.assume:
            assert expr, msg

    当直接使用时，它还提供一个返回值::
        ret = pytest.assume(expr, msg)

    :param expr: 表达式的assert
    :param msg: 断言失败时显示的消息。
    :return: True或False，根据' expr
    """

    def __init__(self):
        self._enter_from_call = False

    def __enter__(self):
        __tracebackhide__ = True
        self._last_status = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __tracebackhide__ = True
        pretty_locals = None
        entry = None
        tb = None
        stack_level = 2 if self._enter_from_call else 1
        (frame, filename, line, funcname, contextlist) = inspect.stack()[stack_level][0:5]
        # 获取文件名、行和上下文
        try:
            filename = os.path.relpath(filename)
        except ValueError:
            pass  # 文件名位于与当前目录不同的挂载上(Windows)

        context = "" if contextlist is None else contextlist[0].lstrip()

        if exc_type is None:
            # format entry
            entry = u"{filename}:{line}: AssumptionSuccess\n>>\t{context}".format(**locals())
            pytest._hook_assume_pass(lineno=line, entry=entry)

            self._last_status = True
            return True

        elif issubclass(exc_type, AssertionError):
            if exc_val:
                context += "{}:{}\n".format(exc_type.__name__, exc_val)
            entry = u"{filename}:{line}: AssumptionFailure\n>>\t{context}".format(**locals())
            pretty_locals = ["\t%-10s = %s" % (name, saferepr(val)) for name, val in frame.f_locals.items()]
            pytest._hook_assume_fail(lineno=line, entry=entry)
            _FAILED_ASSUMPTIONS.append(Assumption(entry, exc_tb, pretty_locals))
            self._last_status = False
            return True
        else:
            return

    def __call__(self, expr, msg=""):
        __tracebackhide__ = True
        self._enter_from_call = True
        with self:
            if msg:
                assert expr, msg
            else:
                assert expr
        self._enter_from_call = False
        return self._last_status


assume = AssumeContextManager()


def pytest_addhooks(pluginmanager):
    """
    这个例子假设钩子是在'hooks'模块中分组的
    :param pluginmanager:
    :return:
    """
    from . import hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config):
    """
    将跟踪列表添加到pytest命名空间，这样我们就可以始终访问它，以及“assume”函数本身
    :param config:
    :return:
    """
    pytest.assume = assume
    pytest._showlocals = config.getoption("showlocals")
    pytest._hook_assume_fail = config.pluginmanager.hook.pytest_assume_fail
    pytest._hook_assume_pass = config.pluginmanager.hook.pytest_assume_pass
    pytest._hook_assume_summary_report = config.pluginmanager.hook.pytest_assume_summary_report


@pytest.hookimpl(tryfirst=True)
def pytest_assume_fail(lineno, entry):
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_assume_pass(lineno, entry):
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_assume_summary_report(failed_assumptions):
    """
    获取错误代码行数
    :param failed_assumptions:
    :return:
    """
    if getattr(pytest, "_showlocals"):
        content = "".join(x.longrepr() for x in failed_assumptions)
    else:
        content = "".join(x.repr() for x in failed_assumptions)
    return content


def restore_xfail(item):
    """
    恢复xfail标记 为以后的xfail/xpass检查工作
    :param item:
    :return:
    """
    if hasattr(item, "_store"):
        item._store[evalxfail_key] = mark_eval(item)
    else:
        item._evalxfail = mark_eval(item)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """
    使用pyfunc_call尽可能“接近”测试的实际调用 立即执行
    注意:我不喜欢这里的异常处理
    :param item:
    :return:
    """
    __tracebackhide__ = True
    outcome = None
    try:
        outcome = yield
    finally:
        failed_assumptions = _FAILED_ASSUMPTIONS
        if failed_assumptions:
            failed_count = len(failed_assumptions)
            root_msg = "\n%s Failed Assumptions:" % failed_count

            content = pytest._hook_assume_summary_report(failed_assumptions=failed_assumptions)

            # 用户在实现自定义钩子pytest_assume_summary_report时，会返回"string" 默认钩子总是作为列表元素0出现
            if len(content) == 1:  # default length
                # Uses default hook
                content = content[0]
            else:
                # User created hook, if any
                content = content[1]

            last_tb = failed_assumptions[-1].tb

            del _FAILED_ASSUMPTIONS[:]
            if outcome and outcome.excinfo:
                # 这是通过pytest_pyfunc_call()钩子完成的,在hook之前。
                if "[XPASS(strict)]" in str(outcome.excinfo[1]):
                    restore_xfail(item)
                    raise_(FailedAssumption, FailedAssumption("%s\n%s" % (root_msg, content)), last_tb)
                root_msg = "\nOriginal Failure:\n\n>> %s\n" % repr(outcome.excinfo[1]) + root_msg
                raise_(
                    FailedAssumption,
                    FailedAssumption(root_msg + "\n" + content),
                    outcome.excinfo[2],
                )
            else:
                exc = FailedAssumption(root_msg + "\n" + content)
                # 注意: 在这里升起，我们保证失败
                raise_(FailedAssumption, exc, last_tb)
