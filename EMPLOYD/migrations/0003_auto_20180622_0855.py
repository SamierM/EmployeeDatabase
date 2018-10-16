# Generated by Django 2.0.6 on 2018-06-22 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employd', '0002_auto_20180621_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='lead',
        ),
        migrations.AddField(
            model_name='workrecord',
            name='lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Lead', to='employd.Employee', verbose_name='Lead'),
        ),
    ]
