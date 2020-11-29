from django.conf.urls import include, url
from movies import views
from order import views

urlpatterns = [
    url(r'^openvip/', views.OpenVip.as_view(), name="openvip"),  # 开通会员的路由
    url(r'commit/', views.OrderCommitView.as_view(), name="commit"),  # 创建订单的路由
    url(r'^pay/', views.OrderPayView.as_view(), name="pay"),  # 支付功能的路由
    url(r"^check/", views.CheckPayView.as_view(), name="check"),  # 查询支付交易结果
]
