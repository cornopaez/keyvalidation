from .models import Account, ValidationKey, KeyGroup
from .objects import KeyCreationData, GenericAccountData
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('number','bank','source')

class KeyCreationRequestSerializer(serializers.Serializer):
	account = serializers.IntegerField()
	bank = serializers.IntegerField()
	source = serializers.CharField(max_length=3)
	doc_num_start = serializers.IntegerField()
	doc_num_end = serializers.IntegerField()

class GenericAccountFieldsSerializer(serializers.Serializer):
	account = serializers.IntegerField()
	bank = serializers.IntegerField()
	source = serializers.CharField(max_length=3)

class KeyGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = KeyGroup
		fields = ('doc_num_start','doc_num_end','creation_dt','exhausted','exhausted_date')

class AccountGroupSerializer(serializers.ModelSerializer):
	key_groups = KeyGroupSerializer(many=True, read_only=True)

	class Meta:
		model = Account
		fields = ('number','bank','source','key_groups')

class FilteredAccountGroupSerializer(serializers.ModelSerializer):
	key_groups = KeyGroupSerializer(source='filtered_key_groups', many=True, read_only=True)

	class Meta:
		model = Account
		fields = ('id','number','bank','source','key_groups')

class ValidationKeySerializer(serializers.ModelSerializer):
	class Meta:
		model = ValidationKey
		fields = ['id','public_key','account_id','group_id','document_number','creation_dt']