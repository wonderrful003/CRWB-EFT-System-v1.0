# Save the code to a file

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from eft_app.models import Bank, Zone, Scheme, DebitAccount, Supplier

class Command(BaseCommand):
    help = 'Seeds CRWB Zones, Schemes, Banks, Debit Accounts, and Suppliers'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting CRWB Seed Process...")

        # 1. Create CRWB Zones
        zones = {
            'HQ_ADMIN': 'Headquarters (Lilongwe)',
            'KS_ZONE': 'Kasungu Zone',
            'MP_ZONE': 'Mponela Zone',
            'SL_ZONE': 'Salima Zone',
            'DZ_ZONE': 'Dedza Zone',
        }
        zone_objs = {}
        for code, name in zones.items():
            z, created = Zone.objects.get_or_create(
                zone_code=code, 
                defaults={'zone_name': name}
            )
            zone_objs[code] = z
            if created:
                self.stdout.write(f"✓ Zone created: {code} - {name}")
        self.stdout.write("✓ All CRWB Zones created")

        # 2. Create Schemes (Mapped to Zones per CRWB structure)
        schemes = [
            ('03000101', 'HQ Administration', 'HQ_ADMIN'),
            ('10019525', 'Mponela Main Scheme', 'MP_ZONE'),
            ('10019524', 'Salima Town Scheme', 'SL_ZONE'),
            ('10019523', 'Dedza Boma Scheme', 'DZ_ZONE'),
            ('10019530', 'Kasungu Boma Scheme', 'KS_ZONE'),
        ]
        for code, name, z_code in schemes:
            scheme, created = Scheme.objects.get_or_create(
                scheme_code=code, 
                defaults={
                    'scheme_name': name, 
                    'zone': zone_objs[z_code],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"✓ Scheme created: {code} - {name} ({zone_objs[z_code].zone_name})")
        self.stdout.write("✓ Schemes mapped to Zones")

        # 3. Create Banks
        banks = [
            ('National Bank of Malawi', 'NBMAMWM0'),
            ('Standard Bank', 'SBICMWM0'),
            ('Reserve Bank of Malawi', 'RBMAMWM0'),
            ('FDH Bank', 'FDHBMWM0'),
            ('NBS Bank', 'NBSBMWM0'),
        ]
        
        # Get any user for created_by (required field)
        admin_user = User.objects.first()
        if not admin_user:
            # Create a temporary system user
            admin_user = User.objects.create_user(
                username='system_seed',
                password='temp_password_123',
                is_active=False
            )
            admin_user.save()
        
        for name, swift in banks:
            bank, created = Bank.objects.get_or_create(
                swift_code=swift, 
                defaults={
                    'bank_name': name, 
                    'is_active': True,
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f"✓ Bank created: {name} ({swift})")
        
        self.stdout.write("✓ All Banks created")

        # 4. Create Default Debit Accounts
        debit_accounts = [
            ('13006161244', '(ORT) MG Other Recurrent Expenditure A/C'),
            ('13006161245', '(ORT) MG Capital Expenditure A/C'),
            ('13006161246', '(ORT) MG Salaries A/C'),
            ('13006161247', '(ORT) MG Project Funds A/C'),
        ]
        
        for acc_num, acc_name in debit_accounts:
            account, created = DebitAccount.objects.get_or_create(
                account_number=acc_num,
                defaults={
                    'account_name': acc_name,
                    'is_active': True,
                    'description': f'CRWB {acc_name}'
                }
            )
            if created:
                self.stdout.write(f"✓ Debit Account created: {acc_num} - {acc_name}")
        
        self.stdout.write("✓ All Debit Accounts created")

        # 5. Get references to created Banks for the suppliers
        try:
            nbm = Bank.objects.get(swift_code='NBMAMWM0')
            std = Bank.objects.get(swift_code='SBICMWM0')
        except Bank.DoesNotExist:
            self.stdout.write(self.style.ERROR("ERROR: Banks not found! Please run migration first."))
            return

        # 6. Create Sample Suppliers (Based on your provided sample files)
        suppliers_data = [
            # Code, Name, Bank, Account, Account Name
            ('57819', 'Bella Enterprise Pvt Ltd', nbm, '2004004560001', 'Bella Enterprise Main'),
            ('3', 'Anderson', std, '91000004', 'Anderson Trading'),
            ('408', 'CCSECUR', std, '12345612', 'City Center Security'),
            ('391', 'JIBSSEC', std, '12345678', 'Jibs Security Services'),
            ('392', 'EASYACC', std, '12345698', 'Easy Access Solutions'),
        ]

        for code, name, bank_obj, acc_no, acc_name in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                supplier_code=code,
                defaults={
                    'supplier_name': name,
                    'bank': bank_obj,
                    'account_number': acc_no,
                    'account_name': acc_name,
                    'created_by': admin_user,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"✓ Supplier created: {code} - {name}")

        self.stdout.write("✓ Sample Suppliers seeded")

        # 7. Summary
        self.stdout.write(self.style.SUCCESS("\n" + "="*50))
        self.stdout.write(self.style.SUCCESS("CRWB ENVIRONMENT SUCCESSFULLY SEEDED!"))
        self.stdout.write(self.style.SUCCESS("="*50))
        self.stdout.write(f"\nSummary of seeded data:")
        self.stdout.write(f"  • Zones: {Zone.objects.count()}")
        self.stdout.write(f"  • Schemes: {Scheme.objects.count()}")
        self.stdout.write(f"  • Banks: {Bank.objects.count()}")
        self.stdout.write(f"  • Debit Accounts: {DebitAccount.objects.count()}")
        self.stdout.write(f"  • Suppliers: {Supplier.objects.count()}")
        self.stdout.write(self.style.SUCCESS("\n✓ Ready to use CRWB EFT System!"))
