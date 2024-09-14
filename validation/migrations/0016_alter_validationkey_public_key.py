# Generated by Django 5.1.1 on 2024-09-13 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("validation", "0015_alter_validationkey_public_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="validationkey",
            name="public_key",
            field=models.CharField(
                editable=False,
                help_text="The public key for a given account number.",
                max_length=450,
            ),
        ),
    ]
