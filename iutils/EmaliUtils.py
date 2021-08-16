# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName：EmaliUtils.py
# Author : YuYanQing
# Desc:   邮件发送
# Date： 2020/5/6 19:27
'''
import smtplib
from email.header import Header
from iutils.LogUtils import Logger
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Email(object):
    def __init__(self,user_email=None,passwd=None,title=None,smtp_server=None,addressee=None)->str:
        '''
        :param self.user_email： 发件人邮箱
        :param self.passwd： 发件人密码
        :param title：标题
        :param smtp_server：邮箱服务器
        :param addressee：收件人邮箱
        '''
        self.logger = Logger.writeLog()  # 调用日志模块
        self.user_email = user_email
        self.passwd = passwd
        self.smtp_server = smtp_server
        self.title = title
        self.addressee = addressee

    @staticmethod
    def enclosure(email_data, file_path):
        '''
        附件发送
        :param file_path:附件的存储路径
        :return:
        '''
        enclosure_data = MIMEMultipart()
        enclosure_data.attach(email_data)
        # 读取文件二进制流
        with open(file_path, 'rb') as f:
            file_data = MIMEText(f.read(), 'base64', 'UTF-8')
        file_data['Content-Type'] = 'application/octet-stream'
        file_data['Content-Disposition'] = 'attachment; filename=%s' % file_path
        enclosure_data.attach(file_data)
        return enclosure_data

    @staticmethod
    def image(email_data, image_path):
        '''
        图片是嵌入在 HTML 中进行发送展示
        :param email_data: 图片地址
        :param image_path:
        :return:
        '''
        email_image = '''
            <div><img src='cid:image-index'></div>
        '''
        image_data = MIMEMultipart()
        email_data.attach(image_data)
        image_data.attach(MIMEText(email_image, 'html', 'UTF-8'))
        # 读取图片二进制流
        with open(image_path, 'rb') as f:
            image_data = MIMEImage(f.read())
        image_data.add_header('Content-ID', '<image-index>')
        email_data.attach(image_data)
        return email_data

    def send(self, subject, content, send_type='plain', file_path=None, image_path=None):
        '''
        邮件发送
        :param file_path: 附件路径
        :param image_path: 图片路径
        :param email_data:发送实体定义
        :param send_type 发送类型：enclosure-附件格式 image-图文格式
        :param email_data['Subject']  邮件主题
        :param email_data['From'] 邮件标题
        :param email_data['To'] 收件人
        :return:
        '''
        email_data = MIMEText(content, send_type, 'UTF-8')
        email_data['Subject'] = Header(subject, 'UTF-8')
        email_data['From'] = Header("%s<%s>" % (self.title, self.user_email), 'UTF-8')
        email_data['To'] = Header(';'.join(self.addressee), 'UTF-8')
        email_cursor = smtplib.SMTP_SSL(self.smtp_server, 465)
        # 发送附件
        if send_type == 'enclosure':
            email_data = self.enclosure(email_data, file_path)
        # 发送图片
        if send_type == 'image':
            email_data = MIMEMultipart()
            email_data = self.image(email_data, image_path)

        try:
            # 登录服务器
            email_cursor.login(self.user_email, self.passwd)
            # 发送邮件
            email_cursor.sendmail(self.user_email, self.addressee, email_data.as_string())
            # 开启 DEBUG
            # email_cursor.set_debuglevel(1)
        except Exception as e:
            self.logger.error('邮件发送失败-:', e)
        else:
            self.logger.info('邮件发送成功~！')
        finally:
            email_cursor.quit()
if __name__ == '__main__':
    Email = Email(user_email="mryu168@163.com",passwd="xxxx",title="test",smtp_server="smtp.163.com",addressee="mryu168@163.com")
    # 发送文本 send_type 参数需要指定为 plain，因为 plain 为默认参数所以可以忽略
    Email.send('测试邮件(标题)', '测试邮件(内容) - 文本')
    # 发送 html send_type 参数需要指定为 html
    Email.send('测试邮件(标题)', '<h2> 测试邮件(内容) - HTML </h2>', send_type='html')
    # 发送带有 [附件] 的格式：send_type 参数需要指定为 enclosure file_path 参数为文件路径
    Email.send('测试邮件(标题)', '测试邮件(内容) - 附件', send_type='enclosure', file_path='../result/Test.txt')
    # 发送带有 [图片] 的格式：
    # 发送图片 send_type 参数需要指定为 image
    # image_path 参数为图片路径
    Email.send('测试邮件(标题)', '测试邮件(内容) - 图片', send_type='image', image_path='../result/mbuntu-5.jpg')