from django.contrib import admin

# Register your models here.

from  .models import Account, ValidationKey, KeyGroup, ValidationKeyHistory

class ValidationKeyHistoryInLine(admin.TabularInline):
	model = ValidationKeyHistory
	readonly_fields = ['id','key_id','validation_result','source','entry_dt']
	extra = 0

class AccountAdmin(admin.ModelAdmin):
	list_display=['source','number','bank']
	ordering = ('number',)

class KeyGroupAdmin(admin.ModelAdmin):
	list_display=('account_id','doc_num_start','doc_num_end','creation_dt','exhausted','exhausted_date')

class ValidationKeyAdmin(admin.ModelAdmin):
	list_display= ['id','account_id','group_id','document_number','status','creation_dt']
	ordering = ('account_id','group_id', 'document_number',)
	inlines = [ValidationKeyHistoryInLine]

class ValidationKeyHistoryAdmin(admin.ModelAdmin):
	list_display = ['key_id','validation_result','source','entry_dt']
	ordering = ['key_id','entry_dt']

admin.site.register(Account, AccountAdmin)
admin.site.register(ValidationKey, ValidationKeyAdmin)
admin.site.register(KeyGroup, KeyGroupAdmin)
admin.site.register(ValidationKeyHistory, ValidationKeyHistoryAdmin)