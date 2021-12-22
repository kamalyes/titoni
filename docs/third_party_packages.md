### 调整case执行顺序

pytest默认按字母顺序去执行的（小写英文--->大写英文--->0-9数字）按照ASCLL码排序，文件内的用例按照从上往下执行

```
setup_module->setup_class->setup_function->testcase->teardown_function->teardown_claas->teardown_module
```

可以通过第三方插件pytest-ordering实现自定义用例执行顺序 [官方文档](https://pytest-ordering.readthedocs.io/en/develop/)

注意：一旦设置了自定义的执行顺序，就必须得延伸@pytest.mark.run(order=1)里面得order字段

!!! tip "pip install pytest-ordering"

```
方式一
第一个执行：@ pytest.mark.first
第二个执行：@ pytest.mark.second
倒数第二个执行：@ pytest.mark.second_to_last
最后一个执行：@pytest.mark.last

方式二
第一个执行：@ pytest.mark.run('first')
第二个执行：@ pytest.mark.run('second')
倒数第二个执行：@ pytest.mark.run('second_to_last')
最后一个执行：@ pytest.mark.run('last')

方式三 （推荐写法）
第一个执行：@ pytest.mark.run(order=1)
第二个执行：@ pytest.mark.run(order=2)
倒数第二个执行：@ pytest.mark.run(order=-2)
最后一个执行：@ pytest.mark.run(order=-1)

```

已经改变了用例执行规则，针对于是全局的，会先执行完@pytest.mark.run(order=1)才会执行order=2的用例
其实总体来说，这个插件的实用场景不是很多，如果需要指定某个用例第一个执行和最后执行，可以用该插件实现。
如果要按照你指定的顺序执行下去，需要在每个用例前都加上@pytest.mark.run(order=1)，其中order中的数字需递增。

### 跳过执行 pytest-dependency

!!! summary "先来一个前一个case失败后者不会执行的简单案例"

```
import pytest
@pytest.mark.dependency()
def test_dependency_001():
    assert 1==2

@pytest.mark.dependency(depends=["test_dependency_001"])
def test_dependency_002():
    print("test_dependency_001 Assert 通过 所以会执行到我")
    
================================== FAILURES ===================================
_____________________________ test_dependency_001 _____________________________

    @pytest.mark.dependency()
    def test_dependency_001():
>       assert 1==2
E       assert 1==2

Helper.py:5: AssertionError
=========================== short test summary info ===========================
FAILED Helper.py::test_dependency_001 - assert False
======================== 1 failed, 1 skipped in 0.18s =========================
```

!!! summary "再来一个前置Case效验通过后者会继续执行的例子"

```
import pytest
@pytest.mark.dependency()
def test_dependency_001():
    assert True

@pytest.mark.dependency(depends=["test_dependency_001"])
def test_dependency_002():
    print("test_dependency_001 Assert 通过 所以会执行到我")
    
============================= test session starts =============================
platform win32 -- Python 3.7.6, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: E:\WorkSpace\PycharmProjects\ProtocolTest, configfile: pytest.ini
plugins: allure-pytest-2.8.0, Faker-8.10.1, PyTestReport-0.2.1, assume-2.4.2, dependency-0.5.1, html-3.1.1, instafail-0.4.2, metadata-1.11.0, ordering-0.6, parallel-0.1.0, report-0.2.1, reportlog-0.1.2, rerunfailures-10.0, sugar-0.9.1, timeout-1.4.2, tmreport-1.3.7
collected 2 items
xxx.py .test_dependency_001 Assert 通过 所以会执行到我
============================== 2 passed in 0.16s ==============================

```
### Pytest部分说明

!!! note "pytest配置文件"

```
;addopts 参数说明
; -s：输出调试信息，包括print打印的信息。
; -v：显示更详细的信息。
; -q：显示简略的结果 与-v相反
; -p no:warnings 过滤警告
; -n=num：启用多线程或分布式运行测试用例。需要安装 pytest-xdist 插件模块。
; -k=value：用例的nodeid包含value值则用例被执行。
; -m=标签名：执行被 @pytest.mark.标签名 标记的用例。
; -x：只要有一个用例执行失败就停止当前线程的测试执行。
; --maxfail=num：与-x功能一样，只是用例失败次数可自定义。
; --reruns=num：失败用例重跑num次。需要安装 pytest-rerunfailures 插件模块。
; -l: 展示运行过程中的全局变量和局部变量
; --collect-only: 罗列出所有当前目录下所有的测试模块，测试类及测试函数
; --ff: 如果上次测试用例出现失败的用例，当使用--ff后，失败的测试用例会首先执行，剩余的用例也会再次执行一次 *基于生成了.pytest_cache文件
; --lf: 当一个或多个用例失败后，定位到最后一个失败的用例重新运行，后续用例会停止运行。*基于生成了.pytest_cache文件
; --html=report.html: 在当前目录生成名为report.html的测试报告 需要安装 pytest-html 插件模块。
```

!!! note "fixture常用特性"

```
fixture_marker = FixtureFunctionMarker(
scope=scope, params=params, autouse=autouse, ids=ids, name=name,)
scope -- 共享这个设备的范围；一个 "function" （默认） "class" ， "module" ， "package" 或 "session" . 此参数也可以是接收 (fixture_name, config) 作为参数返回 str 使用上面提到的值之一。看到了吗 动态范围 更多信息，请参阅文档。
params -- 一个可选的参数列表，它将导致多次调用fixture函数和使用它的所有测试。当前参数在中可用 request.param .
autouse -- 如果为True，那么fixture函数将为所有可以看到它的测试激活。如果为False（默认值），则需要显式引用来激活设备。
ids -- 字符串id的列表，每个与参数相对应，因此它们是测试id的一部分。如果没有提供id，则将从参数自动生成这些id。
name -- 设备的名称。默认为修饰函数的名称。如果fixture是在定义fixture的同一个模块中使用的，那么fixture的函数名将被请求fixture的函数arg隐藏；解决这个问题的一种方法是命名修饰函数 fixture_<fixturename> 然后使用 @pytest.fixture(name='<fixturename>') .
```
!!! summary "调用fixture的三种方法"

1.函数或类下面的函数直接传fixture的函数参数名称

```
import pytest
# 仅函数
@pytest.fixture()
def test_function_001():
    print('\n开始执行test_function_001')
    return 'Hello Word!'

def test_use_fixture_001(test_function_001):
    print('---我是test_use_fixture_001---,%s'%(test_function_001))

# 类中函数调用
class TestCase:
    def test_use_fixture_002(self, test_function_001):
        print('---我是test_use_fixture_002---,%s' % (test_function_001))

```

2.使用装饰器@pytest.mark.usefixtures()修饰需要运行的用例
```
import pytest

@pytest.fixture(scope="function")
def test_function_001():
    print("\n-----开始执行test_function_001------")

@pytest.mark.usefixtures("test_function_001")
def test_function_002():
    print("------开始执行test_function_002------")

if __name__ == '__main__':
    pytest.main(["-s","usefixtures.py::test_function_002"])
```

3.叠加usefixtures 可以使用@pytest.mark.usefixture() 
!!! warning "注意叠加顺序，先执行的放底层，后执行的放上层"

```
import pytest

@pytest.fixture()
def test_function_001():
    print('\n开始执行function1')

@pytest.fixture()
def test_function_002():
    print('\n开始执行function2')

@pytest.mark.usefixtures('test_function_001')
@pytest.mark.usefixtures('test_function_002')
def test_usefixtures_125():
    print('---用例test_usefixtures_125执行---')

@pytest.mark.usefixtures('test_function_002')
@pytest.mark.usefixtures('test_function_001')
class TestCase:

    def test_function_003(self):
        print('---用例test_function_003执行---')

    def test_function_005(self):
        print('---用例test_function_005执行---')

if __name__ == '__main__':
    pytest.main(["-s","usefixtures.py::TestCase::test_function_005"])
```

5.如果不想直接用func_name想要重命名fixture，那么可以使用name参数

```
import pytest

@pytest.fixture(name="rename_fixture")
def test_function_001():
    print('\n开始执行test_function_001')
    return 'Hello Word!'

def test_use_fixture_005(rename_fixture):
    print('---我是test_use_fixture_001---,%s'%(rename_fixture))
```

6.共享范围说明
```
scope = 'function' 测试函数维度，默认范围，则在测试结束时销毁fixture
scope = 'class' 测试类维度，在class中最后一次测试的拆卸过程中，夹具被破坏
scope = 'module' 测试文件维度，在模块中最后一次测试的拆卸过程中，夹具被破坏
scope = 'session' 测试会话维度，夹具在测试会话结束时被销毁
案例 可多变 实际的结果太多调试下看看吧：
import pytest
@pytest.fixture(scope ='class', name="function_is_use")
def test_function_001():
    print('\n开始执行test_function_001')

@pytest.mark.usefixtures('function_is_use')
class TestCase001:
    def test_function_003(self):
        print('---用例test_function_003执行---')

    def test_function_005(self):
        print('---用例test_function_005执行---')

@pytest.mark.usefixtures('function_is_use')
class TestCase002:
    def test_function_006(self):
        print('---用例test_function_006执行---')

if __name__ == '__main__':
    pytest.main(["-s","usefixtures.py"])

```