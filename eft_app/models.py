# eft_app/models.py - UPDATED VERSION WITH RBM FIELDS
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
import uuid

class Bank(models.Model):
    """Bank and SWIFT codes master data"""
    bank_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=11, unique=True, 
        validators=[RegexValidator(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$', 'Invalid SWIFT code')])
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='banks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['bank_name']
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
    
    def __str__(self):
        return f"{self.bank_name} ({self.swift_code})"

class Zone(models.Model):
    """CRWB Zones"""
    zone_code = models.CharField(max_length=10, unique=True)
    zone_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['zone_code']
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
    
    def __str__(self):
        return f"{self.zone_code} - {self.zone_name}"

class Scheme(models.Model):
    """CRWB Schemes mapped to Zones"""
    scheme_code = models.CharField(max_length=10, unique=True)
    scheme_name = models.CharField(max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name='schemes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheme_code']
        verbose_name = 'Scheme'
        verbose_name_plural = 'Schemes'
    
    def __str__(self):
        return f"{self.scheme_code} - {self.scheme_name} ({self.zone.zone_code})"

class Supplier(models.Model):
    """Suppliers/Beneficiaries with RBM-compliant fields"""
    supplier_code = models.CharField(max_length=20, unique=True, help_text="7-digit vendor code")
    supplier_name = models.CharField(max_length=200)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='suppliers')
    account_number = models.CharField(max_length=30, help_text="Beneficiary Bank Account Number")
    account_name = models.CharField(max_length=200, help_text="Payee Details/Beneficiary Name")
    
    # RBM-specific fields from payment file sample
    employee_number = models.CharField(max_length=6, blank=True, help_text="UDF2 at UBS (Optional)")
    national_id = models.CharField(max_length=8, blank=True, help_text="UDF3 at UBS (Optional)")
    credit_reference = models.CharField(max_length=50, blank=True, help_text="Payees Reference/Invoice Number")
    cost_center = models.CharField(max_length=50, blank=True, help_text="Originating Cost/Funds Centre")
    source = models.CharField(max_length=18, blank=True, help_text="Unique reference from IFMIS")
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='suppliers_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['supplier_name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f"{self.supplier_code} - {self.supplier_name}"

class DebitAccount(models.Model):
    """CRWB Debit Accounts"""
    account_number = models.CharField(max_length=20, unique=True, help_text="RBM Account only (e.g., 13006161244)")
    account_name = models.CharField(max_length=200, help_text="Debit Account Name (e.g., (ORT) MG Other Recurrent Expenditure A/C)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['account_number']
        verbose_name = 'Debit Account'
        verbose_name_plural = 'Debit Accounts'
    
    def __str__(self):
        return f"{self.account_number} - {self.account_name}"

class EFTBatch(models.Model):
    """EFT Batch header - RBM compliant"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Authorization'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('EXPORTED', 'Exported to RBM'),
    ]
    
    batch_name = models.CharField(max_length=100, help_text="File Reference: Run ID & Date")
    batch_reference = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    currency = models.CharField(max_length=3, default='MWK', help_text="Transaction Currency (MWK)")
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, help_text="File Total - Total value of transactions")
    record_count = models.IntegerField(default=0, help_text="Total Count - Total number of line-item transactions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    # RBM File reference (from payment file sample)
    file_reference = models.CharField(max_length=16, blank=True, help_text="WTC01-31.01.2023 format")
    
    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='batches_created')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, 
                                   related_name='batches_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # File generation
    generated_file = models.TextField(blank=True)  # Stores EFT file content
    generated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'EFT Batch'
        verbose_name_plural = 'EFT Batches'
        permissions = [
            ("can_approve_eft", "Can approve EFT batches"),
            ("can_export_eft", "Can export EFT files"),
        ]
    
    def __str__(self):
        return f"{self.batch_reference} - {self.batch_name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-generate file reference if not provided
        if not self.file_reference and self.batch_name:
            # Format: WTC01-31.01.2023 (we'll create a simple version)
            date_str = timezone.now().strftime('%d.%m.%Y')
            self.file_reference = f"CRWB-{date_str}"
        super().save(*args, **kwargs)
    
    def can_edit(self):
        return self.status == 'DRAFT'
    
    def can_approve(self):
        return self.status == 'PENDING'
    
    def can_export(self):
        return self.status == 'APPROVED'
    
    def update_totals(self):
        """Update batch totals from transactions"""
        transactions = self.transactions.all()
        self.total_amount = sum(t.amount for t in transactions)
        self.record_count = transactions.count()
        self.save()

class EFTTransaction(models.Model):
    """Individual EFT transactions - RBM compliant"""
    batch = models.ForeignKey(EFTBatch, on_delete=models.CASCADE, related_name='transactions')
    sequence_number = models.CharField(max_length=4, help_text="Line item Count (0001-9999)")
    
    # Mandatory RBM fields
    debit_account = models.ForeignKey(DebitAccount, on_delete=models.PROTECT, related_name='transactions')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='transactions')
    scheme = models.ForeignKey(Scheme, on_delete=models.PROTECT, related_name='transactions')
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name='transactions')
    
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)], 
                                help_text="Payment Amount")
    
    # RBM-specific fields (matching the sample EFT file)
    narration = models.CharField(max_length=200, blank=True, help_text="Description of the transaction")
    reference_number = models.CharField(max_length=16, blank=True, help_text="Invoice Number/Payees Reference")
    
    # Additional fields from payment file
    employee_number = models.CharField(max_length=6, blank=True, help_text="Employee Number (Optional)")
    national_id = models.CharField(max_length=8, blank=True, help_text="National ID (Optional)")
    cost_center = models.CharField(max_length=50, blank=True, help_text="Cost Center (Optional)")
    source_reference = models.CharField(max_length=18, blank=True, help_text="Source - Unique reference from IFMIS")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sequence_number']
        unique_together = ['batch', 'sequence_number']
        verbose_name = 'EFT Transaction'
        verbose_name_plural = 'EFT Transactions'
    
    def __str__(self):
        return f"{self.batch.batch_reference}-{self.sequence_number}: {self.amount} MWK"
    
    def save(self, *args, **kwargs):
        # Auto-derive zone from scheme if not set
        if not self.zone_id and self.scheme_id:
            self.zone = self.scheme.zone
        
        # Copy additional fields from supplier if not set
        if self.supplier_id:
            if not self.employee_number and self.supplier.employee_number:
                self.employee_number = self.supplier.employee_number
            if not self.national_id and self.supplier.national_id:
                self.national_id = self.supplier.national_id
            if not self.cost_center and self.supplier.cost_center:
                self.cost_center = self.supplier.cost_center
            if not self.source_reference and self.supplier.source:
                self.source_reference = self.supplier.source
        
        super().save(*args, **kwargs)
        
        # Update batch totals
        if self.batch:
            self.batch.update_totals()

class ApprovalAuditLog(models.Model):
    """Audit trail for approvals"""
    ACTION_CHOICES = [
        ('SUBMITTED', 'Submitted for Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('EXPORTED', 'Exported to RBM'),
    ]
    
    batch = models.ForeignKey(EFTBatch, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='audit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Approval Audit Log'
        verbose_name_plural = 'Approval Audit Logs'
    
    def __str__(self):
        return f"{self.batch.batch_reference} - {self.action} by {self.user.username} at {self.timestamp}"