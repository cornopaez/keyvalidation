from .models import Account, ValidationKey, KeyGroup
from .objects import KeyCreationData, GenericAccountData
from rest_framework import serializers

# Generic Serializers

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

class ValidationKeySerializer(serializers.ModelSerializer):
	class Meta:
		model = ValidationKey
		fields = ['id','public_key','document_number','creation_dt']

class EnrichedValidationKeySerializer(serializers.ModelSerializer):
	class Meta:
		model = ValidationKey
		fields = ['private_key','public_key','document_number','status','creation_dt']

class FilteredAccountGroupSerializer(serializers.ModelSerializer):
	key_groups = KeyGroupSerializer(source='filtered_key_groups', many=True, read_only=True)

	class Meta:
		model = Account
		fields = ('id','number','bank','source','key_groups')

class FilteredAccountGroupKeySerializer(serializers.ModelSerializer):
	key_group = KeyGroupSerializer(source='filtered_validation_key_groups', many=True, read_only=False)
	validation_key = EnrichedValidationKeySerializer(source='filtered_validation_key', many=True, read_only=False)

	class Meta:
		model = Account
		fields = ('number','bank','source','key_group','validation_key')

class GenericValidationKeySerializer(serializers.Serializer):
	account = serializers.IntegerField()
	public_key = serializers.CharField(max_length=400)
	document_number = serializers.IntegerField()
