!!! note "跳过测试函数的最简单方法是用 skip 可以传递可选 reason"

```
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...
```

!!! note "或者，也可以通过调用 pytest.skip(reason) 功能"

```
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

!!! note "也可以跳过整个模块，使用 pytest.skip(reason, allow_module_level=True) 在模块级别"

```
import sys
import pytest
if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)
参考文献 ： pytest.mark.skip
```

!!! warning "如果您希望有条件地跳过某些内容，则可以使用 skipif 相反。以下是在python3.6之前的解释器上运行时将测试函数标记为跳过的示例"

```
import sys
@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_function():
    ...
```

如果条件评估为 True 在收集期间，将跳过测试函数，使用时在摘要中显示指定的原因 -rs .

你可以分享 skipif 模块之间的标记。考虑这个测试模块：


```
import mymodule

minversion = pytest.mark.skipif(
    mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
)

@minversion
def test_function():
    ...

```

您可以导入标记并在另一个测试模块中重用它：

```
from test_mymodule import minversion
@minversion
def test_anotherfunction():
    ...
```

对于较大的测试套件，最好有一个文件定义标记，然后在整个测试套件中一致地应用这些标记。

或者，您可以使用 condition strings 而不是布尔值，但是它们不容易在模块之间共享，因此主要是出于向后兼容性的原因才支持它们。

参考文献 ： pytest.mark.skipif

跳过类或模块的所有测试函数 你可以使用 skipif 类上的标记（作为任何其他标记）如果条件是 True ，此标记将为该类的每个测试方法生成跳过结果

```
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

!!! warning "如果要跳过模块的所有测试功能，可以使用 pytestmark 修饰符应用于测试函数，如果任何跳过条件为真，则将跳过它"

```
pytestmark = pytest.mark.skipif(...)
```

有时可能需要跳过整个文件或目录，例如，如果测试依赖于特定于Python版本的功能或包含不希望运行pytest的代码。在这种情况下，必须从集合中排除文件和目录。参照 自定义测试集合 更多信息。

跳过缺少的导入依赖项 您可以使用 pytest.importorskip 在模块级，在测试或测试设置功能内。

```
docutils = pytest.importorskip("docutils")
```

如果 docutils 无法在此处导入，这将导致跳过测试结果。也可以根据库的版本号跳过：
```
docutils = pytest.importorskip("docutils", minversion="0.3")
```
版本将从指定的模块中读取 __version__ 属性。

无条件跳过模块中的所有测试：
```
pytestmark = pytest.mark.skip("all tests still WIP")
```

根据某些条件跳过模块中的所有测试：
```
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")
```

如果缺少某些导入，则跳过模块中的所有测试：
```
pexpect = pytest.importorskip("pexpect")
```

你可以使用 xfail 标记以指示预期测试失败：
```
@pytest.mark.xfail
def test_function():
    ...
```
此测试将运行，但失败时不会报告回溯。相反，终端报告会将其列在“预期失败”中 (XFAIL ）或“意外通过” (XPASS 部分。

或者，也可以将测试标记为 XFAIL 必须从测试或其设置功能中：
```
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")
def test_function2():
    import slow_module

    if slow_module.slow_function():
        pytest.xfail("slow_module taking too long")
```

这两个示例说明了您不希望在模块级别检查条件的情况，也就是说，在这种情况下，条件将被评估为标记。

这将使 test_function XFAIL . 注意，在 pytest.xfail() 呼叫，与标记不同。这是因为它是通过引发一个已知的异常在内部实现的。

如果测试只在特定条件下失败，则可以将该条件作为第一个参数通过：

```
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function():
    ...
```

请注意，您还必须传递一个原因（请参阅 pytest.mark.xfail ）可以使用 reason 参数：

```
@pytest.mark.xfail(reason="known parser issue")
def test_function():
    ...
```

如果要更具体地说明测试失败的原因，可以在 raises 参数 如果测试失败，则报告为常规失败，除非 raises .

```
@pytest.mark.xfail(raises=RuntimeError)
def test_function():
    ...
```

如果测试应标记为xfail并报告为xfail，但不应执行，则使用 run 参数AS False 这对于Xfailing测试特别有用，这些测试会使解释器崩溃，应该稍后进行调查

```
@pytest.mark.xfail(run=False)
def test_function():
    ...
```

两个 XFAIL 和 XPASS 默认情况下不要让测试套件失败。您可以通过设置 strict 仅关键字参数到 True ：

```
@pytest.mark.xfail(strict=True)
def test_function():
    ...
```

这将使 XPASS 此测试的（“意外通过”）结果将使测试套件失败。您可以更改 strict 参数使用 xfail_strict ini选项：
```
[pytest]
xfail_strict=true
```

通过在命令行上指定 忽略x失败

```
pytest --runxfail
```

您可以强制运行和报告 xfail 将测试标记为完全没有标记。这也导致 pytest.xfail() 不产生效果。

实例
下面是一个简单的测试文件，有几种用法：
```
import pytest
xfail = pytest.mark.xfail

@xfail
def test_hello():
    assert 0

@xfail(run=False)
def test_hello2():
    assert 0

@xfail("hasattr(os, 'sep')")
def test_hello3():
    assert 0

@xfail(reason="bug 110")
def test_hello4():
    assert 0

@xfail('pytest.__version__[0] != "17"')
def test_hello5():
    assert 0

def test_hello6():
    pytest.xfail("reason")

@xfail(raises=IndexError)
def test_hello7():
    x = []
    x[1] = 1
```

使用“报告xfail”选项运行它可以得到以下输出：

```
example $ pytest -rx xfail_demo.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR/example
collected 7 items

xfail_demo.py xxxxxxx                                                [100%]

========================= short test summary info ==========================
XFAIL xfail_demo.py::test_hello
XFAIL xfail_demo.py::test_hello2
  reason: [NOTRUN]
XFAIL xfail_demo.py::test_hello3
  condition: hasattr(os, 'sep')
XFAIL xfail_demo.py::test_hello4
  bug 110
XFAIL xfail_demo.py::test_hello5
  condition: pytest.__version__[0] != "17"
XFAIL xfail_demo.py::test_hello6
  reason: reason
XFAIL xfail_demo.py::test_hello7
============================ 7 xfailed in 0.12s ============================
```

当使用参数化时，可以对单个测试实例应用诸如skip和xfail之类的标记：

```
import sys
import pytest


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
        (2, 3),
        (3, 4),
        (4, 5),
        pytest.param(
            10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k")
        ),
    ],
)
def test_increment(n, expected):
    assert n + 1 == expected
```