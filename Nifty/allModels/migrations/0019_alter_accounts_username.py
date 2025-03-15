# Generated by Django 5.1.6 on 2025-03-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("allModels", "0018_alter_accounts_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounts",
            name="username",
            field=models.CharField(
                help_text="Required. 21 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=21,
                unique=True,
            ),
        ),
    ]
