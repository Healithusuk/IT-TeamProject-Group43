# Generated by Django 5.1.6 on 2025-03-15 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("allModels", "0026_alter_accounts_favorites_alter_accounts_follower_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounts",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
