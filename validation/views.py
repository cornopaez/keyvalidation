from django.shortcuts import render

# Create your views here.

from .models import Account, ValidationKey, KeyGroup
from rest_framework import generics
from .serializers import AccountSerializer, KeyCreationRequestSerializer, GenericAccountFieldsSerializer, AccountGroupSerializer, FilteredAccountGroupSerializer, KeyGroupSerializer, ValidationKeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .group_utils import get_valid_groups
from .key_utils import create_group_keys

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

# {
# "account":123456789,
# "bank":1,
# "source":"COR",
# "doc_num_start":1,
# "doc_num_end":20
# }