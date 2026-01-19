# eft_app/urls.py
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Redirect root URL to login page
    path('', RedirectView.as_view(pattern_name='login'), name='home'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # System Admin URLs - User Management (CHANGED: 'admin/' to 'system-admin/')
    path('system-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('system-admin/users/', views.user_list, name='user_list'),
    path('system-admin/users/create/', views.user_create, name='user_create'),
    path('system-admin/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('system-admin/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('system-admin/users/<int:user_id>/reset-password/', views.user_reset_password, name='user_reset_password'),
    
    # System Admin URLs - Banks
    path('system-admin/banks/', views.BankListView.as_view(), name='bank_list'),
    path('system-admin/banks/add/', views.BankCreateView.as_view(), name='bank_add'),
    path('system-admin/banks/<int:pk>/edit/', views.BankUpdateView.as_view(), name='bank_edit'),
    path('system-admin/banks/<int:pk>/delete/', views.BankDeleteView.as_view(), name='bank_delete'),
    
    # System Admin URLs - Zones
    path('system-admin/zones/', views.ZoneListView.as_view(), name='zone_list'),
    path('system-admin/zones/add/', views.ZoneCreateView.as_view(), name='zone_add'),
    path('system-admin/zones/<int:pk>/edit/', views.ZoneUpdateView.as_view(), name='zone_edit'),
    path('system-admin/zones/<int:pk>/delete/', views.ZoneDeleteView.as_view(), name='zone_delete'),
    
    # System Admin URLs - Suppliers
    path('system-admin/suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('system-admin/suppliers/add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('system-admin/suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_edit'),
    path('system-admin/suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # System Admin URLs - Schemes
    path('system-admin/schemes/', views.SchemeListView.as_view(), name='scheme_list'),
    path('system-admin/schemes/add/', views.SchemeCreateView.as_view(), name='scheme_add'),
    path('system-admin/schemes/<int:pk>/edit/', views.SchemeUpdateView.as_view(), name='scheme_edit'),
    path('system-admin/schemes/<int:pk>/delete/', views.SchemeDeleteView.as_view(), name='scheme_delete'),
    
    # System Admin URLs - Debit Accounts
    path('system-admin/debit-accounts/', views.DebitAccountListView.as_view(), name='debit_account_list'),
    path('system-admin/debit-accounts/add/', views.DebitAccountCreateView.as_view(), name='debit_account_add'),
    path('system-admin/debit-accounts/<int:pk>/edit/', views.DebitAccountUpdateView.as_view(), name='debit_account_edit'),
    path('system-admin/debit-accounts/<int:pk>/delete/', views.DebitAccountDeleteView.as_view(), name='debit_account_delete'),
    
    # Accounts Personnel URLs (NO CHANGE here)
    path('accounts/dashboard/', views.accounts_dashboard, name='accounts_dashboard'),
    path('accounts/batches/', views.batch_list, name='batch_list'),
    path('accounts/batches/create/', views.create_batch, name='create_batch'),
    path('accounts/batches/<int:batch_id>/edit/', views.edit_batch, name='edit_batch'),
    path('accounts/batches/<int:batch_id>/view/', views.view_batch, name='view_batch'),
    path('accounts/batches/<int:batch_id>/submit/', views.submit_for_approval, name='submit_batch'),
    path('accounts/batches/<int:batch_id>/delete/', views.delete_batch, name='delete_batch'),
    path('accounts/batches/<int:batch_id>/transaction/add/', views.add_transaction, name='add_transaction'),
    path('accounts/batches/<int:batch_id>/transaction/<int:transaction_id>/delete/', 
         views.delete_transaction, name='delete_transaction'),
    path('accounts/batches/<int:batch_id>/export/<str:format>/', views.export_batch, name='export_batch'),
    
    # Authorizer URLs (NO CHANGE here)
    path('authorizer/dashboard/', views.authorizer_dashboard, name='authorizer_dashboard'),
    path('authorizer/batches/', views.authorizer_batch_list, name='authorizer_batch_list'),
    path('authorizer/batches/<int:batch_id>/review/', views.review_batch, name='review_batch'),
    path('authorizer/batches/<int:batch_id>/approve/', views.approve_batch, name='approve_batch'),
    path('authorizer/batches/<int:batch_id>/reject/', views.reject_batch, name='reject_batch'),
    
    # API URLs (NO CHANGE here)
    path('api/supplier/<int:supplier_id>/details/', views.get_supplier_details, name='supplier_details'),
    path('api/scheme/<int:scheme_id>/zone/', views.get_scheme_zone, name='scheme_zone'),
]