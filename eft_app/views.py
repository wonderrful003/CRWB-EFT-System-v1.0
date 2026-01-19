# eft_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction as db_transaction
from django.db.models import Sum, Count, Q
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
import json

from .models import (
    User, Bank, Zone, Scheme, Supplier, DebitAccount,
    EFTBatch, EFTTransaction, ApprovalAuditLog
)
from .forms import (
    BankForm, ZoneForm, SchemeForm, SupplierForm, DebitAccountForm,
    EFTBatchForm, EFTTransactionForm, BatchApprovalForm, BatchRejectionForm,
    UserRegistrationForm
)
from .eft_generator import EFTGenerator

# ================ COMMON VIEWS ================

@login_required
def dashboard(request):
    """Role-based dashboard"""
    user = request.user
    
    # Check user groups
    if user.is_superuser or user.groups.filter(name='System Admin').exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name='Accounts Personnel').exists():
        return redirect('accounts_dashboard')
    elif user.groups.filter(name='Authorizer').exists():
        return redirect('authorizer_dashboard')
    else:
        messages.warning(request, 'No role assigned. Contact administrator.')
        return redirect('logout')

# ================ SYSTEM ADMIN VIEWS ================

def is_system_admin(user):
    """Check if user is system admin"""
    return user.is_superuser or user.groups.filter(name='System Admin').exists()

@login_required
@user_passes_test(is_system_admin)
def admin_dashboard(request):
    """System Admin Dashboard"""
    stats = {
        'banks_count': Bank.objects.count(),
        'suppliers_count': Supplier.objects.count(),
        'zones_count': Zone.objects.count(),
        'schemes_count': Scheme.objects.count(),
        'debit_accounts_count': DebitAccount.objects.count(),
        'users_count': User.objects.count(),
    }
    
    return render(request, 'admin/dashboard.html', {'stats': stats})

# ================ USER MANAGEMENT VIEWS ================

