# Generated by Django 5.1.1 on 2024-09-11 00:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "validation",
            "0007_remove_publickey_acct_uuid_remove_publickey_group_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="keygroup",
            name="creation_dt",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="keygroup",
            name="doc_num_end",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="keygroup",
            name="doc_num_start",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="keygroup",
            name="exhausted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="keygroup",
            name="exhausted_date",
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name="validationkey",
            name="creation_dt",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
