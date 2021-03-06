# Generated by Django 2.1.7 on 2019-12-25 03:36

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(blank=True, null=True, verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, verbose_name='食物名称')),
                ('food_img', models.ImageField(blank=True, max_length=255, null=True, upload_to='food', verbose_name='菜品图片')),
                ('brief', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=2048, null=True, verbose_name='详情介绍')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='发布日期')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='食物原价')),
            ],
            options={
                'verbose_name': '食物详情',
                'verbose_name_plural': '食物详情',
                'db_table': 'dc_food',
            },
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(blank=True, null=True, verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '食物分类',
                'verbose_name_plural': '食物分类',
                'db_table': 'dc_food_category',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='food_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foods.FoodCategory', verbose_name='食物分类'),
        ),
    ]
