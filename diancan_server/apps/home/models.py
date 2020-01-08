from django.db import models
from diancan_server.utils.models import BaseModel


# Create your models here.
class BannerInfo(BaseModel):

    image = models.ImageField(upload_to='banner', verbose_name='Rotation Chart', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='Rotation Chart Name')
    note = models.CharField(max_length=150, verbose_name='Remarks Information')
    link = models.CharField(max_length=150, verbose_name='Advertisement address of broadcasting chart')

    class Meta:
        db_table = 'dc_banner'
        verbose_name = 'Rotation Chart'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NavInfo(BaseModel):
    """
    导航
    """
    NAV_POSITION = (
        (0, 'top'),
        (1, 'footer')
    )

    name = models.CharField(max_length=50, verbose_name='Navigation Bar Name')
    link = models.CharField(max_length=250, verbose_name='Navigation Bar Address')
    opt = models.SmallIntegerField(choices=NAV_POSITION, default=0, verbose_name='Position')

    class Meta:
        db_table = 'dc_nav'
        verbose_name = 'Navigation Bar'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
