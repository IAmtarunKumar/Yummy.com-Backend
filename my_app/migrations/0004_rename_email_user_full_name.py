# Generated by Django 4.1.10 on 2023-09-02 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_rename_name_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='full_name',
        ),
    ]