@login_required
@user_passes_test(is_system_admin)
def user_list(request):
    """List all system users"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
@user_passes_test(is_system_admin)
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Assign to group
                role = form.cleaned_data['role']
                group = Group.objects.get(name=role)
                user.groups.add(group)
                
                messages.success(request, f'User "{user.username}" created successfully with role "{role}"')
                return redirect('user_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'admin/user_form.html', {'form': form})

@login_required
@user_passes_test(is_system_admin)
def user_edit(request, user_id):
    """Edit existing user"""
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        
        with db_transaction.atomic():
            user_obj.username = username
            user_obj.email = email
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.is_active = is_active
            user_obj.save()
            
            # Update group
            user_obj.groups.clear()
            if role:
                group = Group.objects.get(name=role)
                user_obj.groups.add(group)
            
            messages.success(request, f'User "{user_obj.username}" updated successfully')
            return redirect('user_list')
    
    current_role = user_obj.groups.first().name if user_obj.groups.exists() else ''
    
    return render(request, 'admin/user_edit.html', {
        'user_obj': user_obj,
        'current_role': current_role,
        'roles': ['System Admin', 'Accounts Personnel', 'Authorizer']
    })

@login_required
@user_passes_test(is_system_admin)
@require_POST
def user_delete(request, user_id):
    """Delete user"""
    user_obj = get_object_or_404(User, id=user_id)
    
    # Prevent deleting self
    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own account')
        return redirect('user_list')
    
    username = user_obj.username
    user_obj.delete()
    messages.success(request, f'User "{username}" deleted successfully')
    return redirect('user_list')

@login_required
@user_passes_test(is_system_admin)
def user_reset_password(request, user_id):
    """Reset user password"""
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, f'Password reset successfully for user "{user_obj.username}"')
            return redirect('user_list')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'admin/user_reset_password.html', {'user_obj': user_obj})

# ================ BANK CRUD VIEWS ================

class BankListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Bank
    template_name = 'admin/bank_list.html'
    context_object_name = 'banks'
    permission_required = 'eft_app.view_bank'
    paginate_by = 20

class BankCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'admin/bank_form.html'
    permission_required = 'eft_app.add_bank'
    success_url = reverse_lazy('bank_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Bank created successfully')
        return super().form_valid(form)

class BankUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'admin/bank_form.html'
    permission_required = 'eft_app.change_bank'
    success_url = reverse_lazy('bank_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Bank updated successfully')
        return super().form_valid(form)

class BankDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Bank
    template_name = 'admin/bank_confirm_delete.html'
    permission_required = 'eft_app.delete_bank'
    success_url = reverse_lazy('bank_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Bank deleted successfully')
        return super().delete(request, *args, **kwargs)

# ================ ZONE CRUD VIEWS ================

class ZoneListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Zone
    template_name = 'admin/zone_list.html'
    context_object_name = 'zones'
    permission_required = 'eft_app.view_zone'
    paginate_by = 20

class ZoneCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'admin/zone_form.html'
    permission_required = 'eft_app.add_zone'
    success_url = reverse_lazy('zone_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Zone created successfully')
        return super().form_valid(form)

class ZoneUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'admin/zone_form.html'
    permission_required = 'eft_app.change_zone'
    success_url = reverse_lazy('zone_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Zone updated successfully')
        return super().form_valid(form)

class ZoneDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Zone
    template_name = 'admin/zone_confirm_delete.html'
    permission_required = 'eft_app.delete_zone'
    success_url = reverse_lazy('zone_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Zone deleted successfully')
        return super().delete(request, *args, **kwargs)

# ================ SUPPLIER CRUD VIEWS ================

class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Supplier
    template_name = 'admin/supplier_list.html'
    context_object_name = 'suppliers'
    permission_required = 'eft_app.view_supplier'
    paginate_by = 20

class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'admin/supplier_form.html'
    permission_required = 'eft_app.add_supplier'
    success_url = reverse_lazy('supplier_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Supplier created successfully')
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'admin/supplier_form.html'
    permission_required = 'eft_app.change_supplier'
    success_url = reverse_lazy('supplier_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Supplier updated successfully')
        return super().form_valid(form)

class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'admin/supplier_confirm_delete.html'
    permission_required = 'eft_app.delete_supplier'
    success_url = reverse_lazy('supplier_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Supplier deleted successfully')
        return super().delete(request, *args, **kwargs)

# ================ SCHEME CRUD VIEWS ================

class SchemeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Scheme
    template_name = 'admin/scheme_list.html'
    context_object_name = 'schemes'
    permission_required = 'eft_app.view_scheme'
    paginate_by = 20

class SchemeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Scheme
    form_class = SchemeForm
    template_name = 'admin/scheme_form.html'
    permission_required = 'eft_app.add_scheme'
    success_url = reverse_lazy('scheme_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Scheme created successfully')
        return super().form_valid(form)

class SchemeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Scheme
    form_class = SchemeForm
    template_name = 'admin/scheme_form.html'
    permission_required = 'eft_app.change_scheme'
    success_url = reverse_lazy('scheme_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Scheme updated successfully')
        return super().form_valid(form)

class SchemeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Scheme
    template_name = 'admin/scheme_confirm_delete.html'
    permission_required = 'eft_app.delete_scheme'
    success_url = reverse_lazy('scheme_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Scheme deleted successfully')
        return super().delete(request, *args, **kwargs)

# ================ DEBIT ACCOUNT CRUD VIEWS ================

class DebitAccountListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DebitAccount
    template_name = 'admin/debit_account_list.html'
    context_object_name = 'debit_accounts'
    permission_required = 'eft_app.view_debitaccount'
    paginate_by = 20

class DebitAccountCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DebitAccount
    form_class = DebitAccountForm
    template_name = 'admin/debit_account_form.html'
    permission_required = 'eft_app.add_debitaccount'
    success_url = reverse_lazy('debit_account_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Debit Account created successfully')
        return super().form_valid(form)

class DebitAccountUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DebitAccount
    form_class = DebitAccountForm
    template_name = 'admin/debit_account_form.html'
    permission_required = 'eft_app.change_debitaccount'
    success_url = reverse_lazy('debit_account_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Debit Account updated successfully')
        return super().form_valid(form)

class DebitAccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DebitAccount
    template_name = 'admin/debit_account_confirm_delete.html'
    permission_required = 'eft_app.delete_debitaccount'
    success_url = reverse_lazy('debit_account_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Debit Account deleted successfully')
        return super().delete(request, *args, **kwargs)

# ================ ACCOUNTS PERSONNEL VIEWS ================

def is_accounts_personnel(user):
    """Check if user is accounts personnel"""
    return user.groups.filter(name='Accounts Personnel').exists()

@login_required
@user_passes_test(is_accounts_personnel)
def accounts_dashboard(request):
    """Accounts Personnel Dashboard"""
    user = request.user
    
    # Get batch statistics
    batches = EFTBatch.objects.filter(created_by=user)
    
    stats = {
        'total_batches': batches.count(),
        'draft_batches': batches.filter(status='DRAFT').count(),
        'pending_batches': batches.filter(status='PENDING').count(),
        'approved_batches': batches.filter(status='APPROVED').count(),
        'rejected_batches': batches.filter(status='REJECTED').count(),
        'total_amount': batches.filter(status='APPROVED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    
    recent_batches = batches.order_by('-created_at')[:5]
    
    return render(request, 'accounts/dashboard.html', {
        'stats': stats,
        'recent_batches': recent_batches
    })

@login_required
@user_passes_test(is_accounts_personnel)
def create_batch(request):
    """Create new EFT batch"""
    if request.method == 'POST':
        form = EFTBatchForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                batch = form.save(commit=False)
                batch.created_by = request.user
                batch.batch_reference = f"CRWB-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
                batch.save()
                
                messages.success(request, 'EFT batch created successfully')
                return redirect('edit_batch', batch_id=batch.id)
    else:
        form = EFTBatchForm()
    
    return render(request, 'accounts/create_batch.html', {'form': form})

@login_required
@user_passes_test(is_accounts_personnel)
def edit_batch(request, batch_id):
    """Edit EFT batch (only in DRAFT status)"""
    batch = get_object_or_404(EFTBatch, id=batch_id, created_by=request.user)
    
    if batch.status != 'DRAFT':
        messages.error(request, 'Cannot edit batch that is not in DRAFT status')
        return redirect('accounts_dashboard')
    
    transactions = batch.transactions.all().order_by('sequence_number')
    
    if request.method == 'POST':
        # Handle batch update
        form = EFTBatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch updated successfully')
            return redirect('edit_batch', batch_id=batch.id)
    else:
        form = EFTBatchForm(instance=batch)
    
    transaction_form = EFTTransactionForm()
    
    return render(request, 'accounts/edit_batch.html', {
        'batch': batch,
        'transactions': transactions,
        'form': form,
        'transaction_form': transaction_form,
        'total_amount': sum(t.amount for t in transactions)
    })

@login_required
@user_passes_test(is_accounts_personnel)
def add_transaction(request, batch_id):
    """Add transaction to batch"""
    batch = get_object_or_404(EFTBatch, id=batch_id, created_by=request.user)
    
    if batch.status != 'DRAFT':
        return JsonResponse({
            'success': False,
            'message': 'Cannot add transactions to batch that is not in DRAFT status'
        })
    
    if request.method == 'POST':
        form = EFTTransactionForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                transaction = form.save(commit=False)
                transaction.batch = batch
                
                # Generate sequence number
                last_seq = batch.transactions.order_by('sequence_number').last()
                if last_seq:
                    next_seq = int(last_seq.sequence_number) + 1
                else:
                    next_seq = 1
                transaction.sequence_number = str(next_seq).zfill(4)
                
                # Auto-derive zone from scheme
                transaction.zone = transaction.scheme.zone
                
                transaction.save()
                
                # Update batch totals
                batch.update_totals()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Transaction added successfully',
                    'transaction_id': transaction.id,
                    'sequence_number': transaction.sequence_number,
                    'amount': str(transaction.amount),
                    'supplier_name': transaction.supplier.supplier_name,
                    'batch_total': str(batch.total_amount),
                    'record_count': batch.record_count
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_accounts_personnel)
def delete_transaction(request, batch_id, transaction_id):
    """Delete transaction from batch"""
    batch = get_object_or_404(EFTBatch, id=batch_id, created_by=request.user)
    
    if batch.status != 'DRAFT':
        return JsonResponse({
            'success': False,
            'message': 'Cannot delete transactions from batch that is not in DRAFT status'
        })
    
    transaction = get_object_or_404(EFTTransaction, id=transaction_id, batch=batch)
    
    with db_transaction.atomic():
        transaction.delete()
        batch.update_totals()
        
        # Renumber remaining transactions
        transactions = batch.transactions.all().order_by('id')
        for idx, trans in enumerate(transactions, 1):
            trans.sequence_number = str(idx).zfill(4)
            trans.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Transaction deleted successfully',
        'batch_total': str(batch.total_amount),
        'record_count': batch.record_count
    })

@login_required
@user_passes_test(is_accounts_personnel)
def submit_for_approval(request, batch_id):
    """Submit batch for approval"""
    batch = get_object_or_404(EFTBatch, id=batch_id, created_by=request.user)
    
    if batch.status != 'DRAFT':
        messages.error(request, 'Only DRAFT batches can be submitted for approval')
        return redirect('view_batch', batch_id=batch.id)
    
    # Validate batch
    if batch.transactions.count() == 0:
        messages.error(request, 'Cannot submit empty batch')
        return redirect('edit_batch', batch_id=batch.id)
    
    with db_transaction.atomic():
        batch.status = 'PENDING'
        batch.save()
        
        # Create audit log
        ApprovalAuditLog.objects.create(
            batch=batch,
            action='SUBMITTED',
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Batch submitted for approval successfully')
    
    return redirect('accounts_dashboard')

@login_required
@user_passes_test(is_accounts_personnel)
@require_POST
def delete_batch(request, batch_id):
    """Delete a draft batch"""
    batch = get_object_or_404(EFTBatch, id=batch_id, created_by=request.user)
    
    if batch.status != 'DRAFT':
        messages.error(request, 'Only DRAFT batches can be deleted')
        return redirect('batch_list')
    
    with db_transaction.atomic():
        batch_name = batch.batch_name
        batch.delete()
        messages.success(request, f'Batch "{batch_name}" deleted successfully')
    
    return redirect('batch_list')

@login_required
def view_batch(request, batch_id):
    """View batch details"""
    batch = get_object_or_404(EFTBatch, id=batch_id)
    
    # Check permission
    if not (batch.created_by == request.user or 
            request.user.has_perm('eft_app.can_approve_eft') or
            request.user.is_superuser):
        messages.error(request, 'You do not have permission to view this batch')
        return redirect('dashboard')
    
    transactions = batch.transactions.all().order_by('sequence_number')
    audit_logs = batch.audit_logs.all().order_by('-timestamp')
    
    return render(request, 'accounts/view_batch.html', {
        'batch': batch,
        'transactions': transactions,
        'audit_logs': audit_logs
    })

@login_required
def export_batch(request, batch_id, format='txt'):
    """Export EFT file (only for approved batches)"""
    batch = get_object_or_404(EFTBatch, id=batch_id)
    
    # Check if user can export
    if not (request.user.has_perm('eft_app.can_export_eft') and batch.status == 'APPROVED'):
        messages.error(request, 'You do not have permission to export this file or batch is not approved')
        return redirect('view_batch', batch_id=batch.id)
    
    # Generate file content
    try:
        generator = EFTGenerator()
        content = generator.generate_eft_file(batch)
        filename = f"CRWB_EFT_{batch.batch_reference}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == 'csv':
            response = generator.export_to_csv(content, filename)
        else:
            response = generator.export_to_txt(content, filename)
        
        # Log the export
        ApprovalAuditLog.objects.create(
            batch=batch,
            action='EXPORTED',
            user=request.user,
            remarks=f'Exported as {format.upper()}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error generating file: {str(e)}')
        return redirect('view_batch', batch_id=batch.id)

@login_required
@user_passes_test(is_accounts_personnel)
def batch_list(request):
    """List all batches for accounts personnel"""
    batches = EFTBatch.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        batches = batches.filter(status=status_filter)
    
    return render(request, 'accounts/batch_list.html', {
        'batches': batches,
        'status_filter': status_filter
    })

# ================ AUTHORIZER VIEWS ================

def is_authorizer(user):
    """Check if user is authorizer"""
    return user.groups.filter(name='Authorizer').exists()

@login_required
@user_passes_test(is_authorizer)
def authorizer_dashboard(request):
    """Authorizer Dashboard"""
    # Get pending batches
    pending_batches = EFTBatch.objects.filter(status='PENDING').order_by('-created_at')
    
    # Get recent approvals
    recent_approvals = EFTBatch.objects.filter(
        status__in=['APPROVED', 'REJECTED']
    ).order_by('-approved_at')[:10]
    
    stats = {
        'pending_count': pending_batches.count(),
        'approved_today': EFTBatch.objects.filter(
            status='APPROVED',
            approved_at__date=timezone.now().date()
        ).count(),
        'total_approved': EFTBatch.objects.filter(status='APPROVED').count(),
        'total_rejected': EFTBatch.objects.filter(status='REJECTED').count(),
    }
    
    return render(request, 'authorizer/dashboard.html', {
        'pending_batches': pending_batches,
        'recent_approvals': recent_approvals,
        'stats': stats
    })

@login_required
@user_passes_test(is_authorizer)
def review_batch(request, batch_id):
    """Review batch for approval/rejection"""
    batch = get_object_or_404(EFTBatch, id=batch_id, status='PENDING')
    
    # Prevent self-approval
    if batch.created_by == request.user:
        messages.error(request, 'You cannot approve or reject your own batch')
        return redirect('authorizer_dashboard')
    
    transactions = batch.transactions.all().order_by('sequence_number')
    approval_form = BatchApprovalForm()
    rejection_form = BatchRejectionForm()
    
    return render(request, 'authorizer/review_batch.html', {
        'batch': batch,
        'transactions': transactions,
        'approval_form': approval_form,
        'rejection_form': rejection_form,
        'total_amount': sum(t.amount for t in transactions)
    })

@login_required
@user_passes_test(is_authorizer)
def approve_batch(request, batch_id):
    """Approve EFT batch"""
    batch = get_object_or_404(EFTBatch, id=batch_id, status='PENDING')
    
    # Prevent self-approval
    if batch.created_by == request.user:
        messages.error(request, 'You cannot approve your own batch')
        return redirect('authorizer_dashboard')
    
    if request.method == 'POST':
        form = BatchApprovalForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                batch.status = 'APPROVED'
                batch.approved_by = request.user
                batch.approved_at = timezone.now()
                batch.save()
                
                # Create audit log
                ApprovalAuditLog.objects.create(
                    batch=batch,
                    action='APPROVED',
                    user=request.user,
                    remarks=form.cleaned_data['remarks'],
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, 'Batch approved successfully')
                return redirect('authorizer_dashboard')
    
    messages.error(request, 'Invalid request')
    return redirect('review_batch', batch_id=batch_id)

@login_required
@user_passes_test(is_authorizer)
def reject_batch(request, batch_id):
    """Reject EFT batch"""
    batch = get_object_or_404(EFTBatch, id=batch_id, status='PENDING')
    
    # Prevent self-approval
    if batch.created_by == request.user:
        messages.error(request, 'You cannot reject your own batch')
        return redirect('authorizer_dashboard')
    
    if request.method == 'POST':
        form = BatchRejectionForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                batch.status = 'REJECTED'
                batch.rejection_reason = form.cleaned_data['rejection_reason']
                batch.save()
                
                # Create audit log
                ApprovalAuditLog.objects.create(
                    batch=batch,
                    action='REJECTED',
                    user=request.user,
                    remarks=form.cleaned_data['rejection_reason'],
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, 'Batch rejected successfully')
                return redirect('authorizer_dashboard')
    
    messages.error(request, 'Invalid request')
    return redirect('review_batch', batch_id=batch_id)

@login_required
@user_passes_test(is_authorizer)
def authorizer_batch_list(request):
    """List all batches for authorizer"""
    # Authorizer can see all batches except their own drafts
    batches = EFTBatch.objects.exclude(
        Q(status='DRAFT', created_by=request.user)
    ).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        batches = batches.filter(status=status_filter)
    
    return render(request, 'authorizer/batch_list.html', {
        'batches': batches,
        'status_filter': status_filter
    })

# ================ API VIEWS ================

@login_required
def get_supplier_details(request, supplier_id):
    """Get supplier details for AJAX"""
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    data = {
        'bank_name': supplier.bank.bank_name,
        'swift_code': supplier.bank.swift_code,
        'account_number': supplier.account_number,
        'account_name': supplier.account_name,
        'credit_reference': supplier.credit_reference,
    }
    
    return JsonResponse(data)

@login_required
def get_scheme_zone(request, scheme_id):
    """Get zone for a scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    data = {
        'zone_code': scheme.zone.zone_code,
        'zone_name': scheme.zone.zone_name,
    }
    
    return JsonResponse(data)