## Case编写规范
#### 一、全自动模式
1. 调用iutils模块下的HarToData或者手动创建一个测试yaml数据格式如下：

```
config:
- headers:
- allures:
- request:
test_setup:
  test_name:
    allures:
    headers:
    request:
    validations:
      expected_code: status_code
      expected_content: content
      expected_variables: (单字段效验)
        json_path: [eq_method,var]
      expected_time: timeout
      expected_schema: json_schema
    extracts:
        var_name: json_path
    sql:
      before_call_sql:
      before_do_sql:
      after_call_sql:
      after_do_sql:
```

2. 创建一个文件目录（即模块说明）
3. 在对接模块下创建一个测试类 （需注意的是开头需要与pytest.ini配置文件中的python_files保持一致）
4. 编写case：

```
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestClass():
    def test_func_xxx(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["test_name"]])        
```

#### 二、手动
1. 所有的数据来源在case中声明于调用request模块保持一致

#### 三、混合模式
1. yaml+case均给了参数 默认以最后声明者为主

```
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestClass():
    def test_func_xxx(self):
        url= url
        method = method,aided= True
        data, json, params = randData()
        hook_header= extend_headers
        esdata=[config, test_setup["test_name"]]
        Httpx.sendApi(method=method, url=url, aided=True,hook_header=hook_header,data=data,esdata=esdata)
```

#### 四、case上下联动
1. 在全自动模式下需要给extracts参数
2. 手动模式下可以req进行赋值调用Httpx中的获取对应值的函数来实现数据依赖

#### 五、调试测试类

```
import pytest
pytest.main(["-v","test_project.py"])
pytest.main(["-v","test_project.py::TestClass"])
pytest.main(["-v","test_project.py::TestClass::test_func"])
```

#### 六、不同方式的数据请求说明
1. params:字典或者字节序列作为参数增加到URL中多半用于get

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

2. data|json都是用于post提交的、但是区别在于：不同在于data需要强转json.dumps格式、json参数会自动将字典类型的对象转换为json格式

```
response = Httpx.sendApi(method="post", url=url, json=target_data)
等同于：
response = Httpx.sendApi(method="post", url=url, json=json.dumps(target_data,ensure_ascii=False))
```

#### 七、断言
1. 原生assert

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
 
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    assert x == y  #如果这个断言失败，则后续都不会执行
    assert True
    assert False
```

2. pytest-assume

```
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
通过上下文管理器with使用pytest-assume

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

主要注意的是，如果上下文管理器里面包含多个断言，则只有第一个会被执行，如

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
