# Generated by Django 2.1.7 on 2019-02-28 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_asyncemails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AsyncEmails',
            new_name='AsyncEmail',
        ),
    ]