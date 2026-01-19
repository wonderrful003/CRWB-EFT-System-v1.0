# eft_app/eft_generator.py
import csv
from io import StringIO
from django.http import HttpResponse
from django.utils import timezone
from .models import EFTBatch

class EFTGenerator:
    """Generates RBM-compliant EFT files"""
    
    @staticmethod
    def validate_batch(batch):
        """Validate batch before generation"""
        if batch.status != 'APPROVED':
            raise ValueError("Only approved batches can be exported")
        
        transactions = batch.transactions.all()
        
        if transactions.count() == 0:
            raise ValueError("Batch has no transactions")
        
        # Calculate totals
        total_amount = sum(t.amount for t in transactions)
        record_count = transactions.count()
        
        # Validate totals match batch
        if abs(total_amount - batch.total_amount) > 0.01:  # Allow small floating point differences
            raise ValueError(f"Transaction total ({total_amount}) doesn't match batch total ({batch.total_amount})")
        
        if record_count != batch.record_count:
            raise ValueError(f"Transaction count ({record_count}) doesn't match batch record count ({batch.record_count})")
        
        # Validate all required fields are present
        for trans in transactions:
            if not trans.debit_account:
                raise ValueError(f"Transaction {trans.sequence_number}: Debit account is required")
            if not trans.supplier:
                raise ValueError(f"Transaction {trans.sequence_number}: Supplier is required")
            if not trans.supplier.bank:
                raise ValueError(f"Transaction {trans.sequence_number}: Supplier bank is required")
            if not trans.scheme:
                raise ValueError(f"Transaction {trans.sequence_number}: Scheme is required")
            if not trans.zone:
                raise ValueError(f"Transaction {trans.sequence_number}: Zone is required")
        
        return True
    
    @staticmethod
    def format_amount(amount):
        """Format amount to 2 decimal places without thousands separator"""
        return f"{float(amount):.2f}"
    
    @staticmethod
    def generate_eft_file(batch):
        """Generate EFT file content for approved batch"""
        
        # Validate batch
        EFTGenerator.validate_batch(batch)
        
        transactions = batch.transactions.all().order_by('sequence_number')
        
        # Calculate totals
        total_amount = sum(t.amount for t in transactions)
        record_count = transactions.count()
        
        output = StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
        
        # Write header record (Type 0)
        # Format: 0;<BATCH_NAME>;MWK;<TOTAL_AMOUNT>;<RECORD_COUNT>
        writer.writerow([
            '0',
            batch.batch_name[:50],  # Truncate if necessary
            batch.currency,
            EFTGenerator.format_amount(total_amount),
            f"{record_count:04d}"
        ])
        
        # Write body records (Type 1)
        # Format: 1;<SEQ_NO>;MWK;<DEBIT_ACC>;<ZONE>;<AMOUNT>;<BENEF_NAME>;<SCHEME_CODE>;;;<CREDIT_REF>;<BANK_SWIFT>;<BENEF_ACC>;;;<REFERENCE>;<NARRATION>
        for trans in transactions:
            writer.writerow([
                '1',
                trans.sequence_number.zfill(4),
                batch.currency,
                trans.debit_account.account_number,
                trans.zone.zone_code,
                EFTGenerator.format_amount(trans.amount),
                trans.supplier.supplier_name[:55],  # Truncate to 55 chars
                trans.scheme.scheme_code,
                '',  # Empty field
                '',  # Empty field
                trans.supplier.credit_reference or '',
                trans.supplier.bank.swift_code,
                trans.supplier.account_number,
                '',  # Empty field
                '',  # Empty field
                trans.reference_number or '',
                trans.narration[:200] if trans.narration else ''  # Truncate to 200 chars
            ])
        
        content = output.getvalue()
        output.close()
        
        # Save to batch (optional - can be stored in database)
        batch.generated_file = content
        batch.generated_at = timezone.now()
        batch.save(update_fields=['generated_file', 'generated_at'])
        
        return content
    
    @staticmethod
    def generate_eft_content(batch, format='txt'):
        """Generate EFT content in specified format"""
        content = EFTGenerator.generate_eft_file(batch)
        
        if format.lower() == 'csv':
            # For CSV, we need to ensure proper formatting
            lines = content.split('\n')
            csv_output = StringIO()
            csv_writer = csv.writer(csv_output, delimiter=';')
            for line in lines:
                if line.strip():
                    csv_writer.writerow(line.split(';'))
            result = csv_output.getvalue()
            csv_output.close()
            return result
        else:
            return content
    
    @staticmethod
    def export_to_txt(content, filename):
        """Export content to TXT file"""
        response = HttpResponse(content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
        return response
    
    @staticmethod
    def export_to_csv(content, filename):
        """Export content to CSV file"""
        response = HttpResponse(content, content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        return response
    
    @staticmethod
    def generate_sample_eft():
        """Generate sample EFT file for testing"""
        sample_content = """0;TEST_1;MWK;101771778.15;0005
1;0001;MWK;12345678;CENTRAL;1000.00;Anderson;3;;;10019525;SBICMWM0;91000004;;;10019525;3-CENTRA
1;0002;MWK;12345678;CENTRAL;1000.00;CCSECUR;408;;;10019525;SBICMWM0;12345612;;;10019525;408-CENT
1;0003;MWK;12345678;CENTRAL;56153000.00;Anderson;3;;;10019524;SBICMWM0;91000004;;;10019524;3-CENTRA
1;0004;MWK;12345678;CENTRAL;11207300.00;JIBSSEC;391;;;10019524;SBICMWM0;12345678;;;10019524;391-CENT
1;0005;MWK;12345678;CENTRAL;34409478.15;EASYACC;392;;;10019524;MBBCMWM0;12345698;;;10019524;392-CENT
"""
        return sample_content
    
    @staticmethod
    def validate_eft_structure(content):
        """Validate EFT file structure"""
        lines = content.strip().split('\n')
        
        if len(lines) == 0:
            return False, "Empty file"
        
        # Check header
        header_parts = lines[0].split(';')
        if len(header_parts) != 5:
            return False, "Invalid header format"
        
        if header_parts[0] != '0':
            return False, "Header must start with 0"
        
        try:
            record_count = int(header_parts[4])
        except ValueError:
            return False, "Invalid record count in header"
        
        # Check body records
        if len(lines) - 1 != record_count:
            return False, f"Record count mismatch: header says {record_count}, file has {len(lines)-1}"
        
        total_amount = 0
        for i, line in enumerate(lines[1:], 1):
            parts = line.split(';')
            if len(parts) != 17:
                return False, f"Line {i}: Invalid number of fields ({len(parts)} instead of 17)"
            
            if parts[0] != '1':
                return False, f"Line {i}: Body record must start with 1"
            
            try:
                amount = float(parts[5])
                total_amount += amount
            except ValueError:
                return False, f"Line {i}: Invalid amount format"
        
        # Validate total amount
        try:
            header_amount = float(header_parts[3])
            if abs(total_amount - header_amount) > 0.01:
                return False, f"Total amount mismatch: header says {header_amount}, sum is {total_amount}"
        except ValueError:
            return False, "Invalid total amount in header"
        
        return True, "EFT file structure is valid"