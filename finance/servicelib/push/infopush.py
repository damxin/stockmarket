# -*- coding:utf-8 -*-
'''
Created on 2019/12/28
@author: damxin
@group :
@contact: nfx080523@hotmail.com
@消息推送
'''

from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

# NMHBSCOQTRXPTRWH 登录密码输入以下授权密码
def mail():
    msg = MIMEText('这是一封测试邮件 by python3', 'plain', 'utf-8')
    msg['From'] = formataddr(["走心的狗", 'nifaxin27026676@126.com'])
    msg['To'] = formataddr(["Wayne", '27026676@qq.com'])
    server = smtplib.SMTP()
    server.connect("smtp.126.com")
    try:
        server.login("nifaxin27026676@126.com", "126nfx27026676")
    except:
        print("login failed")
    server.sendmail('nifaxin27026676@126.com', ['27026676@qq.com'], msg.as_string())
    server.quit()
