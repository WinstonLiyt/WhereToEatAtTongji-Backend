# Generated by Django 5.0.5 on 2024-05-10 01:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DishTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('location', models.CharField(max_length=32)),
                ('phone_number', models.CharField(max_length=11)),
                ('description', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RestImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='RestTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=100, unique=True, verbose_name='微信openid')),
                ('wx_nickname', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信昵称')),
                ('wx_avatar_url', models.URLField(blank=True, null=True, verbose_name='微信头像')),
                ('type', models.IntegerField(choices=[(1, '顾客'), (2, '商家'), (3, '管理员'), (4, '客服')], default=1, verbose_name='用户类型')),
                ('credits', models.IntegerField(default=0, verbose_name='经验值')),
                ('token', models.IntegerField(choices=[(1, '绿牌'), (2, '蓝牌'), (3, '黄牌')], default=1, verbose_name='牌子')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tags', models.ManyToManyField(to='tjeatwhatApp.dishtag')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='images',
            field=models.ManyToManyField(blank=True, to='tjeatwhatApp.restimage'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tags',
            field=models.ManyToManyField(to='tjeatwhatApp.resttag'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.user'),
        ),
        migrations.CreateModel(
            name='DishEval',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
                ('reply', models.CharField(max_length=200, null=True)),
                ('reply_time', models.DateTimeField(null=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.dish')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tjeatwhatApp.user')),
            ],
        ),
    ]
