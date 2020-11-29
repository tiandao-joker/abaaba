from django.db import models
from db.base_model import BaseModel


# Create your models here.

class OrderInfo(BaseModel):
    """   订单模型类   """
    PAY_METHOD_CHOICES = (
        (1, "支付宝"),
        (2, "微信支付"),

    )
    PAY_METHODS = {
        1: "支付宝",
        2: "微信支付",
    }
    ORDER_STATUS = {
        1: "待支付",
        2: "已完成"
    }
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "已完成")
    )
    order_id = models.CharField(max_length=128, primary_key=True, verbose_name="订单ID")
    user = models.ForeignKey("user.User", verbose_name="用户")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    total_count = models.IntegerField(default=1, verbose_name="订购时长")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价")
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")
    trade_no = models.CharField(max_length=128, default='', verbose_name="支付编号")

    class Meta:
        db_table = "df_order_info"
        verbose_name = "订单"
        verbose_name_plural = verbose_name
