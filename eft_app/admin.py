# eft_app/admin.py
from django.contrib import admin
from django.contrib import messages  # ADD THIS IMPORT
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import (
    Bank, Zone, Scheme, Supplier, DebitAccount,
    EFTBatch, EFTTransaction, ApprovalAuditLog
)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_groups', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('groups', 'is_staff', 'is_active', 'is_superuser')
    
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Roles'

# Unregister default User admin and register custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Bank Admin
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'swift_code', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('bank_name', 'swift_code')
    readonly_fields = ('created_by', 'created_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        # Allow superusers and System Admins
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_delete_permission(request, obj)

# Zone Admin
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('zone_code', 'zone_name', 'created_at')
    search_fields = ('zone_code', 'zone_name')
    readonly_fields = ('created_at',)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_delete_permission(request, obj)

# Scheme Admin
@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_code', 'scheme_name', 'zone', 'is_active', 'created_at')
    list_filter = ('is_active', 'zone')
    search_fields = ('scheme_code', 'scheme_name')
    readonly_fields = ('created_at',)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_delete_permission(request, obj)

# Supplier Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'supplier_name', 'bank', 'account_number', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'bank', 'created_at')
    search_fields = ('supplier_code', 'supplier_name', 'account_number')
    readonly_fields = ('created_by', 'created_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_delete_permission(request, obj)

# Debit Account Admin
@admin.register(DebitAccount)
class DebitAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('account_number', 'account_name')
    readonly_fields = ('created_at',)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='System Admin').exists():
            return True
        return super().has_delete_permission(request, obj)

# Inline for EFT Transactions
class EFTTransactionInline(admin.TabularInline):
    model = EFTTransaction
    extra = 0
    readonly_fields = ('sequence_number', 'zone', 'created_at')
    fields = ('sequence_number', 'debit_account', 'supplier', 'scheme', 'zone', 
              'amount', 'narration', 'reference_number', 'created_at')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# EFT Batch Admin
@admin.register(EFTBatch)
class EFTBatchAdmin(admin.ModelAdmin):
    list_display = ('batch_reference', 'batch_name', 'status', 'total_amount', 
                   'record_count', 'created_by', 'created_at', 'approved_by', 'approved_at')
    list_filter = ('status', 'created_at', 'approved_at')
    search_fields = ('batch_reference', 'batch_name', 'created_by__username')
    readonly_fields = ('batch_reference', 'total_amount', 'record_count', 'created_by', 
                      'created_at', 'approved_by', 'approved_at', 'rejection_reason',
                      'generated_file', 'generated_at')
    inlines = [EFTTransactionInline]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()
    
    def save_model(self, request, obj, form, change):
        # Prevent editing in admin
        if change:
            messages.error(request, 'EFT batches cannot be edited in admin. Use the web interface.')
            return
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()

# Approval Audit Log Admin
@admin.register(ApprovalAuditLog)
class ApprovalAuditLogAdmin(admin.ModelAdmin):
    list_display = ('batch', 'action', 'user', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('batch__batch_reference', 'user__username', 'remarks')
    readonly_fields = ('batch', 'action', 'user', 'timestamp', 'remarks', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()

# Custom Group Admin to show permissions
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_permissions_count')
    filter_horizontal = ('permissions',)
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permissions Count'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='System Admin').exists()

# Unregister default Group admin and register custom
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)