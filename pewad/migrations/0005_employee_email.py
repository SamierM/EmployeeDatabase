# Generated by Django 2.0.6 on 2018-06-27 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pewad', '0004_auto_20180625_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email'),
        ),
    ]
