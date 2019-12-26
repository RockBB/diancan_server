# Generated by Django 2.1.7 on 2019-12-26 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(blank=True, null=True, verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('buy_number', models.CharField(max_length=128, null=True, verbose_name='账单号')),
                ('buy_type', models.SmallIntegerField(choices=[(0, '支付宝'), (1, '微信支付'), (2, '免费活动'), (3, '活动赠品'), (4, '系统赠送')], default=0, verbose_name='购买方式')),
                ('pay_time', models.DateTimeField(null=True, verbose_name='购买时间')),
                ('out_time', models.DateTimeField(null=True, verbose_name='过期时间')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='foods_users', to='foods.Food', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_cp', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '点菜记录',
                'verbose_name_plural': '点菜记录',
                'db_table': 'dc_user',
            },
        ),
    ]