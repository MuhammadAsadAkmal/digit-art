# Generated by Django 3.2.18 on 2023-05-04 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artGalleryMain', '0017_auto_20230504_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='delivered_at',
        ),
    ]