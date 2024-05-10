# Generated by Django 5.0.5 on 2024-05-10 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tjeatwhatApp', '0002_restaurant_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='tags',
        ),
        migrations.AlterField(
            model_name='resttag',
            name='name',
            field=models.CharField(choices=[(1, '面食'), (2, '甜点'), (3, '饮品'), (4, '早品'), (5, '水果'), (6, '烧烤'), (7, '西餐'), (8, '炒菜')], max_length=32, unique=True),
        ),
        migrations.DeleteModel(
            name='DishTag',
        ),
    ]