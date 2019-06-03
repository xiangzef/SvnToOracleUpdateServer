#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import os
import re

localtime = time.asctime( time.localtime(time.time()) )

my_sender = '13212778536@163.com'  # 发件人邮箱账号
my_pass = 'xiangzef1234'  # 发件人邮箱密码
my_user = '13212778536@163.com'  # 收件人邮箱账号，我这边发送给自己

d = '..\output\\'
class MailServer:
    def __init__(self,dir):
        if dir is '':
            self.d = d
        else:
            self.d = dir


    def mail(self):
        ret = True
        output = ''
        try:
            for root, dirs, files in os.walk(self.d):
                for file in files:
                    output = output + re.findall('FD201[0-9]*[A-Za-z]', file)[0]+'\\r'
                    if file.find('txt') > 0:
                        with open(d+file, 'r', encoding='utf-8') as f:
                            txt = f.read()
                        output = output + txt

            msg = MIMEText( output, 'plain', 'utf-8')
            msg['From'] = formataddr(["FromRobot", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["xiangzf22027", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "报错信息" + localtime  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print(output)
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    def Result(self, mail):
        ret = mail
        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")