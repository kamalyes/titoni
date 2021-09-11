## allure及pytest
#### 一、fixture常用特性
```
fixture_marker = FixtureFunctionMarker(
scope=scope, params=params, autouse=autouse, ids=ids, name=name,)
scope -- 共享这个设备的范围；一个 "function" （默认） "class" ， "module" ， "package" 或 "session" . 此参数也可以是接收 (fixture_name, config) 作为参数返回 str 使用上面提到的值之一。看到了吗 动态范围 更多信息，请参阅文档。
params -- 一个可选的参数列表，它将导致多次调用fixture函数和使用它的所有测试。当前参数在中可用 request.param .
autouse -- 如果为True，那么fixture函数将为所有可以看到它的测试激活。如果为False（默认值），则需要显式引用来激活设备。
ids -- 字符串id的列表，每个与参数相对应，因此它们是测试id的一部分。如果没有提供id，则将从参数自动生成这些id。
name -- 设备的名称。默认为修饰函数的名称。如果fixture是在定义fixture的同一个模块中使用的，那么fixture的函数名将被请求fixture的函数arg隐藏；解决这个问题的一种方法是命名修饰函数 fixture_<fixturename> 然后使用 @pytest.fixture(name='<fixturename>') .
```
scope详细说明
1. scope = 'function' 测试函数维度，默认范围，则在测试结束时销毁fixture。
2. scope = 'class' 测试类维度，在class中最后一次测试的拆卸过程中，夹具被破坏。
3. scope = 'module' 测试文件维度，在模块中最后一次测试的拆卸过程中，夹具被破坏。
4. scope = 'session' 测试会话维度，夹具在测试会话结束时被销毁。

#### 二、allure标签
1. @allure.epic()	epic描述	敏捷里面的概念，定义史诗，往下是feature
2. @allure.feature()用于描述被测试产品需求
3. @allure.story() 用于描述feature的用户场景，即测试需求
4. @allure.title() 用于描述用例名称 重命名html报告名称
5. @allure.step() 用于描述用例步骤
6. @allure.description() 用于描述用例，支持html显示
7. allure.attach() 用于添加附件
8. @allure.severity() 用于描述用例级别 
    ```
    - blocker　 阻塞缺陷（功能未实现，无法下一步）
    - critical　　严重缺陷（功能点缺失）
    - normal　　 一般缺陷（边界情况，格式错误）
    - minor　 次要缺陷（界面错误与ui需求不符）
    - trivial　　 轻微缺陷（必须项无提示，或者提示不规范）
    ```
8. @allure.testcase()	测试用例的链接地址	对应功能测试用例系统里面的case
9. @allure.issue()	缺陷	对应缺陷管理系统里面的链接
10. @allure.link()	链接	定义一个链接，在测试报告展现

函数外部调用
```
import pytest
import allure
@allure.epic()
@allure.severity('critical')
@allure.feature('用于描述被测试产品需求')
@allure.story('用于描述feature的用户场景，即测试需求')
@allure.title('用于描述用例名称')
def test_01():
    # 可以在用例内部编写用例步骤，等同于@allure.step()
    # 步骤必须写在方法内部，注意格式
    with allure.step('描述步骤'):
        # allure.attach可以向报告中添加附件
        with open(file_path, 'rb') as file:
            img = file.read()
        allure.attach(img, '这是....附件')
    pass
```
函数内部调用
```
def test02():
    allure.dynamic.severity('critical')
    allure.dynamic.feature('用于描述被测试产品需求')
    allure.dynamic.story('用于描述feature的用户场景，即测试需求')
    allure.dynamic.title('用于描述用例名称')
    allure.dynamic.description('这是用例描述')
    pass
```
封装后的调用
```
    1. setTag(test_setup["xxx"]["allures"]) 
    以上写法依赖yaml配置 （全局或单例都可以）：
    config:
    - allures:
        severity: 等级
        feature: 用于描述被测试产品需求
        story: 用于描述feature的用户场景
        title: 用于描述用例名称     
        description: 这是继承测试的用例描述
    test_setup:
      xxx_case:
        allures:
          severity: 等级
          feature: 用于描述被测试产品需求
          story: 用于描述feature的用户场景
          title: 用于描述用例名称     
          description: 这是继承测试的用例描述
    2. setTag(
      {'feature': '用于描述被测试产品需求',
     'severity': '等级',
     'story':'用于描述feature的用户场景',
     'title':'用于描述用例名称',
     'description': '这是用例描述'})
```
#### 三、 case执行顺序调整
1. pytest默认按字母顺序去执行的（小写英文--->大写英文--->0-9数字）
2. 用例之间的顺序是文件之间按照ASCLL码排序，文件内的用例按照从上往下执行
```
setup_module->setup_claas->setup_function->testcase->teardown_function->teardown_claas->teardown_module
```
3. 可以通过第三方插件pytest-ordering实现自定义用例执行顺序
官方文档： https://pytest-ordering.readthedocs.io/en/develop/
注意：一旦设置了自定义的执行顺序，就必须得延伸@pytest.mark.run(order=1)里面得order字段
```
pip install pytest-ordering
```
1. 方式一
```
第一个执行：@ pytest.mark.first
第二个执行：@ pytest.mark.second
倒数第二个执行：@ pytest.mark.second_to_last
最后一个执行：@pytest.mark.last
```
方式二
```
第一个执行：@ pytest.mark.run('first')
第二个执行：@ pytest.mark.run('second')
倒数第二个执行：@ pytest.mark.run('second_to_last')
最后一个执行：@ pytest.mark.run('last')
```
方式三
```
第一个执行：@ pytest.mark.run(order=1)
第二个执行：@ pytest.mark.run(order=2)
倒数第二个执行：@ pytest.mark.run(order=-2)
最后一个执行：@ pytest.mark.run(order=-1)
```
已经改变了用例执行规则，针对于是全局的，会先执行完@pytest.mark.run(order=1)才会执行order=2的用例
其实总体来说，这个插件的实用场景不是很多，如果需要指定某个用例第一个执行和最后执行，可以用该插件实现。
如果要按照你指定的顺序执行下去，需要在每个用例前都加上@pytest.mark.run(order=1)，其中order中的数字需递增。
#### 四、跳过执行 pytest-dependency
1. 首先我们需要在用例开始的位置打上一个装饰器@pytest.mark.dependency()，这是代表这条用例作为主条件，如果这条用例失败，关联它的用例会跳过执行。
在被关联的用例上，也打上带参数的装饰器@pytest.mark.dependency()，depends接受的参数是关联的依赖用例名。
在depends也可以用别名的方式指定用例名。
用过unittest的童鞋都知道，有两个前置方法，两个后置方法；分别是
```
setup()
setupClass()
teardown()
teardownClass()
```
Pytest也贴心的提供了类似setup、teardown的方法，并且还超过四个，一共有十种
```
模块级别：setup_module、teardown_module
函数级别：setup_function、teardown_function，不在类中的方法
类级别：setup_class、teardown_class
方法级别：setup_method、teardown_method
方法细化级别：setup、teardown
```

#### 五、pytest-ini

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
