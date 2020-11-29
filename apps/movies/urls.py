from django.conf.urls import include, url
from movies import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),  # 配置首页路由
    url(r"^test/", views.TestView.as_view(), name="test"),  # 测试用
    url(r'^comedy/(?P<subject>\d+)/(?P<page>\d+)/', views.ComedyView.as_view(), name="comedy"),  # 跳转电影分类详情
    url(r"^single/(?P<movie_id>\d+)/(?P<set_id>\d+)/", views.SingleView.as_view(), name="single"),  # 跳转到视频详情页
]
