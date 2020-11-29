from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
from tinymce.models import HTMLField


# Create your models here.


class MoviesType(BaseModel):
    """   定义视频的模型类  """
    name = models.CharField(max_length=20, verbose_name="类别名称")  # 填写视频的类型  电影、电视剧、动漫、沙雕视频等类型
    logo = models.CharField(max_length=20, verbose_name="标识")  # 填写类型标识  movies tvs animations shadiao等标识

    class Meta:
        db_table = 'df_movies_type'
        verbose_name = "视频类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movies(BaseModel):
    """   定义视频SPU模型类   """
    name = models.CharField(max_length=20, verbose_name="视频SPU名称")
    # 富文本类型：带有格式的文本类型
    detail = HTMLField(blank=True, verbose_name="视频类型描述")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "df_movies"
        verbose_name = "视频SPU"
        verbose_name_plural = verbose_name


class MoviesSKU(BaseModel):
    """  电影SKU模型类  """
    status_choices = (
        (0, "会员"),
        (1, "非会员")
    )
    type = models.ForeignKey("MoviesType", verbose_name="视频类型")
    movies = models.ForeignKey("Movies", verbose_name="视频SPU")
    name = models.CharField(max_length=30, verbose_name="视频名称")
    desc = models.CharField(max_length=256, verbose_name="视频简介")
    cover_image = models.ImageField(upload_to="movies", verbose_name="视频封面")
    movie_file = models.FileField(upload_to="videos/", blank=True, default='', verbose_name="视频")
    index = models.SmallIntegerField(default=1, verbose_name="视频集数")
    count = models.IntegerField(default=0, verbose_name="播放量")
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name="视频状态")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "df_movies_sku"
        verbose_name = "视频"
        verbose_name_plural = verbose_name


class IndexMoviesBanner(BaseModel):
    """   首页轮播商品展示模型类   """
    sku = models.ForeignKey("MoviesSKU", verbose_name="视频")
    image = models.ImageField(upload_to="banner", verbose_name="图片")
    index = models.SmallIntegerField(default=0, verbose_name="展示顺序")

    def __str__(self):
        return self.sku.name

    class Meta:
        db_table = "df_index_banner"
        verbose_name = "首页轮播图视频"
        verbose_name_plural = verbose_name


class IndexTypeMoviesBanner(BaseModel):
    """   首页分类视频展示模型类   """
    type = models.ForeignKey("MoviesType", verbose_name="视频类型")
    sku = models.ForeignKey("Movies", verbose_name="视频分类")

    index = models.SmallIntegerField(default=0, verbose_name="显示顺序")

    def __str__(self):
        return self.type.name + "---" + self.sku.name

    class Meta:
        db_table = "df_index_type_goods"
        verbose_name = "主页分类展示视频"
        verbose_name_plural = verbose_name


class UserMoviesComment(BaseModel):
    user_id = models.ForeignKey("user.User", verbose_name="用户名")
    sku = models.ForeignKey("MoviesSKU", verbose_name="视频")
    comment = HTMLField(blank=True, verbose_name="视频评论")

    def __str__(self):
        return self.user_id + "---" + self.sku.name + "---" + self.comment

    class Meta:
        db_table = "df_user_comment"
        verbose_name = "视频评论信息"
        verbose_name_plural = verbose_name


class VipMovies(BaseModel):
    movie_file = models.FileField(upload_to="vipvideos/", blank=True, default='', verbose_name="广告视频")

    class Meta:
        db_table = "df_vip_movies"
        verbose_name = "vip广告视频"
        verbose_name_plural = verbose_name
