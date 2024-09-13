# Generated by Django 5.1.1 on 2024-09-10 19:51

import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "validation",
            "0006_privatekey_document_number_publickey_document_number_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="publickey",
            name="acct_uuid",
        ),
        migrations.RemoveField(
            model_name="publickey",
            name="group_id",
        ),
        migrations.CreateModel(
            name="ValidationKey",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unique ID for this private key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "private_key",
                    models.CharField(
                        editable=False,
                        help_text="The private key for a given account number.",
                        max_length=1000,
                    ),
                ),
                (
                    "public_key",
                    models.CharField(
                        editable=False,
                        help_text="The public key for a given account number.",
                        max_length=1000,
                    ),
                ),
                ("document_number", models.PositiveSmallIntegerField(default=0)),
                (
                    "acct_uuid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="validation.account",
                    ),
                ),
                (
                    "group_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="validation.keygroup",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PrivateKey",
        ),
        migrations.DeleteModel(
            name="PublicKey",
        ),
        migrations.AddConstraint(
            model_name="validationkey",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("private_key"),
                name="private_key_unique",
                violation_error_message="The private key already exixts.",
            ),
        ),
        migrations.AddConstraint(
            model_name="validationkey",
            constraint=models.UniqueConstraint(
                fields=("private_key", "acct_uuid", "document_number"),
                name="pv_key_acct_doc_num_unique",
                violation_error_message="This key is already tied to this account and document number.",
            ),
        ),
    ]
