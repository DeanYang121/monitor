#encoding: utf-8
import smtplib
from email.mime.text import MIMEText

#发送给谁
mail_to = ["958672189@qq.com"]
#设置服务器，用户名，口令以及邮箱后缀
mail_host = "smtp.126.com"
mail_user = "deanyang1996"
mail_pass = "yy631562"
mail_postfix = "126.com"
# subject = "测试 第一份"
# mail_msg = """
# <p>Python 邮件发送测试...</p>
# <p><a href="http://119.29.101.170">这是一个链接</a></p>
# """

def send_126_mail(sub,content,mail_to=["958672189@qq.com"]):
    """
    send_126_mail("deanyang1996@126.com","sub","content")
    mail_to:发送给谁 
    sub: 主题
    content:内容 
    """
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    # msg = MIMEText(content,'html',"utf-8")
    msg = MIMEText(content)
    msg["subject"] = sub
    msg["From"] = me
    msg["To"] = ";".join(mail_to)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,mail_to,msg.as_string())
        s.close()
        print(content)
    except BaseException as e:
        print(str(e))

if __name__=="__main__":
    if send_126_mail(mail_to,"subject","mail_msg"):
        print("发送成功")
    else:
        print("发送失败")



