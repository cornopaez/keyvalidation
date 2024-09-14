from django.shortcuts import render

# Create your views here.

from .models import Account, ValidationKey, KeyGroup
from rest_framework import generics
from .serializers import AccountSerializer, KeyCreationRequestSerializer, GenericAccountFieldsSerializer, AccountGroupSerializer, FilteredAccountGroupSerializer, KeyGroupSerializer, ValidationKeySerializer, GenericValidationKeySerializer, EnrichedValidationKeySerializer, FilteredAccountGroupKeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .group_utils import get_valid_groups
from .key_utils import create_group_keys, get_validation_key_data, validate_public_key

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
            rich_key_data = FilteredAccountGroupKeySerializer(account_data)
            validation_res = validate_public_key(rich_key_data.data['validation_key'][0])
            if validation_res:
                res = {
                    'message': 'Validation success.'
                }
            else:
                res = {
                    'message': 'Validation failed.'
                }
            return Response(res)

        print(serial_data.errors)
        return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

# {
# "account":123456789,
# "bank":1,
# "source":"COR",
# "doc_num_start":1,
# "doc_num_end":20
# }


# {
#     "account":123456789,
#     "public_key": "7373682d727361204141414142334e7a61433179633245414141414441514142414141424151433935504e562f4d335a462f57304b7168636e486a614f71666b653366727664452b5a5261512b7a514974624a6e6170744268667a535632554e4c4e584d786d585970653039776964744d71734d324f6869664a38676f63697063597039716b4e3472595a3339316e6c42436f6769682b775551654e61423845506541717665555776586c4157744d626631564c564f734430344f514e59667847746a66615346372f555069704c6d7a6d546a714c42396b6f4f4471486e55496d6c7273644e4d44534d357a4b78594a6a4353733169794e63706d64535878456a7643686b7253416e62784b73755468396161524245664d6e2f74464a78624868414b5747744361356a3337676b554f6639612b645846664134337032383044476f545a2f4e62627435704b59316c6f7a664a505a61353473794c77795575772b74375a7564396267426a6331596947626c387671703367584d704e",
#     "document_number": 19
# }
