# Generated by Django 5.1.1 on 2024-09-13 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("validation", "0019_alter_validationkey_message_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="validationkey",
            name="message",
            field=models.CharField(
                editable=False,
                help_text="A random string of chars to use for key validation.",
                max_length=1000,
            ),
        ),
        migrations.AlterField(
            model_name="validationkey",
            name="signature",
            field=models.CharField(
                editable=False,
                help_text="The signature for the message using the private key.",
                max_length=1000,
            ),
        ),
    ]
