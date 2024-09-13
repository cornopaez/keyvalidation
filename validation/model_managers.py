from django.db import models
from django.core.exceptions import ValidationError

class ValidationKeyManager(models.Manager):
    def create_validation_key(self, private_key, public_key, account_id, group_id, document_number):
        validation_key = (self
            .create(
                account_id=account_id, 
                group_id=group_id, 
                document_number=document_number,
                private_key=private_key,
                public_key=public_key,
            )
        )

        try:
            validation_key.full_clean()
            return validation_key
        except ValidationError as e:
            print(e)
            pass

class KeyGroupManager(models.Manager):
    def create_key_group(self, account_id, doc_num_start, doc_num_end):
        key_group = (self
            .create(
                account_id=account_id,
                doc_num_start=doc_num_start,
                doc_num_end=doc_num_end,
            )
        )

        try:
            key_group.full_clean()
            return key_group
        except ValidationError as e:
            print(e)
            pass