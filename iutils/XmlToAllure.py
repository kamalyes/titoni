# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： XmlToAllure.py
# Author : YuYanQing
# Desc: jmeter脚本运行的xml文件转Pytest脚本
# Date： 2021/8/23 15:09
'''
import json,uuid
from xml.etree import cElementTree

def checkChildren(xmlObject, checkString, num, result, demoFile, featureIndex, storyIndex,timeChekout):
    """
    :param xmlObject:  xml工程
    :param checkString: 这个其实是固定值 httpSample，只不过后面想要获取其他结构参数化
    :param num:
    :param result: 传递解析的xml
    :param demoFile: 生成的pytes文件
    :param featureIndex: 用来排序参数用例，按照jmeter中的树结果
    :param storyIndex: 同上，是第二层级的排序
    :param timeChekout: 用来替换allure报告中的时间为jmeter报告时间
    :return:
    """
    for children in xmlObject:
        try:
            if num == 1 and children.attrib['sby'] != "0":
                featureIndexStr='#'+str(featureIndex)+" " if featureIndex >= 10 else '#0'+str(featureIndex)+" "
                result["feature"] = featureIndexStr+children.attrib['lb']
                featureIndex += 1
                if num >= 2 and children.tag== "sample":
                    storyIndexStr= '#' + str(storyIndex) + " " if storyIndex >= 10 else '#0' + str(storyIndex) + " "
                    result["story"] = storyIndexStr+children.attrib['lb']
                    storyIndex += 1
        except:
            pass
        if children.tag== checkString:
            result['caseName'] = children.attrib['lb']
            for httpSampleChildren in children:
                if httpSampleChildren.tag== 'assertionResult':
                    assertionResultChildrenTag=[]
                    for assertionResultChildren in httpSampleChildren:
                        assertionResultChildrenTag.append(assertionResultChildren.tag)
                        result[assertionResultChildren.tag] = assertionResultChildren.text
                        if "failureMessage" not in assertionResultChildrenTag:
                            result['failureMessage'] = None
                else:
                    result[httpSampleChildren.tag] = httpSampleChildren.text
                    feature= result['feature'] if "feature" in result else None
                    caseName= result['caseName'] if 'caseName' in result else None
                    url= result['java.net.URL'] if 'java.net.URL' in result else None
                    method= result['method'] if 'method' in result else None
                    requestHeader= result['requestHeader'] if 'requestHeader' in result else None
                    queryString= result['queryString'] if 'queryString' in result else None
                    responseData= result['responseData'] if 'responseData' in result else None
                    failureMessage= result['failureMessage'] if 'failureMessage' in result else None
                    failure= result['failure'] if 'failure' in result else "false"
                    menthodUuid= str(uuid.uuid1()).replace('-','')
                    start= int(children.attrib['ts'])
                    stop= int(children.attrib['ts'])+int(children.attrib['t'])
                    timeChekout["test_demo#test_allure_report_"+menthodUuid]={"start":start,"stop":stop}
                    pyString= '''@allure.feature("{feature}")\n@allure.story("{feature}")\n@allure.title("{caseName}")
def test_allure_report_{num}():
    with allure.step("网络请求：%s"%(urlparse("{url}").path)):
        allure.attach(name="Request Url", body="{url}")
        allure.attach(name="Request Method", body="{method}")
        allure.attach(name="Request Headers", body='{requestHeader}')
        allure.attach(name="Query String Parametrize", body='{queryString}')
    with allure.step("响应结果：%s"%(urlparse("{url}").path)):
        allure.attach(name="Query String ResponseTime", body='{responseData}')
        allure.attach(name="Query String ResponseText", body='{reponseTime}s')
    with allure.step("基本参数效验：%s"%(urlparse("{url}").path)):
        allure.attach(name="Assert Parametrize", body='"{failureMessage}"')
    assert "{failure}" == "flase"
                        '''.format(feature=feature,
                                   caseName=caseName,num=menthodUuid,
                                   url=url,method=method, requestHeader=str(requestHeader).replace('\n', '')
                                   .replace('\r', ''),queryString=str(json.dumps(queryString)).replace("'","\""),
                                   responseData=str(json.dumps(responseData)).replace("'","\""),reponseTime=((stop-start)/1000),
                                   failureMessage=str(failureMessage).replace("'","\""),failure=failure)
            with open(demoFile,'a',encoding="utf-8") as c:
                c.write(pyString)
        else:
            checkChildren(children,checkString,num+1,result,demoFile,featureIndex,storyIndex,timeChekout)
    return timeChekout

if __name__ == '__main__':
    with open(r"test_demo.py", "w") as file:
        file.write('''# -*- coding:utf-8 -*-\nimport allure\nfrom urllib.parse import urlparse\n''')
    tree= cElementTree.parse(r"E:\WorkSpace\PycharmProjects\RvetInterfaceTest\debug\result.xml")
    realQueryTime= checkChildren(tree.getroot(),"httpSample",1,{},r"test_demo.py",1,1,{})