首先，你需要修改..\config\push_message.yaml下的配置

```
email:
  # 发件人邮箱
  user:  "user"
  # 发件人邮箱授权码
  password:  "password"
  # 邮箱host
  host:  "host"
  contents:  请使用已安装Live Server 插件的VsCode或者其它Ide，打开index.html查看报告
  # 收件人邮箱
  addressees:  ["addressees001","addressees002"]
  title:  title
  # 附件
  enclosures: report.zip

jenkins:
  # 用户名
  user:  "user"
  # 密码
  password:  "password"
  # 项目名
  job_name: "job_name"
  # 连接地址
  build_url: "build_url"

robot:
  # 企业微信私钥
  debug_qywx_key: "debug use"
  qywx_key: "prod use"

other:
  # 项目概述
  product: "product_name"
```

接下来需要修改Jenkins Execute shell配置

!!! warning "从未部署CI/CD的可以先了解[快速搭建Jenkins+Allure环境](continue_integration.md)"

```
#!/bin/bash
cd ${WORKSPACE}
python3 RunAll.py
python3 -m pytest -vs --alluredir ${WORKSPACE}/allure_report
python3 Message.py
```