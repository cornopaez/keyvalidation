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
	private_key = models.CharField(max_length=2000, editable=False, help_text='The private key for a given account number.')
	public_key = models.CharField(max_length=400, editable=False, help_text='The public key for a given account number.')
	account_id = models.ForeignKey('Account', on_delete=models.PROTECT, null=False)
	group_id = models.ForeignKey('KeyGroup', on_delete=models.PROTECT, null=False)
	document_number = models.PositiveSmallIntegerField(default=0)
	creation_dt = models.DateTimeField(auto_now_add=True)

	objects = ValidationKeyManager()

	class Meta:
		constraints = [
			UniqueConstraint(
					Lower('private_key'),
					name='private_key_unique',
					violation_error_message='The private key already exixts.',
				),
			UniqueConstraint(
					fields = ('private_key','account_id','document_number'),
					name = 'pv_key_acct_doc_num_unique',
					violation_error_message='This key is already tied to this account and document number.',
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

	# class Meta:
	# 	constraints = [
	# 		UniqueConstraint(
	# 				Lower(str('id')),
	# 				name='id_unique',
	# 				violation_error_message='The Key Group ID already exixts.',
	# 			)
	# 	]

	def __str__(self):
		"""String for representing the Model object."""
		return str(self.id)