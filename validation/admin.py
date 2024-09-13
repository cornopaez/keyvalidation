from django.contrib import admin

# Register your models here.

from  .models import Account, ValidationKey, KeyGroup

class AccountAdmin(admin.ModelAdmin):
	list_display=['source','number','bank']
	ordering = ('number',)

class KeyGroupAdmin(admin.ModelAdmin):
	list_display=('account_id','doc_num_start','doc_num_end','creation_dt','exhausted','exhausted_date')

class ValidationKeyAdmin(admin.ModelAdmin):
	list_display= ['account_id','group_id','document_number','creation_dt']
	ordering = ('account_id','group_id', 'document_number',)

admin.site.register(Account, AccountAdmin)
admin.site.register(ValidationKey, ValidationKeyAdmin)
admin.site.register(KeyGroup, KeyGroupAdmin)