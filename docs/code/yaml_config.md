```
config: 父类的配置
- headers: (必填)
- allures:  
- request: (必填)
test_setup: 用例准备 子类与父类公用的字段优先级：子类=不配置>父类
  test_name: case名称 需要唯一
    allures: 
    headers: 
    request: 
    validations: (参数效验)
      expected_code: status_code 验证码比较
      expected_text: 暂时不要用
      expected_content: content  完整响应体比较
      expected_field: (单字段效验)
        json_path: [eq_method,var]
        .....
      expected_time: timeout
      expected_schema: json_schema
    extracts: (提取参数)
        var_name: json_path
        .....
    sql: (数据库效验 暂不支持)
      before_call_sql:
      before_do_sql:
      after_call_sql:
      after_do_sql:
```