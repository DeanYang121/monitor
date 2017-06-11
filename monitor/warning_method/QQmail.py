# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务  
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "958672189@qq.com"  # 用户名
mail_pass = "gchrysfjuuwpbdgf"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

sender = '958672189@qq.com'
receivers = ['deanyang1996@126.com','luxury199601@foxmail.com' ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('a test for python', 'plain', 'utf-8')
message['From'] = Header("deanyang", 'utf-8')
message['To'] = Header("hello_world", 'utf-8')

subject = 'my alert'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  #通过ssl建立安全链接
    smtpObj.login(mail_user, mail_pass)     #邮箱账号登录校验
    smtpObj.sendmail(sender, receivers, message.as_string())  #邮件发送
    smtpObj.quit()
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(e)