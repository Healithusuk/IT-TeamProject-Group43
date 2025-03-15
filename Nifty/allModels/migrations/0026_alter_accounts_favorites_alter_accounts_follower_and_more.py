# Generated by Django 5.1.6 on 2025-03-14 03:43

import allModels.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("allModels", "0025_accounts_follower_accounts_following"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounts",
            name="favorites",
            field=models.JSONField(
                blank=True, default=allModels.models.default_favorites
            ),
        ),
        migrations.AlterField(
            model_name="accounts",
            name="follower",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="accounts",
            name="following",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
