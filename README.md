## Git提交规范
```
feat 适用场景：全是新增功能，在旧功能基础上做改动（包含新增，删除）
fix 适用场景：修复bug，包含测试环境和生产环境
refactor 适用场景：重构任何功能，重构前和重构后输入和输出需要完全不变，如果有变化，在改动的部分请使用`feat`
test 适用场景：增加单元测试时
style 适用场景：修改代码格式，代码逻辑完全不变
docs 适用场景：编写注释或者使用文档
```
## 一、整个框架设计思路
1. `OkHttps`+`AllureUtils` 模块进行http的请求及allure报告日志信息注入
2. `pytest`实现单元测试 、`@pytest.mark.parametrize`实现数据驱动（实际业务使用过程中并不灵活，太局限）
3. `HarToData EncrypUtils（加解密）`实现模块自动导出标`RESTful`风格的测试用例 （有依赖性的接口 感觉效率并不高）
4. `Processor` 来实现 前置、后置脚本处理的功能
5. `RandUtils （随机获取字符）FileUtils（文件处理）DataUtils（日期处理）....`来产生测试数据
6. `MySQLUtils`、`RedisUtils`实现过多依赖上级接口调换数据中间挂了的问题
7. `DataKit`、`Loader`、`JsonUtils`、`YamlUtils`、`Template`数据加载及处理部分格式问题
8. `Wrapper` 扩展语法糖
9. `WxRobotTools`、`EmaliUtils`、`JenkinsUtils` 实现企微推送机器人及邮件抄送

## 二、实际目录结构
```
InterfaceTest
├─ config （allure、header、消息推送是的一些配置信息）
│  ├─ allure_feature.yaml
│  ├─ norm_headers.yaml
│  └─ push_message.yaml
├─ environment.properties （allure报告所需的环境变量）
├─ application-prod.yaml  （生成环境配置）
├─ application-sit.yaml   （sit环境配置）
├─ application-uat.yaml   （uat环境配置）
├─ application.properties.yaml （环境声明）
├─ BaseSetting.py          （项目所需引用到的路径配置）
├─ conftest.py             （pytest fixture应用）
├─ iutils  （工具类、若业务用不上的也可以去掉一部分）
│  ├─ AllureUtils.py
│  ├─ AreaCode.py
│  ├─ Assertion.py
│  ├─ ConfigParser.py
│  ├─ DataKit.py
│  ├─ DateUtils.py
│  ├─ DingTalkRobot.py
│  ├─ EmaliUtils.py
│  ├─ EncryptUtils.py
│  ├─ Exceptions.py
│  ├─ FolderUtils.py
│  ├─ HarToData.py
│  ├─ Helper.py
│  ├─ IDCards.py
│  ├─ JenkinsUtils.py
│  ├─ JsonUtils.py
│  ├─ Loader.py
│  ├─ LogUtils.py
│  ├─ MySQLUtils.py
│  ├─ OkHttps.py
│  ├─ PandasUtils.py
│  ├─ Processor.py
│  ├─ RandUtils.py
│  ├─ RedisUtils.py
│  ├─ Shell.py
│  ├─ Swagger.py
│  ├─ Template.py
│  ├─ Wrapper.py
│  ├─ WxRobotTools.py
│  ├─ YamlUtils.py
│  └─ __init__.py
├─ libs  （依赖包）
├─ output（日志产生存等相关输出的路径）
├─ pytest.ini （pytest一些基础配置、注意要ansi编码）
├─ requirements.txt （依赖架包）
├─ RunAll.py  （调试的时候用的主函数）
├─ SendMsg.py  （发送邮件及消息推送）
├─ summary.yaml 存储产生报告结果的
├─ testings  （测试类、主要分config、control、dao、service层具体实现根据不同业务）
│  ├─ config
│  │  ├─ localhost （离线本地数据）
│  │  │  └─ xxxx.yaml
│  │  ├─ properties (域名及url的基础配置)
│  │  │  ├─ dns_prod.yaml
│  │  │  ├─ dns_sit.yaml
│  │  │  └─ dns_uat.yaml
│  │  └─ variables  （自定义参数：如token、全局变量...）
│  │     ├─ token.yaml
│  │     └─ global.yaml
│  ├─ control （一些相关配置：依赖数据、路径、sql连接、url...）
│  │  ├─ data.py
│  │  ├─ init.py
│  │  ├─ path.py
│  │  ├─ sql.py
│  │  ├─ url.py
│  │  ├─ variables.py
│  │  └─ __init__.py
│  ├─ dao  （准备好的测试数据）
│  │  ├─ test_csv
│  │  │  └─ xxxx.csv
│  │  ├─ test_img
│  │  │  └─ xxxx.png
│  │  ├─ test_json
│  │  │  └─ xxxxx.json
│  │  └─ test_yaml
│  │     └─ xxxxx.yaml
│  ├─ entity  （公共实体类）
│  │  ├─ Backend.py
│  │  ├─ Blockette.py
│  │  ├─ Login.py
│  │  └─ Seckill.py
│  └─ service  （case编写）
│     ├─ product
│     │  ├─ test_xxxx_001.py
│     │  └─ test_xxxx_002.py
│     └─ seckilll
│        ├─ test_xxxx_001.py
│        ├─ test_xxxx_002.py
│        ├─ test_xxxx_003.py
├─ _version.py
├─ __init__.py
```
## 三、jenkins 持续集成
1. jenkins 中配置源码 git 路径
2. jenkins 中配置 allure
3. 构建，查看报告

## 四、allure及pytest相关的补充
### 1、fixture常用特性
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

### 2、allure标签
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
### 三、 case执行顺序调整
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
### 四、跳过执行 pytest-dependency
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

### 五、断言原生assert和pytest-assume
```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
 
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    assert x == y  #如果这个断言失败，则后续都不会执行
    assert True
    assert False
 
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_pytest_assume(x, y):
    pytest.assume(x == y) #即使这个断言失败，后续仍旧执行
    pytest.assume(True)
    pytest.assume(False)
```


|断言类型| 1，1 | 1，0 | 0，1 | 结论 |
| :----:| :----: | :----: |:----:| :----: |
| assert | 断言3失败 | 断言1失败 |断言2和断言3不执行|断言1失败，断言2和断言3不执行|assert遇到断言失败则停下|
| pytest.assume | 断言3失败 | 断言1失败 |断言2和断言3继续执行|断言1失败，断言2和断言3继续执行|pytest.assume无论断言结果，全部执行|
1. 通过上下文管理器with使用pytest-assume

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: assert x == y
    with assume: assert True
    with assume: assert False
```

2. 主要注意的是，如果上下文管理器里面包含多个断言，则只有第一个会被执行，如

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
    
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: 
        #只有第一个断言会被执行！
        assert x == y
        assert True
        assert False  
```

## 六、补充
#### 1.不同方式的数据请求说明
params:字典或者字节序列作为参数增加到URL中多半用于get
```
data ={'wd':'params作用域',}
response = requests.get('https://www.baidu.com/s',params=data)
print(response.url)
输出：
https://www.baidu.com/s?wd=params作用域
等同于：
response = requests.get('https://www.baidu.com/s?wd=params作用域')
print(response.url)
```
data|json都是用于post提交的、但是区别在于：不同在于data需要强转json.dumps格式、json参数会自动将字典类型的对象转换为json格式
```
response = Httpx.sendApi(method="post", url=url, json=target_data)
等同于：
response = Httpx.sendApi(method="post", url=url, json=json.dumps(target_data,ensure_ascii=False))
```        
