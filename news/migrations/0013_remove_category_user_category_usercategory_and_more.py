# Generated by Django 4.1.1 on 2022-11-02 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0012_rename_category_user_category_user_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user_category',
        ),

    ]
