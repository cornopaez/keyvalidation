from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from .models import ValidationKey

import uuid

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

    doc_item['private_key'] = private_key
    doc_item['public_key'] = public_key

    return doc_item

def create_group_keys(key_group):
    final_docs = []
    doc_range = range(key_group.doc_num_start, key_group.doc_num_end + 1)

    init_docs = [{'document_number': x } for x in doc_range]

    for doc in init_docs:
        doc['account_id'] = key_group.account_id
        doc['group_id'] = key_group

    doc_with_keys = [generate_key_pairs(doc) for doc in init_docs]

    final_docs = [ValidationKey(private_key=doc['private_key'], public_key=doc['public_key'], account_id=doc['account_id'], group_id=doc['group_id'], document_number=doc['document_number']) for doc in doc_with_keys]

    return final_docs