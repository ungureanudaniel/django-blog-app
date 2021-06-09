# Generated by Django 3.0.7 on 2021-06-05 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0006_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.CharField(max_length=600)),
                ('image', models.FileField(blank=True, upload_to='blog_image')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogapp.Post')),
                ('user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
