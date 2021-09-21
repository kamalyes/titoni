# Advanced Usage

If you are not familiar with the basic features of sendApi, it is recommended that you write the appropriate entry level cases [Quickstart](quickstart.md)

### Why use auto?

!!! note "TL;DR"
    
    Automatic mode of httpx.sendAPI is highly recommended if you find singleton mode too cumbersome, use case management poor, and more than just experiments, one-time scripts, or prototypes
    
### Full automatic mode

Call HarToData under the iutils module or manually create a test YAML data format as follows:

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

Create a file directory (module description)

Create a test class under the docking module (note that the start must be consistent with python_files in the PyTest.ini configuration file)

Write a case:

```
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestClass():
    def test_func_xxx(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["test_name"]])        
```

### Hand Movement

All data sources are declared in case consistent with the call to the Request module

### Mixed mode

Yaml + Case all give arguments to the last declarator by default

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

!!! Hint

    Now, let's get started
   
First, you need to create a test YAMl file in ..\testings\dao\test_yaml.

```shell
config:
- headers:
    accept: application/json, text/plain, */*
    accept-encoding: gzip
    accept-language: zh-CN,zh;q=0.9
    content-type: application/json;charset=UTF-8
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
      like Gecko) Chrome/92.0.4515.107 Safari/537.36
- allures:
    feature: 函数助手测试(部分参数固定值仅做测试)
    severity: normal
- request:
    method: get
    url:  [localhost,8001]
test_setup:
  search_001:
    allures:
      severity: critical
      description: 这是继承测试的用例描述
      story: 单条url&全局的用户自定义变量
    headers:
      accept: application/json, text/plain, */*
      accept-encoding: gzip
      accept-language: zh-CN,zh;q=0.9
    request:
      method: post
      url:  https://www.so.com/s
      params: {"Int": "{{Int}}","ComputeTime": "{{ComputeTime}}","Letters": "{{Letters}}","Sample": "{{Sample}}"}
    validations:
      expected_code: 200
      expected_content: {"code":200,"message":"","error":"","details":null}
      expected_time: 10
    sql:
      before_call_sql:
      before_do_sql:
      after_call_sql:
      after_do_sql:  
```

!!! note "Urls"
        
    You need create a description in ..\application.properties.yaml environment 
    
    And  Declare DNS and PATH in ...\testings\config\properties

```shell
application.properties.yaml   --> profiles: "dev/sit/uat/pord"
address.yaml --> 8001:"8001"
dns_xx.yaml  --> localhost: "localhost"
```

!!! note "Params"
        
You can do it at... Create a description in ...\testings\config\properties

```shell
user_vars.yaml -->
Int: ${randInt}
Float: ${randFloat(10,5,2)}
randPwd: ${randPwd()}
Custom_INT_VAR: 12356789
Custom_STR_VAR: 12356789ABCDEFG
Custom_None_VAR: NONE
Custom_NULL_VAR: null
```

Again in YAML to declare or call in a function You can write this directly in yaml_case

```shell
json/data/params: {"Int": "{{Int}}","ComputeTime": "{{ComputeTime}}","Letters": "{{Letters}}","Sample": "{{Sample}}"}
```

If you want to call random dynamics in case alone you can do this

```shell
json/data/params: {"Int": "${randInt}","ComputeTime": "${randTime(10timestamp)}","Letters": "${randLetters}","Sample": "${randSample}"}
```

If you don't feel secure in any of these parameters you can call encryption

```shell
json/data/params: {"md5": "$ENC_(md5,Md5参数加密)"}
json/data/params: {"sha1": "$ENC_(sha1,Sha1参数加密)"}
json/data/params: {"base64": "$ENC_(base64,Base64参数加密)"}
```

!!! note "Extract"

    Of course in case there is a hierarchy linkage you can do this

```shell
test_yaml/test.yaml declares extract
extract:
    vars_001: "$.data.vars_001"
    vars_002: "$.data.vars_002"
```

Link parameter extraction will be automatically stored in ..\testings\config\variables\global.yaml And If you want to call it in the next case the thing to notice is that this is converted to uppercase and if the last parameter is empty then the value that you fill in is also empty

```shell
json/data/params: {"vars_001": "$VAR_VARS_001","vars_002": "$VAR_VARS_002"}
```

You can call these functions in addition to those in the examples above

