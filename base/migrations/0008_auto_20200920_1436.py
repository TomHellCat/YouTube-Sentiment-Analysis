# Generated by Django 3.0.7 on 2020-09-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20200920_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoinfo2',
            name='date',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
