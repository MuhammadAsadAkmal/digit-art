# Generated by Django 3.2.18 on 2023-05-04 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artGalleryMain', '0014_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_category',
            field=models.CharField(choices=[('PAINTING', 'Painting'), ('DEGITIAL_ART', 'Digital Art'), ('PHOTOGRAPHY', 'Photography'), ('SCULPTURE', 'Sculpture'), ('PRINTS', 'Prints'), ('DRAWING', 'Drawing')], default='PAINTING', max_length=100),
        ),
    ]