```
   randInt(min_=1, max_=100) 随机生成整数
   randFloat(min=0, max=1, length=2) 随机生成浮点数
   randTime(layout) 随机生成时间
   randComputeTime 随机生成偏移时间
   randLetters(length=10) 随机生成字母
   randSample(elements=default_elements) 随机生成字符（英文+数字）
   randNumber() 随机生成手机号
   randName() 随机生成名字
   randAddress() 随机生成所在地址
   randCountry() 随机生成国家名
   randCountryCode() 随机生成国家代码
   randCityName() 随机生成城市名
   randCity()  随机生成城市
   randProvince() 随机生成省份
   randEmail() 随机生成email 
   randIpv4() 随机生成IPV4地址
   randLipate() 随机生成车牌号
   randColor() 随机生成颜色
   randSafeHexColor() 随机生成16进制的颜色
   randColorName() 随机生成颜色名字
   randCompanyName() 随机生成公司名
   randJob() 随机生成工作岗位
   randPwd() 随机生成密码
   randUuid4() 随机生成uuid
   randSha1() 随机生成sha1
   randMd5() 随机生成md5
   randFemale() 随机生成女性名字
   randMale() 随机生成男性名字
   randUserInfo() 随机生成粗略的基本信息
   randUserInfoPro() 随机生成详细的基本信息
   randUserAgent() 随机生成浏览器头user_agent
   randIdCard() 随机生成身份证
   getUserVars(global) 获取全局变量

   json/data/params: {"vars_001": "${randInt}","vars_002": "${randInt(5,6)}"}
   json/data/params: {"vars_001": "${randNumber}","vars_002": "${randNumber()}"}
   
```

!!! note "Assert"

    Comparison of expected and actual values You can do five things
    
```shell    
validations:
      expected_code: status_code
      expected_variables:
        $.code: Service response code
        $.data.vars_0001: "expected_var"
        $.data.vars_0002: "expected_var"
      expected_time: expected_timeout
      expected_schema: json_schema
```

If you don't think these effects are thoughtful enough then you can call more type comparisons
   
```shell
contrast in ["eq", "equal", "=="]
contrast in ["lt", "less_than", "lessThan", "<"]
contrast in ["le", "less_or_equal", "lessOrEqual", "<=", "≤"]:
contrast in ["gt", "greater_than", "greaterThan", ">"]:
contrast in ["ge", "greater_or_equal", "greaterOrEqual", ">=", "≥"]:
contrast in ["ne", "not_equal", "notEqual", "!=", "≠"]:
contrast in ["str_eq", "string_equal", "stringEqual"]
contrast in ["str_lg", "str_length", "strLength"]
contrast in ["re","regexMatch"]
contrast in ["bg","beginSwith"]
contrast in ["end","endSwith"]

validations:
      expected_variables:
        $.data.vars_0001: ["lt",1]
        $.data.vars_0002: ["gt",5]
        $.data.vars_0003: ["str_eq","expected_var"]
```

If you don't think that's advanced enough, there's also an external response

```shell
from iutils.OkHttps import Httpx
from pytest_assume.plugin import assume
from iutils.Helper import combData,citeHelper

# Parameter merging can be written in two ways
data = {"test_val":citeHelper("$ENC_(base64,Base64参数加密)")}
data = combData({"key1":"$ENC_(base64,Base64参数加密)"})

response = Httpx.sendApi(method="post", url=url, hook_header={}, json=data)
with assume:
        assert Httpx.getStatusCode(response) == status_code
        assert Httpx.getText(response) == response_text
        assert Httpx.getHeaders(response) == response_headers
        assert Httpx.getEncoding(response) == response_encoding
        assert Httpx.getHttpxd(response) == response_httpxd
        assert Httpx.getResponseTime(response) == response_time
        assert Httpx.getContent(response) == response_content
```

!!! note "SQL"

    If you need to connect to a database to do something you need to register the configuration of the database connection pool in application-path.yaml 
    
    And register it under control/data.py and sql.py
    
    Pay attention to：It is recommended that you use global encapsulation again first

```shell

data.py -->
APPLICATION = Loader.yamlFile(APPLICATION_PATH)
DB_CONFIG = APPLICATION["database"]

sql.py -->
from iutils.MySQLUtils import MysqlTools
from testings.control.data import APPLICATION

DB_HOST = APPLICATION["database"]["host"]
DB_PORT = APPLICATION["database"]["port"]
DB_USER = APPLICATION["database"]["user"]
DB_PASSWORD = APPLICATION["database"]["password"]
DB_NAME = APPLICATION["database"]["db_name"]
DB_CHARSET = APPLICATION["database"]["charset"]

connModel = MysqlTools(host=DB_HOST, user=DB_USER, pass_word=DB_PASSWORD, database=DB_NAME, port=DB_PORT)
connModel.init()

Call it -->

from testings.control.sql import connModel
connModel.dosql("sql")
connModel.callsql("sql")
```

!!! Hint

If you want to learn more about test reports and some of the features of PyTest, you can learn in[Report of Pytest](pytest_allure.md)