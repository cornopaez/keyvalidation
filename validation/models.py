from django.db import models
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

from .model_managers import ValidationKeyManager, KeyGroupManager

# Create your models here.

import uuid

class Account(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a given account and bank number, and source system.')
	number = models.BigIntegerField()
	bank = models.PositiveSmallIntegerField()
	source = models.CharField(max_length=3, help_text='The source system for this account.')

	class Meta:
		constraints = [
			UniqueConstraint(
					fields=['number', 'bank'],
					name='unique_account_for_source',
					violation_error_message='The account, bank, and source already exixts.',
				)
		]

	def __str__(self):
		"""String for representing the Model object."""
		return str(self.number)

class ValidationKey(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this private key.")
	private_key = models.CharField(max_length=3500, editable=False, help_text='The private key for a given account number.')
	private_key_hash = models.CharField(max_length=128, editable=False, help_text='The SHA512 has of the private key. This is used to enforce uniqueness in the database.')
	public_key = models.CharField(max_length=1000, editable=False, help_text='The public key for a given account number.')
	message = models.CharField(max_length=1000, null=False, blank=False, editable=False, help_text='A random string of chars to use for key validation.')
	signature = models.CharField(max_length=1000, null=False, blank=False, editable=False, help_text='The signature for the message using the private key.')
	account_id = models.ForeignKey('Account', related_name='validation_key_account', on_delete=models.PROTECT, null=False)
	group_id = models.ForeignKey('KeyGroup', related_name='validation_key_group', on_delete=models.PROTECT, null=False)
	document_number = models.PositiveSmallIntegerField(default=0)
	creation_dt = models.DateTimeField(auto_now_add=True)

	KEY_STATUS = (
		('a', 'Available'),
		('s', 'Spent'),
	)

	status = models.CharField(
		max_length=1,
		choices=KEY_STATUS,
		blank=False,
		default='a',
		help_text='The status of the validation key.'
	)

	objects = ValidationKeyManager()

	class Meta:
		constraints = [
			UniqueConstraint(
					fields=['private_key_hash'],
					name='private_key_hash_unique',
					violation_error_message='The private key hash already exixts.',
				),
			UniqueConstraint(
					fields = ('private_key_hash','account_id','document_number'),
					name = 'private_key_hash_acct_doc_num_unique',
					violation_error_message='This key hash is already tied to this account and document number.',
				)
		]

	def __str__(self):
		"""String for representing the Model object."""
		return str(self.id)

class KeyGroup(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this key group.")
	account_id = models.ForeignKey('Account', related_name='key_groups', on_delete=models.PROTECT, null=False)
	doc_num_start = models.IntegerField(default=0)
	doc_num_end = models.IntegerField(default=0)
	creation_dt = models.DateTimeField(auto_now_add=True)
	exhausted = models.BooleanField(default=False, blank=True, null=True)
	exhausted_date = models.DateTimeField(default=None, blank=True, null=True)

	objects = KeyGroupManager()

	def __str__(self):
		"""String for representing the Model object."""
		return str(self.id)

class ValidationKeyHistory(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this key validation history entry.")
	key_id = models.ForeignKey('ValidationKey', on_delete=models.PROTECT, null=False)

	VALIDATION_OPTS = (
		('s', 'Success'),
		('f', 'Failure'),
	)

	validation_result = models.CharField(
		max_length=1,
		choices=VALIDATION_OPTS,
		blank=False,
		null=False,
		help_text='The result of the key validation attempt.'
	)
	entry_dt = models.DateTimeField(auto_now_add=True)
	source = models.CharField(max_length=100, blank=False, null=False)

	def __str__(self):
		return str(self.id)