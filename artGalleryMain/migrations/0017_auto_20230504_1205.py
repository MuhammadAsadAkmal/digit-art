# Generated by Django 3.2.18 on 2023-05-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artGalleryMain', '0016_auto_20230504_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='cart',
            name='deliveryDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='orderDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
