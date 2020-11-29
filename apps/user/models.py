from django.contrib.auth.models import AbstractUser
from django.db import models
from db.base_model import BaseModel


# Create your models here.

class User(AbstractUser, BaseModel):
    """   用户模型类  """

    class Meta:
        db_table = "df_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class UserInfo(BaseModel):
    user = models.ForeignKey("user.User", verbose_name="用户")
    name = models.CharField(max_length="50", default=None, verbose_name="昵称")
    head_portrait = models.ImageField(upload_to="head_portrait", default=None, verbose_name="头像")
    vip_time_end = models.DateTimeField(blank=True, null=True, default=None, verbose_name="到期时间")

    class Meta:
        db_table = "df_user_info"
        verbose_name = "用户"
        verbose_name_plural = verbose_name