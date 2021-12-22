def pytest_assume_fail(lineno, entry):
    """
    钩子在假设失败时操作用户定义的数据。
    :param lineno:  代码中假设失败的那一行
    :param entry: 由assume()调用生成的假设失败消息
    :return:
    """
    pass


def pytest_assume_pass(lineno, entry):
    """
    钩子，在假设成功的情况下操作用户定义的数据。
    lineno: 代码中假设成功的那一行
    entry: 由assume()调用生成的假设成功消息
    """
    pass


def pytest_assume_summary_report(failed_assumptions):
    """

    :param failed_assumptions:
    :return:
    """
    pass
