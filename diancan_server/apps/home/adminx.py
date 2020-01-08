import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "Ordering system"
    site_footer = "Cosmos Limited"
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSettings)

from .models import BannerInfo


class BannerInfoModelAdmin(object):
    list_display = ["name", "orders", "is_show"]


xadmin.site.register(BannerInfo, BannerInfoModelAdmin)

from .models import NavInfo


class NavInfoInfoModelAdmin(object):
    list_display = ["name", "link", "is_show"]


xadmin.site.register(NavInfo, NavInfoInfoModelAdmin)
