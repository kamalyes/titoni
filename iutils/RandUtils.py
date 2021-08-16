# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# File  : RandUtils.py
# Author: YuYanQing
# Desc  : 随机文本(id/姓名/邮箱/身份证/列表/浮点型/验证码)
# Date  : 2020/10/11 15:01
'''
import uuid
import random
import string
from random import choice
from iutils.LogUtils import Logger

class RandValue(object):
    def __init__(self):
        self.logger = Logger.writeLog()

    def getEmail(self,emailtype=None,maxnum=None,rad_count=None):
        """
        :param emailtype: 邮箱类型
        :param count:     所生成的数量
        :param maxnum:    邮箱地址最大长度
        :param temp:      临时存储生成的字符  temp_str转化list为str
        :return: email_list 最终输出的邮箱集合
        """
        temp = []
        count = 0
        email_list = []
        email_array = ['@126.com', '@163.com', '@sina.com', '@sohu.com', '@yahoo.com.cn', '@gmail.com', '@yahoo.com']
        if emailtype == None:
            emailtype = random.choice(email_array)
        if maxnum == None:
            maxnum = random.randint(6, 10)
        if rad_count == None:
            rad_count = 1
        while count<rad_count:
            for i in range(0, maxnum):
                status = random.randint(0, 1)
                if status == 0:
                    letters = string.ascii_letters
                    random_letter = random.choice(letters)
                    temp.append(random_letter)
                else:
                    random_num = random.randint(0, 1)
                    temp.append(str(random_num))
            temp_str = "".join(temp)
            # 每次转化后就丢弃temp、避免出现遍历追加['VJT000Ho@qq.com', 'VJT000Ho0110fm0w@qq.com'............]
            temp.clear()
            email_list.append(temp_str + emailtype)
            count +=1
        # self.logger.info("成功生成%s个，%s个前缀，且类型为%s邮箱地址%s"%(count,maxnum,emailtype,email_list))
        return email_list

    def getVerifi(self,maxnum,radcount):
        """
        随机生成6位的验证码
        :param maxnum:  最多可生成的长度
        :param radcount: 需要生成的数量
        :return: verifi_code 输出结果集
        """
        # 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
        # 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
        count = 0
        verifi_code = []
        while count < radcount:
            code_list = []
            for i in range(10):  # 0-9数字
                code_list.append(str(i))
            for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
                code_list.append(chr(i))
            for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
                code_list.append(chr(i))
            myslice = random.sample(code_list, maxnum)  # 从list中随机获取6个元素，作为一个片断返回
            verifi_code.append(''.join(myslice))  # list to string
            count += 1
        # self.logger.info("成功生成%s个%s位长度的字符：%s"%(radcount,maxnum,verifi_code))
        if radcount > 1:
            return verifi_code
        else:
            return verifi_code[0]

    def getPhone(self,radcount):
        """
        随机生成有效手机号码
        :param radcount: 需要生成的数量
        :return:
        """
        count = 0
        phone_num =[]
        while count < radcount:
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                        "153", "155", "156", "157", "158", "159", "186", "187", "188"]
            cell =random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
            phone_num.append(''.join(cell))  # list to string
            count +=1
        # self.logger.info("成功生成%s个手机号%s"%(radcount,phone_num))
        return phone_num

    def getName(self,radcount,length):
        """
        :param radcount: 随机产生多少个
        :param length:   名字长度
        :param surnames 姓氏
        :param fames    名
        :return: name_list 多个时采用list集合返回
        """
        count = 0
        name_list = []
        surnames = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛'\
               '奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康'\
               '伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵'\
               '席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗'\
               '丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫'\
               '乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄'\
               '印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂'\
               '濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘'\
               '匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相'\
               '查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳'\
               '淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空丌官司寇仉督子车颛孙端木'\
               '巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生'\
               '岳帅缑亢况郈有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福'
        fames = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清' \
                '飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善' \
                '厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家' \
                '致树炎德行时泰盛秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环' \
                '雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶' \
                '怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑筠柔竹霭凝晓欢霄枫芸菲寒欣滢伊亚宜可姬舒影荔枝思丽秀' \
                '飘育馥琦晶妍茜秋珊莎锦黛青倩婷宁蓓纨苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希'
        while count < radcount:
            sur = random.choice(surnames)
            name = "".join(random.choice(fames) for i in range(length))
            name_list.append(sur+name)
            count +=1
        # self.logger.info("成功生成%s个名字%s"%(radcount,name_list))
        return name_list

    def getStrList(self,length):
        '''生成给定长度的字符串，返回列表格式'''
        numbers = ''.join(map(str, [i for i in range(10) if i != 4]))  # 数字
        init_chars = ''.join(numbers)
        sample_list = random.sample(init_chars, length)
        # self.logger.info("成功生成数字列表：%s"%(sample_list))
        return sample_list

    def getStr(self,num_length):
        """
        从a-zA-Z0-9生成指定数量的随机字符
        :param num_length: 字符串长度
        :return:
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(num_length)]
        random_str = ''.join(str_list)
        return random_str

    def getNum(self,num_length):
        """
        从0-9生成指定数量的随机数字
        :param num_length: 字符串长度
        :return:
        """
        str_list = [random.choice(string.digits) for i in range(num_length)]
        random_str = ''.join(str_list)
        return random_str


    def getInt(self,data):
        """
        获取随机int数据
        :param data: 开始值,结束值 例如：1,5 输出：1
        :return:
        """
        try:
            start_num, end_num = data.split(",")
            start_num = int(start_num)
            end_num = int(end_num)
        except ValueError:
            raise AssertionError("调用随机整数失败%s" % data)
        if start_num <= end_num:
            num = random.randint(start_num, end_num)
        else:
            num = random.randint(end_num, start_num)
        # self.logger.info("成功生成随机整型数据：%s"%(num))
        return num

    def getFloat(self,data):
        """
        获取随机浮点数据
        :param data: 开始值,结束值,浮点数 例如：1,5,3 输出：1.123
        :return:
        """
        try:
            start_num, end_num, accuracy = data.split(",")
            start_num = int(start_num)
            end_num = int(end_num)
            accuracy = int(accuracy)
        except ValueError:
            raise AssertionError("调用随机整数失败，范围参数或精度有误！\n小数范围精度 %s" % data)
        if start_num <= end_num:
            num = random.uniform(start_num, end_num)
        else:
            num = random.uniform(end_num, start_num)
        num = round(num, accuracy)
        # self.logger.info("成功生成随机浮点数据：%s"%(num))
        return num

    def getUuid(self):
        """
        基于MAC地址+时间戳+随机数来生成GUID
        :param:
        :return:
        """
        str_uuid =  str(uuid.uuid1()).upper()
        # self.logger.info("成功生成随机uuid：%s"%(str_uuid))
        return str_uuid

    def getUserAgent(self):
        Mozilla = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.3589.115 Safari/537.36"
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Dalvik/2.1.0 (Linux; U; Android 10; SPN-AL00 Build/HUAWEISPN-AL00)",
            ]
        return choice(Mozilla)

RandValue = RandValue()

if __name__ == '__main__':
    print(RandValue.getEmail(emailtype="@qq.com", maxnum=10, rad_count=5))
    print(RandValue.getVerifi(maxnum=6, radcount=1))
    print(RandValue.getPhone(radcount=6))
    print(RandValue.getName(length=2, radcount=10))
    print(RandValue.getStrList(length=5))
    print(RandValue.getStr(256))
    print(RandValue.getInt("1,5"))
    print(RandValue.getFloat("1,5,6"))
    print(RandValue.getUuid())
    print(RandValue.getNum(255))
    print(str(RandValue.getStr(RandValue.getInt("1,22"))).title())
    print(RandValue.getFloat("1,100,10"))