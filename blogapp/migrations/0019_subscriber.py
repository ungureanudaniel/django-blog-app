# Generated by Django 3.1.9 on 2021-06-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0018_delete_newsletteruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('name', models.EmailField(max_length=200)),
                ('conf_num', models.CharField(max_length=15)),
                ('voucher_prize', models.CharField(max_length=10)),
                ('confirmed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
