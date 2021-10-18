<p align="center">
    <em>ProtocolTest 接口自动化测试框架，易于学习，高效编码，生产可用</em>
</p>
<p align="center">
<a href="https://codecov.io/gh/kamalyes/protocoltest" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/kamalyes/protocoltest?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/protocoltest" target="_blank">
    <img src="https://img.shields.io/pypi/v/protocoltest?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

关键特性:

* **高效编码**：提高编写用例速度约 50％ 至 100％。*
* **更少 bug**：减少约 40％ 的人为（开发者）导致错误。*
* **智能**：极佳的编辑器支持。处处皆可<abbr title="也被称为自动完成、智能感知">自动补全</abbr>，减少调试时间。
* **简单**：设计的易于使用和学习，阅读文档的时间更短。
* **简短**：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少。
* **健壮**：生产可用级别的代码。还有生成的交互式测试报告。
* **标准化**：基于（并完全兼容）API 的相关开放标准：<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (以前被称为 Swagger) 和 <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>。
* **工具集** : 宗旨是不造轮子，尽可能多的集成、组装轮子，以及降低轮子的使用难度，集中精力把时间花在测试用例的设计上

<small>* 根据对某个构建线上应用的内部开发团队所进行的测试估算得出。</small>

## Git提交规范
```
feat 适用场景：全是新增功能，在旧功能基础上做改动（包含新增，删除）
fix 适用场景：修复bug，包含测试环境和生产环境
refactor 适用场景：重构任何功能，重构前和重构后输入和输出需要完全不变，如果有变化，在改动的部分请使用`feat`
test 适用场景：增加单元测试时
style 适用场景：修改代码格式，代码逻辑完全不变
docs 适用场景：编写注释或者使用文档
emoji	emoji代码	commit说明
🎨 (调色板)	:art:	改进代码结构/代码格式
⚡️ (闪电)	:zap:	提升性能
🐎 (赛马)	:racehorse:	提升性能
🔥 (火焰)	:fire:	移除代码或文件
🐛 (bug)	:bug:	修复 bug
🚑 (急救车)	:ambulance:	重要补丁
✨ (火花)	:sparkles:	引入新功能
📝 (铅笔)	:pencil:	撰写文档
🚀 (火箭)	:rocket:	部署功能
💄 (口红)	:lipstick:	更新 UI 和样式文件
🎉 (庆祝)	:tada:	初次提交
✅ (白色复选框)	:white_check_mark:	增加测试
🔒 (锁)	:lock:	修复安全问题
🍎 (苹果)	:apple:	修复 macOS 下的问题
🐧 (企鹅)	:penguin:	修复 Linux 下的问题
🏁 (旗帜)	:checked_flag:	修复 Windows 下的问题
🔖 (书签)	:bookmark:	发行/版本标签
🚨 (警车灯)	:rotating_light:	移除 linter 警告
🚧 (施工)	:construction:	工作进行中
💚 (绿心)	:green_heart:	修复 CI 构建问题
⬇️ (下降箭头)	:arrow_down:	降级依赖
⬆️ (上升箭头)	:arrow_up:	升级依赖
👷 (工人)	:construction_worker:	添加 CI 构建系统
📈 (上升趋势图)	:chart_with_upwards_trend:	添加分析或跟踪代码
🔨 (锤子)	:hammer:	重大重构
➖ (减号)	:heavy_minus_sign:	减少一个依赖
🐳 (鲸鱼)	:whale:	相关工作
➕ (加号)	:heavy_plus_sign:	增加一个依赖
🔧 (扳手)	:wrench:	修改配置文件
🌐 (地球)	:globe_with_meridians:	国际化与本地化
✏️ (铅笔)	:pencil2:	修复 typo
!!! note "note, seealso"
!!! summary "summary, tldr"
!!! info "info, todo"
!!! tip "tip, hint, important"
!!! success "success, check, done"
!!! question "question, help, faq"
!!! warning "warning, caution, attention"
!!! failure "failure, fail, missing"
!!! danger "danger, error"
!!! bug "bug"
!!! quote "quote, cite"
```
## 一、整个框架设计思路

依赖Python 3.7 及更高版本
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
protocoltest
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
```
def jobName = "jobName"
def maxNumber = 300
Jenkins.instance.getItemByFullName(jobName).builds.findAll {
  it.number <= maxNumber
}.each {
  it.delete()
}
```