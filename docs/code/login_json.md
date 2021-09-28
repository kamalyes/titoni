```pycon
{
  "config": [
    {
      "headers": {
        "host": "localhost:8006",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win65; x65) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.5577.82 Safari/537.36",
        "content-type": "application/json;charset=UTF-8",
        "referer": "http://localhost:8006/",
        "accept-encoding": "gzip",
        "accept-language": "zh-CN,zh;q=0.9"
      }
    },
    {
      "allures": {
        "severity": [
          "# blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）",
          "# critical级别：临界缺陷（ 功能点缺失）",
          "# normal级别：普通缺陷（数值计算错误）",
          "# minor级别：次要缺陷（界面错误与UI需求不符）",
          "# trivial级别：轻微缺陷（必输项无提示，或者提示不规范）"
        ],
        "feature": "用于描述被测试产品需求",
        "story": "用于描述feature的用户场景，即测试需求",
        "title": "用于描述用例名称",
        "description": "这是用例描述"
      }
    },
    {
      "request": {
        "method": "POST",
        "url": "http://localhost:8006/api/login"
      }
    }
  ],
  "test_setup": {
    "apilogin": {
      "headers": "子级扩展头部信息（写法与父类一致）",
      "allures": "子级扩展allure配置（写法与父类一致）",
      "validations": {
        "expected_time": 157,
        "expected_code": 200,
        "expected_text": "OK",
        "expected_content": "{\n  \"data\": {\n    \"account\": \"dengrr\", \n    \"create_user\": 1, \n    \"created_time\": \"2021-09-28 12:27:59\", \n    \"id\": 2, \n    \"name\": \"\\u7ba1\\u7506\\u5558\", \n    \"role_id\": 2, \n    \"status\": 1, \n    \"token\": \"eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzMjgyODUxMSwiZXhwIjoxNjMyODY0NTExfQ.eyJpZCI6Mn0.D1EFWprk5IQ9Q8YsyLQqAAUHeHKWrrS9bRm5FwdP_slQRGhxOWYRwC1zaKGgscElQF57dF5gAg1CqJSpDJZc5w\", \n    \"update_time\": \"2021-09-28 12:33:55\"\n  }, \n  \"message\": \"\\u767b\\u5f55\\u6210\\u529f\", \n  \"status\": 200\n}",
        "expected_field": [
          {
            "$.variables1": "value1"
          },
          {
            "$.variables2": "value2"
          }
        ],
        "expected_schema": "json_schema"
      },
      "sql": {
        "before_call_sql": "",
        "before_do_sql": "",
        "after_call_sql": "",
        "after_do_sql": ""
      },
      "extract": [
        {
          "var_name001": "json_path"
        },
        {
          "var_name002": "json_path"
        }
      ]
    }
  }
}
```