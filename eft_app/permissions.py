# eft_app/permissions.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def create_groups_and_permissions():
    """Create user roles and assign permissions"""
    
    print("Setting up user groups and permissions...")
    
    # Get content types
    try:
        from .models import (
            Bank, Zone, Scheme, Supplier, DebitAccount, 
            EFTBatch, EFTTransaction
        )
        
        bank_ct = ContentType.objects.get_for_model(Bank)
        zone_ct = ContentType.objects.get_for_model(Zone)
        scheme_ct = ContentType.objects.get_for_model(Scheme)
        supplier_ct = ContentType.objects.get_for_model(Supplier)
        debitaccount_ct = ContentType.objects.get_for_model(DebitAccount)
        eftbatch_ct = ContentType.objects.get_for_model(EFTBatch)
        efttransaction_ct = ContentType.objects.get_for_model(EFTTransaction)
    except Exception as e:
        print(f"Error getting content types: {e}")
        return
    
    # Get or create custom permissions only
    can_approve_eft, created = Permission.objects.get_or_create(
        codename='can_approve_eft',
        defaults={
            'name': 'Can approve EFT batches',
            'content_type': eftbatch_ct
        }
    )
    if created:
        print("✓ Created permission: can_approve_eft")
    
    can_export_eft, created = Permission.objects.get_or_create(
        codename='can_export_eft',
        defaults={
            'name': 'Can export EFT files',
            'content_type': eftbatch_ct
        }
    )
    if created:
        print("✓ Created permission: can_export_eft")
    
    # Get existing Django default permissions (created automatically)
    try:
        permissions_map = {
            # Bank permissions (use .get() instead of .get_or_create())
            'add_bank': Permission.objects.get(codename='add_bank', content_type=bank_ct),
            'change_bank': Permission.objects.get(codename='change_bank', content_type=bank_ct),
            'delete_bank': Permission.objects.get(codename='delete_bank', content_type=bank_ct),
            'view_bank': Permission.objects.get(codename='view_bank', content_type=bank_ct),
            
            # Zone permissions
            'add_zone': Permission.objects.get(codename='add_zone', content_type=zone_ct),
            'change_zone': Permission.objects.get(codename='change_zone', content_type=zone_ct),
            'delete_zone': Permission.objects.get(codename='delete_zone', content_type=zone_ct),
            'view_zone': Permission.objects.get(codename='view_zone', content_type=zone_ct),
            
            # Scheme permissions
            'add_scheme': Permission.objects.get(codename='add_scheme', content_type=scheme_ct),
            'change_scheme': Permission.objects.get(codename='change_scheme', content_type=scheme_ct),
            'delete_scheme': Permission.objects.get(codename='delete_scheme', content_type=scheme_ct),
            'view_scheme': Permission.objects.get(codename='view_scheme', content_type=scheme_ct),
            
            # Supplier permissions
            'add_supplier': Permission.objects.get(codename='add_supplier', content_type=supplier_ct),
            'change_supplier': Permission.objects.get(codename='change_supplier', content_type=supplier_ct),
            'delete_supplier': Permission.objects.get(codename='delete_supplier', content_type=supplier_ct),
            'view_supplier': Permission.objects.get(codename='view_supplier', content_type=supplier_ct),
            
            # Debit Account permissions
            'add_debitaccount': Permission.objects.get(codename='add_debitaccount', content_type=debitaccount_ct),
            'change_debitaccount': Permission.objects.get(codename='change_debitaccount', content_type=debitaccount_ct),
            'delete_debitaccount': Permission.objects.get(codename='delete_debitaccount', content_type=debitaccount_ct),
            'view_debitaccount': Permission.objects.get(codename='view_debitaccount', content_type=debitaccount_ct),
            
            # EFT Batch permissions
            'add_eftbatch': Permission.objects.get(codename='add_eftbatch', content_type=eftbatch_ct),
            'change_eftbatch': Permission.objects.get(codename='change_eftbatch', content_type=eftbatch_ct),
            'view_eftbatch': Permission.objects.get(codename='view_eftbatch', content_type=eftbatch_ct),
            
            # EFT Transaction permissions
            'add_efttransaction': Permission.objects.get(codename='add_efttransaction', content_type=efttransaction_ct),
            'change_efttransaction': Permission.objects.get(codename='change_efttransaction', content_type=efttransaction_ct),
            'delete_efttransaction': Permission.objects.get(codename='delete_efttransaction', content_type=efttransaction_ct),
            'view_efttransaction': Permission.objects.get(codename='view_efttransaction', content_type=efttransaction_ct),
            
            # Custom permissions
            'can_approve_eft': can_approve_eft,
            'can_export_eft': can_export_eft,
        }
    except Permission.DoesNotExist as e:
        print(f"Error: Some permissions don't exist. Make sure migrations are run.")
        print(f"Missing permission: {e}")
        return
    
    # Define role permissions
    role_permissions = {
        'System Admin': [
            'add_bank', 'change_bank', 'delete_bank', 'view_bank',
            'add_zone', 'change_zone', 'delete_zone', 'view_zone',
            'add_scheme', 'change_scheme', 'delete_scheme', 'view_scheme',
            'add_supplier', 'change_supplier', 'delete_supplier', 'view_supplier',
            'add_debitaccount', 'change_debitaccount', 'delete_debitaccount', 'view_debitaccount',
        ],
        'Accounts Personnel': [
            'add_eftbatch', 'change_eftbatch', 'view_eftbatch',
            'add_efttransaction', 'change_efttransaction', 'delete_efttransaction', 'view_efttransaction',
            'view_bank', 'view_zone', 'view_scheme', 'view_supplier', 'view_debitaccount',
            'can_export_eft',
        ],
        'Authorizer': [
            'view_eftbatch', 'view_efttransaction',
            'view_bank', 'view_zone', 'view_scheme', 'view_supplier', 'view_debitaccount',
            'can_approve_eft', 'can_export_eft',
        ]
    }
    
    # Create groups and assign permissions
    for role_name, perm_codenames in role_permissions.items():
        group, created = Group.objects.get_or_create(name=role_name)
        
        if created:
            print(f"✓ Created group: {role_name}")
        else:
            print(f"✓ Group already exists: {role_name}")
        
        # Clear existing permissions
        group.permissions.clear()
        
        # Add new permissions
        added_count = 0
        for codename in perm_codenames:
            if codename in permissions_map:
                group.permissions.add(permissions_map[codename])
                added_count += 1
        
        print(f"  → Assigned {added_count} permissions to {role_name}")
    
    print("\n✓ Groups and permissions setup completed successfully!")

@receiver(post_migrate)
def setup_user_roles(sender, **kwargs):
    """Signal handler to setup roles after migrations"""
    if sender.name == 'eft_app':
        create_groups_and_permissions()