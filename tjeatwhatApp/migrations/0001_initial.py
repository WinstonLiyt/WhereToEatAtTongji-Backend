# Generated by Django 5.0.4 on 2024-05-09 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('label', models.CharField(blank=True, max_length=50, null=True)),
                ('num_upvotes', models.IntegerField(default=0)),
                ('num_stars', models.IntegerField(default=0)),
                ('ip', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('avatar', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_post_comment', models.BooleanField(default=True)),
                ('ip', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('num_upvotes', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=2000)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.post')),
            ],
        ),
        migrations.CreateModel(
            name='UpvoteComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.users')),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.users')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tjeatwhatApp.users'),
        ),
    ]
