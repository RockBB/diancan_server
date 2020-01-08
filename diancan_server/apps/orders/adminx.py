import xadmin

from .models import Order


class OrderModelAdmin(object):
    pass


xadmin.site.register(Order, OrderModelAdmin)

from .models import OrderDetail


class OrderDetailModelAdmin(object):
    pass


xadmin.site.register(OrderDetail, OrderDetailModelAdmin)
