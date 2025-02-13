# Generated by Django 5.1.1 on 2024-09-13 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("validation", "0010_rename_account_keygroup_account_id"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="validationkey",
            name="pv_key_acct_doc_num_unique",
        ),
        migrations.RenameField(
            model_name="validationkey",
            old_name="acct_uuid",
            new_name="account_id",
        ),
        migrations.AlterField(
            model_name="keygroup",
            name="account_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="key_groups",
                to="validation.account",
            ),
        ),
        migrations.AlterField(
            model_name="validationkey",
            name="private_key",
            field=models.CharField(
                editable=False,
                help_text="The private key for a given account number.",
                max_length=2000,
            ),
        ),
        migrations.AlterField(
            model_name="validationkey",
            name="public_key",
            field=models.CharField(
                editable=False,
                help_text="The public key for a given account number.",
                max_length=400,
            ),
        ),
        migrations.AddConstraint(
            model_name="validationkey",
            constraint=models.UniqueConstraint(
                fields=("private_key", "account_id", "document_number"),
                name="pv_key_acct_doc_num_unique",
                violation_error_message="This key is already tied to this account and document number.",
            ),
        ),
    ]
