# Generated by Django 5.1.1 on 2024-09-08 19:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("validation", "0002_alter_privatekey_private_key_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unique ID for a given account and bank number, and source system.",
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="privatekey",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unique ID for this private key.",
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="publickey",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unique ID for this public key.",
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
