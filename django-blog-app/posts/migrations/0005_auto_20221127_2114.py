# Generated by Django 3.2.16 on 2022-11-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_picture',
            field=models.ImageField(blank=True, default='kindpng_4517876.png', upload_to='cover_images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='kindpng_4517876.png', upload_to='Profile_images/'),
        ),
    ]