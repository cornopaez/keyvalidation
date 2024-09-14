from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from  cryptography.exceptions import InvalidSignature

import hashlib

from .models import ValidationKey, Account, KeyGroup, ValidationKeyHistory
from django.db.models import Q, Prefetch
from django.core.exceptions import ValidationError

from .serializers import EnrichedValidationKeySerializer

import uuid
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length)).encode('ascii')

def generate_key_pairs(doc_item):
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    message = randomword(100)

    signature = key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(crypto_hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        crypto_hashes.SHA256()
    )

    hash_object = hashlib.sha512(private_key)
    private_key_hash = hash_object.hexdigest()

    doc_item['private_key'] = private_key.hex()
    doc_item['public_key'] = public_key.hex()
    doc_item['private_key_hash'] = private_key_hash
    doc_item['message'] = message.hex()
    doc_item['signature'] = signature.hex()

    return doc_item

def create_group_keys(key_group):
    final_docs = []
    doc_range = range(key_group.doc_num_start, key_group.doc_num_end + 1)

    init_docs = [{'document_number': x } for x in doc_range]

    for doc in init_docs:
        doc['account_id'] = key_group.account_id
        doc['group_id'] = key_group

    doc_with_keys = [generate_key_pairs(doc) for doc in init_docs]

    final_docs = [ValidationKey(private_key=doc['private_key'], private_key_hash=doc['private_key_hash'], public_key=doc['public_key'], message=doc['message'],signature=doc['signature'], account_id=doc['account_id'], group_id=doc['group_id'], document_number=doc['document_number']) for doc in doc_with_keys]

    return final_docs

def get_validation_key_data(serial_data):
    prefetch_key_group = Prefetch(
        'key_groups',
        queryset=(KeyGroup.objects.filter(
            exhausted__exact=False,
            doc_num_start__lte=serial_data['document_number'],
            doc_num_end__gte=serial_data['document_number'],
        )),
        to_attr='filtered_validation_key_groups'
    )

    prefetch_key = Prefetch(
        'validation_key_account',
        queryset=(ValidationKey.objects.filter(
            public_key=serial_data['public_key'],
            document_number=serial_data['document_number']
        )),
        to_attr='filtered_validation_key'
    )

    key_account_data = (Account.objects
        .prefetch_related(
            prefetch_key_group,
            prefetch_key
        )
        .get(
            number=serial_data['account']
        )
    )

    return key_account_data

def validate_public_key(account_data, rich_key_data, source):
    public_key = crypto_serialization.load_ssh_public_key(bytes.fromhex(rich_key_data['public_key']))
    signature = bytes.fromhex(rich_key_data['signature'])
    message = bytes.fromhex(rich_key_data['message'])
    res = False
    validation_key = account_data.filtered_validation_key[0]

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(crypto_hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            crypto_hashes.SHA256()
        )

        res = True
        validation_result = 's'
        validation_key.status = validation_result
        validation_key.save()
    except InvalidSignature as e:
        validation_result = 'f'
    finally:
        history_entry = ValidationKeyHistory(key_id=validation_key,validation_result=validation_result,source=source)
        try:
            history_entry.full_clean()
            history_entry.save()
        except Exception as e:
            print(e)
            pass
        return res