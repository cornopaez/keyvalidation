from django.shortcuts import render

# Create your views here.

from .models import Account, ValidationKey, KeyGroup
from rest_framework import generics
from .serializers import AccountSerializer, KeyCreationRequestSerializer, GenericAccountFieldsSerializer, AccountGroupSerializer, FilteredAccountGroupSerializer, KeyGroupSerializer, ValidationKeySerializer, GenericValidationKeySerializer, EnrichedValidationKeySerializer, FilteredAccountGroupKeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .group_utils import get_valid_groups
from .key_utils import create_group_keys, get_validation_key_data

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountAndKeyApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            "account": request.data.get('account'),
            "bank": request.data.get('bank'),
            "source": request.data.get('source'),
            "doc_num_start": request.data.get('doc_num_start'),
            "doc_num_end": request.data.get('doc_num_end'),
        }

        serializer = KeyCreationRequestSerializer(data=data)

        if serializer.is_valid():
            account = get_valid_groups(data)
            acct_group_data = FilteredAccountGroupSerializer(account).data

            if len(acct_group_data['key_groups']) < 1:

                # TODO: Change this so that the save op can be rolled back if things go wrong
                new_key_group = (KeyGroup.objects
                    .create_key_group(
                        account_id=account,
                        doc_num_start=data['doc_num_start'],
                        doc_num_end=data['doc_num_end'],
                    )
                )

                new_keys_objs = create_group_keys(new_key_group)

                keys = ValidationKey.objects.bulk_create(new_keys_objs)

                return Response(ValidationKeySerializer(keys, many=True).data)
            else:        
                res = {
                    'error': 'Unable to generate keys for this account. Either the account number is incorrect, it does not exist, or the document numbers are invalid.'
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KeyGroupApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            "account": request.data.get('account'),
            "bank": request.data.get('bank'),
            "source": request.data.get('source'),
        }

        serializer = GenericAccountFieldsSerializer(data=data)

        if serializer.is_valid():
            account = (Account.objects
                .filter(
                    number=request.data.get('account'),
                    bank=request.data.get('bank'),
                    source=request.data.get('source')
                )
            )

            return Response(AccountGroupSerializer(account, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidationKeyProcessing(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'account':request.data.get('account'),
            'public_key':request.data.get('public_key'),
            'document_number':request.data.get('document_number'),
        }

        serial_data = GenericValidationKeySerializer(data=data)

        if serial_data.is_valid():
            account_data = get_validation_key_data(serial_data.data)
            print(AccountSerializer(account_data).data)
            rich_key_data = FilteredAccountGroupKeySerializer(account_data)

            return Response(rich_key_data.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {
# "account":123456789,
# "bank":1,
# "source":"COR",
# "doc_num_start":1,
# "doc_num_end":20
# }

# {
#     "account":123456789,
#     "public_key": "b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDTnPvtNRe/z5Jz6PEehoi5rctLnNodwYOZcypKGEZosWLCTOaV4/MH53YRmxd9sfreuBtrBfGeU5JABiqDVCxhmNSJCc0Nd2I8iy0p+vvlaMrz7fRNLwYCypzaXf6mT/2tDXfx6Ii2+xBocXaFh7tYGpQlIs0bcZEemGacVwiMhvZyRQ+X5n+0d0cgIaj/61mAmFoOfpc0q1cWyGGfOOHP95UAPyELu4NON5m8Gh4ok+drbbCtUbYgXWM88M84k6/w0m2NYv9Pd/oF5LG7lEAa3xD7dQT7ppe7fm3TxpfPdZaXdbad1QIKHZZDo74/a8qGCeUsHPkX6ntOFSpWPfeh'",
#     "document_number": 1000
# }
