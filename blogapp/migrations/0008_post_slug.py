# Generated by Django 3.0.7 on 2021-06-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_about_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='default', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]