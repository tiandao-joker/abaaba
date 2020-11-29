from user.models import User
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django_redis import get_redis_connection
from movies.models import MoviesType, MoviesSKU, Movies, IndexMoviesBanner, IndexTypeMoviesBanner, VipMovies, UserMoviesComment
from django.http import HttpResponse,JsonResponse
import json


# Create your views here.

class IndexView(View):
    def get(self, request):
        # 判断用户有没有登陆
        user = request.user
        user_info = None
        # 检验用户名是否存在
        if user.is_authenticated():
            user_info = User.objects.get(username=user)
        # 获取视频所有的种类
        types = MoviesType.objects.all()
        # 获取首页轮播图数据
        movies_banners = IndexMoviesBanner.objects.all().order_by("index")

        # 获取视频题材
        for type in types:
            subjects = IndexTypeMoviesBanner.objects.filter(type=type).order_by("index")
            # 动态的为type添加题材
            type.subjects = subjects

        # 获取首页视频数据
        top_movies = MoviesSKU.objects.filter(index="1").order_by("create_time")[:9]
        featured_movies = MoviesSKU.objects.filter(index="1").order_by("-count")[:12]
        rating_movies = MoviesSKU.objects.filter(index="1").order_by("-create_time")[:12]  # 评论量
        recrnt_movies = MoviesSKU.objects.filter(index="1").order_by("-create_time")[:12]

        content = {
            "user_info": user_info,
            "types": types,
            "movies_banners": movies_banners,
            "top_movies": top_movies,
            "featured_movies": featured_movies,
            "rating_movies": rating_movies,
            "recrnt_movies": recrnt_movies
        }
        return render(request, 'index.html', content)


class TestView(View):
    def get(self, request):
        # 测试获得视频
        # movies = MoviesSKU.objects.get(id=1)
        return render(request, "test.html")


class ComedyView(View):
    def get(self, request, subject, page):
        # 判断用户有没有登陆
        user = request.user
        user_info = None
        # 检验用户名是否存在
        if user.is_authenticated():
            user_info = User.objects.get(username=user)
        # 获取视频所有的种类
        types = MoviesType.objects.all()
        # 获取视频题材
        for ty in types:
            subjects = IndexTypeMoviesBanner.objects.filter(type=ty).order_by("index")
            # 动态的为type添加题材
            ty.subjects = subjects
        # 获取分类详情页
        subject = IndexTypeMoviesBanner.objects.filter(id=subject).first()
        # 获取分类相关的视频
        movies = MoviesSKU.objects.filter(type=subject.type, movies=subject.sku, index="1")

        paginator = Paginator(movies, 6)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        movie_page = paginator.page(page)
        return render(request, 'comedy.html',
                      {"user_info": user_info, 'types': types, "subject": subject, "movie_page": movie_page})


class SingleView(View):
    # 这里还缺少一个参数，用来确定具体的视频详情
    def get(self, request, movie_id, set_id):
        # 判断用户有没有登陆
        user = request.user
        user_info = None
        set_id_head = set_id
        movie = MoviesSKU.objects.get(id=movie_id)
        # 检验用户名是否存在
        if user.is_authenticated():
            user_info = User.objects.get(username=user)

            # 链接redis
            conn = get_redis_connection("default")  # default 使用的是settings中配置的default
            # 查询操作
            movie_key = 'movie_%s' % user.id  # 电影的key
            cart_count = conn.hlen(movie_key)

            history_key = "history_%s" % user.id  # 是redis中足迹的key

            # 删除足迹中有重复的
            conn.lrem(history_key, 0, movie.name)

            # 添加足迹功能
            conn.lpush(history_key, movie.name)  # 往链表的左边添加
            movie.count += 1
            movie.save()
            # 保留链表指定区间的数据,包含两边
            conn.ltrim(history_key, 0, -1)

        # 获取视频所有的种类
        types = MoviesType.objects.all()
        # 获取视频题材
        for ty in types:
            subjects = IndexTypeMoviesBanner.objects.filter(type=ty).order_by("index")
            # 动态的为type添加题材
            ty.subjects = subjects
        sets = MoviesSKU.objects.filter(name=movie.name)
        set_id = int(set_id) - 1
        movie = list(sets)[set_id]

        # 获取视频评论
        try:
            comments = UserMoviesComment.objects.filter(sku=movie_id).order_by("-create_time")
        except Exception as e:
            comments = []



        context = {
            "types": types,
            "movie": movie,
            "user_info": user_info,
            "sets": sets,
            "comments":comments,
            "movie_id":movie_id,
            "set_id":set_id_head
        }

        return render(request, "single.html", context)

    def post(self, request, movie_id, set_id):
        '''
        保存用户评论信息
        :param request:
        :param movie_id:
        :param set_id:
        :return:
        '''
        user = request.user
        user = User.objects.get(username=user)
        comment = request.POST.get("comment")
        user_comment = UserMoviesComment.objects.create(user_id_id=user.id, sku_id=movie_id, comment=comment)

        user_comment.save()
        # print(user_comment.comment)
        comments = []
        try:
            comments_all = UserMoviesComment.objects.all().order_by("-create_time")
            for comment in comments_all:
                username = User.objects.get(id=comment.user_id_id).username
                create_time_year = comment.create_time.strftime("%Y")
                create_time_month = comment.create_time.strftime("%m")
                create_time_day = comment.create_time.strftime("%d")
                create_time_hours = str(int(comment.create_time.strftime("%H")))
                create_time_minutes = comment.create_time.strftime("%M")
                create_time = create_time_year + "年" + create_time_month + "月" + create_time_day + "日" + " " + create_time_hours + ":" + create_time_minutes
                # print(type(comment.create_time))
                comments_dict = {
                    "comment_one":comment.comment,
                    "create_time":create_time,
                    "username":username
                }
                comments.append(comments_dict)
        except Exception as e:
            comments = []
        # print(comments)
        # return render(request, "single.html", {"comment":comments})
        return JsonResponse({"errno":1,"comments":comments})
        # return HttpResponse()
        # return redirect(reverse("movies:single", kwargs={"movie_id":movie_id, "set_id":set_id}))






























