# Generated by Django 3.0.7 on 2020-07-02 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_auto_20200702_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Recipes', 'Recipes'), ('Lifestyle', 'Lifestyle'), ('Children', 'Children')], default='Recipes', max_length=20),
        ),
    ]
