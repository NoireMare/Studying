# Generated by Django 4.1.1 on 2022-10-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_rename_rating_author_author_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_add',
            field=models.DateField(auto_now_add=True),
        ),
    ]
