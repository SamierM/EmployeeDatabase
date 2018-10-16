# Generated by Django 2.0.6 on 2018-06-25 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employd', '0003_auto_20180622_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='first_name',
            new_name='fname',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='last_name',
            new_name='lname',
        ),
        migrations.RenameField(
            model_name='workrecord',
            old_name='contract',
            new_name='cont',
        ),
        migrations.RenameField(
            model_name='workrecord',
            old_name='employee',
            new_name='emp',
        ),
        migrations.RenameField(
            model_name='workrecord',
            old_name='project',
            new_name='proj',
        ),
        migrations.RenameField(
            model_name='workrecord',
            old_name='workTasking',
            new_name='task',
        ),
    ]