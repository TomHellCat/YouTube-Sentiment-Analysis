# Generated by Django 3.0.7 on 2020-08-11 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('search_term', models.CharField(default='', max_length=30)),
                ('total_views', models.IntegerField(default=0)),
                ('fav_titles', models.IntegerField(default=0)),
                ('unfav_titles', models.IntegerField(default=0)),
                ('likes_fav', models.IntegerField(default=0)),
                ('dislikes_fav', models.IntegerField(default=0)),
                ('likes_unfav', models.IntegerField(default=0)),
                ('dislikes_unfav', models.IntegerField(default=0)),
                ('total_favourability', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
