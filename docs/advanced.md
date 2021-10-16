相信如果熟悉了[快速入门](quickstart.md)的就会知道部分动态参数的使用以及手工用例的编写，下面将会讲解纯YAML版的用例维护的细节

!!! question "若你想给测试报告中打个tag 那么你可以在yaml中声明allures属性"

```
iutils/AllureUtils.py:21 --> 可以自行增加、目前仅适用于以下几种
:param severity:  优先级
:param epic:      史诗级
:param feature:   一级标签 用于描述被测试产品需求
:param story:     二级标签 用于描述feature的用户场景，即测试需求
:param title:     标题 用于描述用例名称
:param description:  备注信息
```

!!! question "若你想参数化url、那么可以使用list给包含起来并配置动态键值"

```
iutils/OkHttps.py:265 -->
可以写成[dns,path]或者单个str类型完整路径
1.使用list包含则需在dns_（profiles）.yaml中声明url/address中声明path
2.使用完整url 就只需str的即可
注意：
1.如果写法不正确则会报错：raise IndexError("自动模式下必须要先配置Host及Url或者仅传入Path，且为List例如：[host,url_path]")
2.如果最后发送请求的url不是有效re.match(r'^https?:/{2}\w.+$', url)也会报错：raise Exception("%s-不是有效Url！！！" % (url))
```

!!! question "若你想在当前用例的执行前调用其它前置用例、可以使用depends"

```
depends: ["test_helper.yaml","search_001,search_002"]
depends: {"path":"test_depends.yaml","case":["test_depends_001","test_depends_002"]}
```

!!! question "若你想在当前用例的执行前调用其它其它的函数、可以使用tlackback"

```
在根目录下创建一个tlackback.py 之后的函数引用即可
tlackback: ["**kwargs"]
例如：
from iutils.Helper import RandValue
def randInt(min_,max_):
    return RandValue.getInt("{min_},{max_}".format(min_=min_, max_=max_))
使用：
tlackback: ["randInt(1,100)","randInt(1,500)"]
```

!!! question "若你想先提取后使用参数则可以结合extract、$VAL_来实现"

```
实例：query_user_info接口response结果如下
{
    "data": {
        "curPage": 1,
        "datas": [
            {
                "anonymous": 0,
                "appendForContent": 0,
                "articleId": 15500,
                "content": "<p>🐮</p>",
                "contentMd": "🐮",
                "id": 1555,
                "status": True,
                "toUserId": 0,
                "toUserName": "",
                "userId": 26628,
                "userName": "gaoandroid",
                "zan": 0
            }
        ],
        "offset": 0,
        "pageCount": 1,
        "size": 200,
        "total": 20
}
    }
1. 需要提取status、userId、total三个值
那么可以在yaml中新增一个extract节点：
extract:
 user_info_userId: $.data.datas[0].userId
 user_info_Status: $.data.datas[0].status
 user_info_total: $.data.total
2.在下一个用例中可以使用$VAL_调用 (目前只适用于header以及json/params/data 可扩展)
$VAL_USER_INFO_USERID,...,... #可以大小写随意、有函数强转了、但必须唯一 
ivar = {"$VAR_%s" % (str(key).upper()): _value[0] if _value else None}
```

!!! question "若你想效验值，那么可以加上validation来实现，具体效验方式如下"

```
validation:
    expected_code: status_code
    expected_field:
      $.value_001: [str_eq,""] #文本对比
      $.value_002: [">||<||≥||≤||...",equal_var] #number对比
      $.value_003: "equal_text" # 文本值相等比较也可以这样子写
    expected_content: dict的json返回值
    expected_border: [left,own,right] # 左右边界值比较
    expected_reason: reason # 请求状态 与expected_code类似
    expected_text: body_text # html返回体相等比较
    expected_schema: json_schema # json结构体比较
    expected_time: outtime # 响应时间对比
```

!!! question "若你想在json/data/params中引用其它的yaml动态参数，你可以使用shader"
```
只需在request下新增一个shader，并按照规定传值：
request:
  shader: {"path":"file_path","file":"file_name","var_key":"key", "method":"params"}
  备注：
  1. path/var_key（非必填项、默认取test_yaml下的、及整个yaml文件数据）
  2. 若传参了则可扫描对应的目录下对应的文件、且可以指定某个键值
简单案例如下：
test_shader_case.yaml===>
    config:
      - headers:
          accept: application/json, text/plain, */*
          accept-encoding: gzip
          accept-language: zh-CN,zh;q=0.9
          content-type: application/json;charset=UTF-8
          user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
              like Gecko) Chrome/92.0.4515.107 Safari/537.36
      - allures:
          feature: 引用其它的yaml动态参数(部分参数固定值仅做测试)
          severity: normal
      - request:
          method: get
          url:  [localhost,8001]
    test_setup:
      shader_001:
        headers:
          accept: application/json, text/plain, */*
          accept-encoding: gzip
          accept-language: zh-CN,zh;q=0.9
        request:
          method: post
          url:  https://test.com
          shader: {"file":"shader.yaml", "method":"params"}
        validations:
          expected_code: 200
          expected_content: {"code":200,"message":"","error":"","details":null}
          expected_time: 10
          expected_border: [left,own,right]
shader.yaml===> 外部引用
{"Int": "${randInt}","ComputeTime": "${randTime(10timestamp)}","Letters": "${randLetters}","Sample": "${randSample}"}
# 备注：test_shader用例发送请求时就会把shader.yaml下所有内容当做对应的method形式发送也就是params、对应的还有data/json俩类型
test_shader.py===>
from iutils.OkHttps import Httpx
from testings.control.init import Envision
config = Envision.getYaml("test_shader_case.yaml")['config']
test_setup = Envision.getYaml("test_shader_case.yaml")['test_setup']
class TestHelper():
    def test_helper_test_get(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["shader_001"]])
```
