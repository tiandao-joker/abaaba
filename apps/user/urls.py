from user import views
from django.conf.urls import url

urlpatterns = [
    url(r"^login/", views.LoginView.as_view(), name="login"),  # 配置登录路由
    url(r'^register/', views.RegisterView.as_view(), name='register'),  # 配置注册的路由
    url(r'^active/(?P<token>.*)/', views.ActiveView.as_view(), name="active"),  # 用户激活
    url(r"^forgetpwd/", views.ForgetPwdView.as_view(), name="forgetpwd"),  # 忘记密码
    url(r'^updata/(?P<token>.*)/', views.UpdataPwdView.as_view(), name='updata'),  # 修改密码
    url(r"^updatasucc/", views.UpdataSuccView.as_view(), name='updatasucc'),  # 修改密码成功
    url(r'^logout/', views.LogoutView.as_view(), name="logout"),  # 退出登录
    url(r'^userinfo/(?P<page>.*)$', views.UserInfoView.as_view(), name="userinfo"),  # 用户中心浏览记录
    url(r'^uservip/', views.UserVipView.as_view(), name="uservip"),  # 用户中心我的会员
    url(r'^userown/', views.UserOwnView.as_view(), name="userown"),  # 用户中心个人信息
    url(r'^userorder/(?P<page>\d+)/', views.UserOrderInfoView.as_view(), name="userorder")  # 用户订单
]
