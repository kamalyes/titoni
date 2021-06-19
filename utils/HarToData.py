# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： HarToData.py
# Author : YuYanQing
# Desc: Har数据包转换为Json或Yaml文件
# Date： 2021/6/11 15:01
'''
import io,os
import sys,yaml,json

class HarParser:
    def loadHarEntries(self,file_path):
        """
        加载har中entries信息
        :param file_path:
        :return:
        """
        with io.open(file_path, "r+", encoding="utf-8-sig") as f:
            try:
                content_json = json.loads(f.read())
                return content_json["log"]["entries"]
            except (KeyError, TypeError):
                self.logger.error("HAR file content error: {}".format(file_path))
                sys.exit(1)

    def readHarDatas(self,file_path):
        """
        读取Har文件并return dict类型的数据
        :param file_path 文件目录
        :return:
        """
        result = {}
        # 判断路径是否传空或是否存在
        if file_path is None or os.path.isfile(file_path) == False:
            raise "Please check whether the file path or file name exists"
        else:
            head, tail = os.path.split(file_path)
            name, suffix = os.path.splitext(tail)
            # 判断文件类型
            if suffix.lower() == ".har":
                result.update({"har_entries": self.loadHarEntries(file_path)})
            else:
                raise "The file type must be in .Har format"
        return result

    def checkSuffix(self,data):
        """
        检查是否为cgi服务还是html/woff2/css/js/png...资源
        :param data
        :param req_url_type url尾缀格式类型
        :param rule 过滤的类型
        :return:
        """
        url_type = str(data.get("request").get("url")).split(".")[-1].lower() # 取出尾缀并转换为小写格式
        rule = ["html",".woff2","font","crx", "htm", "jsp", "css", "mp4", "avi", "png", "jpg", "ico", "js"]
        if  url_type not in rule:
            return True
        else:
            print("暂时不支持%s格式"%(url_type))

    def setHarInfo(self,data):
        """
        获取request传参的所有信息、并清洗拿到所需的字段
        :param data
        :return:
        """
        result = {}
        # 获取头部信息
        request = data.get("request")
        url = request.get("url")
        method = request.get("method")
        httpVersion = request.get("httpVersion")
        headers = request.get("headers")
        result.update({"desc": "描述信息"})
        for i in range(len(headers)):
            if headers[i].get("name") == "accept":
                result.update({"accept": headers[i].get("value")})
            elif headers[i].get("name") == "user-agent":
                result.update({"user-agent": headers[i].get("value")})
            elif headers[i].get("name") == "content-type":
                result.update({"content-type": headers[i].get("value")})
            elif headers[i].get("name") == "referer":
                result.update({"referer": headers[i].get("value")})
            elif headers[i].get("name") == "accept-encoding":
                result.update({"accept-encoding": headers[i].get("value")})
            elif headers[i].get("name") == "accept-language":
                result.update({"accept-language": headers[i].get("value")})
        # 获取请求参数信息
        postData = request.get("postData", "post data is not exist")
        # 获取响应后的信息
        response = data.get("response")
        statusCode = response.get("statusCode")
        statusText = response.get("statusText")
        # cookies = response.get("cookies","${cookies}")
        content = response.get("content")
        result.update({"request":{"method":method,"url":url,"httpVersion":httpVersion,"cookies":"${cookies}"},
                       "postData":postData,
                       "relevance": {"rel_type":"关联数据-Json/FromData格式","rel_data":"关联的数据参数"},
                       "response":{"checkSuffix":"check_json","expected_code":statusCode,"expected_text":statusText,"expected_content":str(content).strip()}})
        return result

    def writeFile(self,data,file_path,method)->str:
        """
        写入文件
        :param data:
        :param method 方式 --->json、yaml
        :return:
        """
        outpath = "%s.%s" % (file_path.split(".")[0],method)
        if method == "json":
            with open(outpath,"w",encoding="utf-8") as file:
                file.write(json.dumps(data,indent=4))
        else:
            with open(outpath,"w",encoding="utf-8") as file:
                yaml.dump(data,file,default_flow_style=False, allow_unicode=True,indent=4)

    def run(self):
        """
        合并数据
        :return:
        """
        req_info = {}
        file_path = input("Please enter the path of the HAR file to escape:")
        method = input("Please enter the storage type you want to escape (JSON, YAML) :").lower()
        har_data = self.readHarDatas(file_path)
        har_entries = har_data.get("har_entries")
        for i in range(len(har_entries)):
            temp = self.setHarInfo(har_entries[i])
            if self.checkSuffix(temp) is True:
                module_name = temp.get("request").get("url").split("/")[-1].lower()
                req_info.update({module_name: temp})
                head,tail = os.path.split(file_path)
                self.writeFile(req_info,"%s\\%s.%s"%(head,tail.replace(".har",""),method),method)

if __name__ == '__main__':
    HarParser().run()