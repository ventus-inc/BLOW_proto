from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# Create your models here.
class TokenBoardManager(models.Manager):
    def get_seller(self, master):
        obj = SellOrder.objects.filter(master=master)
        seller = obj.all()

    def get_buyer(self, master):
        obj = BuyOrder.objects.filter(master=master)
        buyer = obj.all()


class TokenBoard(models.Model):
    """売り買い板
    """
    master = models.ForeignKey(settings.AUTH_USER_MODEL, default=None)
    price_now = models.FloatField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    object = TokenBoardManager()

class Token(models.Model):
    """持っているtoken
    """
    ground_token_address = settings.GROUND_TOKEN_ADDRESS
    token_board = models.ForeignKey(
        TokenBoard, null=True, blank=True)  # 暫定的にblank=True
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, related_name='publisher')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              default=None, related_name='owner')
    bought_price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    latest_price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    lot = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    token_address = models.CharField(default=ground_token_address,
                                     max_length=255)


class Order(models.Model):
    # master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='origin')
    price = models.FloatField(
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0.0)])
    token_board = models.ForeignKey(TokenBoard, blank=True, null=True)
    lot = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        message = 'order_by:' + str(self.master) + \
                  '\n at:' + str(self.timestamp)
        return str(message)

    class Meta:
        ordering = ('price',)
        abstract = True


class BuyOrderManager(models.Manager):
    def get_summed_lot(self, master):
        buys = self.get_queryset().filter(master=master).order_by('-price')
        total_buys = []
        previous_price = None
        obj = BuyOrder()
        for i in buys:
            if not previous_price:
                obj = BuyOrder(
                    master=i.master,
                    buyer=i.buyer,
                    price=i.price,
                    lot=i.lot,
                )
            else:
                if not previous_price == i.price:
                    total_buys.append(obj)
                    obj = BuyOrder(
                        master=i.master,
                        buyer=i.buyer,
                        price=i.price,
                        lot=i.lot,
                    )
                else:
                    obj.lot += i.lot
            previous_price = i.price
        total_buys.append(obj)
        return total_buys

    def get_summed_list(self, master):
        buys = self.get_queryset().filter(master=master).order_by('-price')
        total_price = []
        total_lot = []
        previous_price = None
        price = 0
        lot = 0
        obj = BuyOrder()
        for i in buys:
            if not previous_price:
                price = i.price
                lot = i.lot
            else:
                if not previous_price == i.price:
                    total_price.append(price)
                    total_lot.append(lot)
                    price = i.price
                    lot = i.lot
                else:
                    lot += i.lot
                    obj.lot += i.lot
            previous_price = i.price
        total_price.append(price)
        total_lot.append(lot)
        return [total_price, total_lot]


class BuyOrder(Order):
    """注文
    """
    master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='origin_buy')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer')
    objects = BuyOrderManager()


class SellOrderManager(models.Manager):

    def get_summed_lot(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_sells = []
        previous_price = None
        obj = SellOrder()
        for i in sells:
            if not previous_price:
                obj = SellOrder(
                    master=i.master,
                    seller=i.seller,
                    price=i.price,
                    lot=i.lot,
                )
            else:
                if not previous_price == i.price:
                    total_sells.append(obj)
                    obj = SellOrder(
                        master=i.master,
                        seller=i.seller,
                        price=i.price,
                        lot=i.lot,
                    )
                else:
                    obj.lot += i.lot
            previous_price = i.price
        total_sells.append(obj)
        return total_sells

    def get_summed_list(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_price = []
        total_lot = []
        previous_price = None
        price = 0
        lot = 0
        obj = SellOrder()
        for i in sells:
            if not previous_price:
                price = i.price
                lot = i.lot
            else:
                if not previous_price == i.price:
                    total_price.append(price)
                    total_lot.append(lot)
                    price = i.price
                    lot = i.lot
                else:
                    lot += i.lot
                    obj.lot += i.lot
            previous_price = i.price
        total_price.append(price)
        total_lot.append(lot)
        return [total_price, total_lot]


class SellOrder(Order):
    """注文
    """
    master = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='origin_sell')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller')
    objects = SellOrderManager()


class OrderManager(models.Manager):
    def get_summed_lot(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_sells = []
        previous_price = None
        obj = SellOrder()
        for i in sells:
            if not previous_price:
                obj = SellOrder(
                    master=i.master,
                    seller=i.seller,
                    price=i.price,
                    lot=i.lot,
                )
            else:
                if not previous_price == i.price:
                    total_sells.append(obj)
                    obj = SellOrder(
                        master=i.master,
                        seller=i.seller,
                        price=i.price,
                        lot=i.lot,
                    )
                else:
                    obj.lot += i.lot
            previous_price = i.price
        total_sells.append(obj)
        return total_sells

    def get_summed_list(self, master):
        sells = self.get_queryset().filter(master=master).order_by('-price')
        total_price = []
        total_lot = []
        previous_price = None
        price = 0
        lot = 0
        for i in sells:
            if not previous_price:
                price = i.price
                lot = i.lot
            else:
                if not previous_price == i.price:
                    total_price.append(price)
                    total_lot.append(lot)
                    price = i.price
                    lot = i.lot
                else:
                    lot += i.lot
                    obj.lot += i.lot
            previous_price = i.price
        total_price.append(price)
        total_lot.append(lot)
        return [total_price, total_lot]
