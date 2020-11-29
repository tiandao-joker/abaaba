from datetime import datetime
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from movies.models import MoviesType
from order.models import OrderInfo
from alipay import AliPay
from user.models import UserInfo


# Create your views here.

class OpenVip(View):
    """  开通会员  """

    def get(self, request):
        # 获取视频所有的种类
        types = MoviesType.objects.all()
        content = {
            "types": types,
        }
        return render(request, 'open_vip.html', content)


class OrderCommitView(View):
    def post(self, request):
        """  创建订单页面  """
        # 获取登录的用户
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"res": 1, "errmsg": "用户未登录"})

        # 接收参数：
        order_time = request.POST.get("order_time")
        order_money = request.POST.get("order_money")
        order_money = int(re.findall(r"\d+", order_money)[0])
        pay_method = request.POST.get("pay_method")
        # 校验参数
        if not all([order_money, order_time, pay_method]):
            return JsonResponse({"res": 1, "errmsg": "参数不完整"})

        # 判断开通时长
        # 判断开通时长
        if order_time == "1年":
            order_time = 365
        elif order_time == "6个月":
            order_time = 180
        elif order_time == "3个月":
            order_time = 90
        elif order_time == "1个月":
            order_time = 30
        elif order_time == "5天":
            order_time = 5
        pay_method = int(pay_method)
        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({"res": 1, "errmsg": "非法的支付方式"})

        # todo: 创建订单核心业务
        # 生成订单id
        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)
        order = OrderInfo.objects.create(
            order_id=order_id,  # 订单id
            user=user,  # 用户id
            pay_method=pay_method,
            total_count=order_time,  # 会员时间
            total_price=order_money,  # 钱
        )

        # todo: 向订单信息表中添加一条记录

        # 保存开通视频的时间和总价格
        return JsonResponse({"res": 0, "errmsg": "创建成功"})


class OrderPayView(View):
    """   获取订单支付结果  """

    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({"res": 1, "errmsg": "用户未登录，请先登录"})

        # 接收参数
        order_id = request.POST.get("order_id")
        # 校验参数
        if not order_id:
            return JsonResponse({"res": 1, "errmsg": "无效的订单id"})

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, pay_method=1, order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({"res": 1, "errmsg": "订单错误"})


        # 业务处理：使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPay(
            appid="2016102700768726",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open("apps/order/app_private_key.pem").read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open("apps/order/alipay_public_key.pem").read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_price),
            subject="阿巴阿巴%s" % order_id,  # 订单描述信息
            return_url="http://192.168.0.104/user/userorder/1/",
            notify_url=None
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        return JsonResponse({"res": 0, "errmsg": "OK", "pay_url": pay_url})


# /order/check/
class CheckPayView(View):
    """    查看订单支付结果   """

    def post(self, request):
        user = request.user

        if not user.is_authenticated():
            return JsonResponse({"res": 1, "errmsg": "用户未登录，请先登录"})

        ordertime = request.POST.get("order_count")

        # 判断开通时长
        if ordertime == "1年":
            ordertime = 365
        elif ordertime == "6个月":
            ordertime = 180
        elif ordertime == "3个月":
            order_time = 90
        elif ordertime == "1个月":
            ordertime = 30
        elif ordertime == "5天":
            ordertime = 5

        # 接收参数
        order_id = request.POST.get("order_id")
        # 校验参数
        if not order_id:
            return JsonResponse({"res": 1, "errmsg": "无效的订单id"})

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, pay_method=1, order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({"res": 1, "errmsg": "订单错误"})

        # 查询用户信息
        try:
            user_info = UserInfo.objects.get(user_id=user.id)
        except UserInfo.DoesNotExist:
            return JsonResponse({"res":1,"errmsg":"用户错误"})
        # 并为会员设置到期时间
        import datetime
        delta = datetime.timedelta(days=int(ordertime))
        print(delta)
        vip_time_end = user_info.vip_time_end
        create_time = order.create_time

        if user.is_staff:
            vip_time_end = vip_time_end + delta
            print(vip_time_end)
        else:
            vip_time_end = datetime.datetime.now() + delta
            print(vip_time_end)

        # 业务处理：使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPay(
            appid="2016102700768726",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open("apps/order/app_private_key.pem").read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open("apps/order/alipay_public_key.pem").read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        while True:
            response = alipay.api_alipay_trade_query(order_id)

            # 其返回值
            """response = {
                "alipay_trade_query_response": {
                    "trade_no": "2017032121001004070200176844",
                    "code": "10000",
                    "invoice_amount": "20.00",
                    "open_id": "20880072506750308812798160715407",
                    "fund_bill_list": [
                        {
                            "amount": "20.00",
                            "fund_channel": "ALIPAYACCOUNT"
                        }
                    ],
                    "buyer_logon_id": "csq***@sandbox.com",
                    "send_pay_date": "2017-03-21 13:29:17",
                    "receipt_amount": "20.00",
                    "out_trade_no": "out_trade_no15",
                    "buyer_pay_amount": "20.00",
                    "buyer_user_id": "2088102169481075",
                    "msg": "Success",
                    "point_amount": "0.00",
                    "trade_status": "TRADE_SUCCESS",
                    "total_amount": "20.00"
                },
                "sign": ""
            }
            """
            code = response.get("code")
            if code == "10000" and response.get("trade_status") == "TRADE_SUCCESS":
                # 支付成功
                trade_no = response.get("trade_no")
                order.trade_no = trade_no
                # 判断用户是否为会员,
                user_info.vip_time_end = vip_time_end
                user.is_staff = 1
                order.order_status = 2
                order.total_count = ordertime
                order.save()
                user_info.save()
                user.save()
                return JsonResponse({"res": 0, "errmsg": "支付成功"})
            elif code == "40004" or response.get("trade_status") == "WAIT_BUYER_PAY":
                # 等待付款
                import time
                time.sleep(5)
                continue
            else:
                # 支付错误
                return JsonResponse({"res": 1, "errmsg": "支付失败"})
