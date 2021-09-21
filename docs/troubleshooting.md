# Troubleshooting

!!! bug "Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))"
    解决方案：
    
    1. 请检查你的服务器网络是否正常
    2. 请确定是否被视为攻击者，阻止了你的请求
    3. 请检查本地是否有开代理，或出站规则是否配置
    
!!! bug "File OkHttps.py, line 305, in sendApi if re.match(r'^https?:/{2}\w.+$', url): TypeError: expected string or bytes-like object"
    
    错误案例：>>> Httpx.sendApi(method="get")
    
    解决方案：调用sendApi时需传入合法的url

!!! bug "File "OkHttps.py", line 256, in sendApi method = method.lower() AttributeError: 'NoneType' object has no attribute 'lower'"
    
    错误案例1：>>> Httpx.sendApi(url=url)

    错误案例2：>>> Httpx.sendApi(method="错误Method请求",url="http://www.test.com")
    
    解决方案：调用sendApi时未传入合法method
    
!!! bug "File OkHttps.py, line 276, in sendApi raise Exception("该场景未配置、请调试后添加判断") Exception: 该场景未配置、请调试后添加判断"
    
    错误案例：>>> Httpx.sendApi(method="post",url="http://www.test.com")
    
    解决方案：调用sendApi时若method="post" 那么headers 里必须得添加content_type

!!! bug "header = header.encode('ascii') UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)"
    
    错误案例：>>> Httpx.sendApi(method="post",url="http://www.test.com",data={},headers={"中文的":"vars"})
    
    解决方案：headers中的key值不能为中文
    
!!! bug "values[i] = one_value.encode('latin-1') UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-2: ordinal not in range(256)"
    
    错误案例：>>> Httpx.sendApi(method="post",url="http://www.test.com",data={},headers={"vars":"中文的"})
    
    解决方案：headers中的value值不能为中文
    
!!! bug "TypeError: func() got an unexpected keyword argument 'xxxxx'"
    
    错误案例：>>> class.func(error_params={"test_key":"test_var"})
    
    解决方案：没有这个参数入口
    
!!! bug "raise TypeError("%s比较函数错误" % (func)) TypeError: numMatch比较函数错误"
    
    错误案例：
    
            >>> expected_variables = {"expected_variables":{'test_001': 500, "test002":["aaa",500]}}
            >>> assertEqual(expected_variables, variables= {'test_001': 500, "test002":[]})
    
    解决方案：修改效验方式
    
!!! bug "Arguments: (ZeroDivisionError('division by zero'),)"
    
    错误原因：没有有效的pytest测试函数或在单例中调用了函数
    
    解决方案：检查py文件中是否有Test命名的class及test_命名的测试函数且后面没有函数调用
    