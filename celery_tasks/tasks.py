from celery import Celery  # 导入可以执行异步任务的包
from django.template import loader, RequestContext

from abaaba import settings
from django.core.mail import send_mail

# 下面这部分代码是centos上任务的处理者需要的环境初始化 而windows上在manage.py上已经初始化了 所以在将下面这部分代码上传至处理者环境中后注释掉
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abaaba.settings")
django.setup()

from django_redis import get_redis_connection

# 创建一个异步任务对象
# 第一个参数：表示任务所在目录
# 第二个参数：表示指定什么作为你的中间人，使用centos上redis的9号数据库作为中间人
app = Celery("celery_tasks.tasks", broker="redis://:111111@192.168.0.104:6379/4")
# 如果redis没有密码，请将下面的注释打开，修改ip，并且注释掉上面的代码
# app = Celery("celery_tasks.tasks", broker="redis://192.168.0.41:6379/4")

# 定义一个任务函数
@app.task  # 这样声明之后说明就会存在一个delay()方法
def send_regiser_active_email(email, user_name, token):
    # 邮件的主题
    subject = "欢迎您成为小破站的会员"
    # 邮件的内容
    message = "<h1>%s,欢迎您注册小破站会员，请单击下面链接进行激活账号：<br></h1> <a href='http://192.168.0.104/user/active/%s/'>http://192.168.0.104/user/active/%s/</a>" % (
        user_name, token, token)
    # 收件人
    recv = [email]
    send_mail(subject, message, settings.EMAIL_FROM, recv, html_message=message)


@app.task  # 这样声明之后说明就会存在一个delay()方法
def send_updata_pwd_email(email, user_name, token):
    # 邮件的主题
    subject = "小破站修改密码"
    # 邮件的内容
    message = "<h1>%s,尊敬的小破站会员，您好，请单击下面链接进行修改密码：<br></h1> <a href='http://192.168.0.104/user/updata/%s/'>http://192.168.0.104/user/updata/%s/</a>" % (
        user_name, token, token)
    # 收件人
    recv = [email]
    send_mail(subject, message, settings.EMAIL_FROM, recv, html_message=message)
