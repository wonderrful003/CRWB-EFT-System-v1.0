# CRWB EFT System v1.0

## 🏦 Electronic Funds Transfer System with RBM Compliance

### **One-Command Setup • Complete Data Included • Ready-to-Run**

---

## 🚀 **GET STARTED IN 60 SECONDS**

### **Windows Users (Recommended):**
```cmd
# 1. Clone the repository
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0

# 2. Run ONE command (does everything)
launch.bat
```

### **What Happens Automatically:**
✅ Creates virtual environment  
✅ Installs 44+ dependencies  
✅ Sets up database  
✅ Loads **YOUR original data** (6 users, 6 banks, 5 zones, etc.)  
✅ Starts development server  
✅ Opens http://127.0.0.1:8000  

**Your system is now IDENTICAL to the original!**

---

## 📋 **YOUR PRE-LOADED SYSTEM DATA**

| Component | Quantity | Status |
|-----------|----------|---------|
| 👤 **Users** | 6 | ✅ Original passwords preserved |
| 🏦 **Banks** | 6 | ✅ SWIFT codes included |
| 📍 **Zones** | 5 | ✅ Original configuration |
| 📋 **Schemes** | 5 | ✅ With default cost centers |
| 💼 **Suppliers** | 5 | ✅ Bank accounts loaded |
| 📊 **Total Records** | 167 | ✅ Everything identical |

**All your original users are ready to login immediately!**

---

## 🔧 **MANAGEMENT COMMANDS**

### **Setup & Launch:**
| Command | Purpose | Best For |
|---------|---------|----------|
| **`launch.bat`** | Complete setup & start server | First-time users |
| **`setup.bat`** | Setup only (no server start) | Separate setup & run |
| **`start.bat`** | Start server only | After setup |
| **`quick_setup.bat`** | Fast minimal setup | Quick testing |

### **Maintenance & Backup:**
| Command | Purpose |
|---------|---------|
| **`reset.bat`** | Reset everything (clean slate) |
| **`backup.bat`** | Create data backups |
| **`restore.bat`** | Restore from backup |
| **`update.bat`** | Update all packages |

### **Administration:**
| Command | Purpose |
|---------|---------|
| **`admin.bat`** | Create new admin user |
| **`check.bat`** | System diagnostics |
| **`runserver.bat`** | Just run server (venv active) |

---

## 🌐 **ACCESS INFORMATION**

After running `launch.bat`:
- **🌐 Application**: http://127.0.0.1:8000
- **🔧 Admin Panel**: http://127.0.0.1:8000/admin
- **👤 Login**: Use any of your 6 original users
- **🔑 Admin Fallback**: admin / admin123 (if no data file)

**Default Port**: 8000  
**Change Port**: `python manage.py runserver 8001`

---

## 🎯 **SYSTEM FEATURES**

### **Role-Based Access Control:**
| Role | Permissions | Use Case |
|------|-------------|----------|
| **👑 System Admin** | Full system management | User management, configuration |
| **📊 Accounts Personnel** | Create & manage EFT batches | Payment processing, batch creation |
| **✅ Authorizer** | Approve/reject batches | Quality control, final approval |

### **Core Functionality:**
- **Payment Processing**: Batch creation with real-time validation
- **RBM Compliance**: Banking-compliant EFT file generation (TXT/CSV)
- **Multi-Level Approval**: Complete audit trail for compliance
- **Master Data Management**: Banks, suppliers, zones, schemes
- **Real-Time Reporting**: Role-specific dashboards and analytics

### **Technical Specifications:**
- **Backend**: Django 4.2.27
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite3 (Development)
- **Authentication**: Django Auth with custom permissions
- **File Formats**: TXT, CSV, Excel export

---

## 📁 **PROJECT STRUCTURE**

```
CRWB-EFT-System-v1.0/
├── 📜 launch.bat                 # Main launcher (ONE COMMAND)
├── 📜 setup.bat                  # Setup only
├── 📜 start.bat                  # Start server only
├── 📜 reset.bat                  # Reset everything
├── 📜 backup.bat                 # Create backups
├── 📜 restore.bat                # Restore from backup
├── 📜 update.bat                 # Update packages
├── 📜 admin.bat                  # Create admin user
├── 📜 check.bat                  # System diagnostics
├── 📜 quick_setup.bat           # Fast minimal setup
├── 📜 runserver.bat             # Just run server
│
├── 📄 requirements.txt           # 44+ Python dependencies
├── 📄 manage.py                  # Django management
│
├── 📁 crwb_eft/                 # Project settings
│   ├── settings.py              # Configuration
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI configuration
│
├── 📁 eft_app/                  # Main application
│   ├── models.py               # Database models
│   ├── views.py                # Business logic
│   ├── forms.py                # Form definitions
│   ├── admin.py                # Admin interface
│   ├── fixtures/               # YOUR DATA
│   │   └── all_data.json      # Complete original system
│   └── templates/              # HTML templates
│
├── 📁 templates/                # Base templates
├── 📁 static/                  # CSS, JS, images
└── 📁 media/                   # Uploaded files
```

---

## 🛠️ **DEVELOPER WORKFLOW**

### **For Contributors:**
```bash
# 1. Create feature branch
git checkout -b feature/description

# 2. Test with your changes
launch.bat

# 3. Export updated data (if changed)
python manage.py dumpdata --indent 2 > eft_app/fixtures/all_data.json

# 4. Commit and push
git add .
git commit -m "Feature: description"
git push origin feature/description
```

### **Database Operations:**
```bash
# Export current system state
backup.bat

# Create data migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load specific data
python manage.py loaddata eft_app/fixtures/specific_data.json
```

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues & Solutions:**

#### **1. Python Not Found:**
```cmd
# Check installation
python --version
# Should show Python 3.9+

# If not installed:
# Download from: https://python.org
# Check "Add Python to PATH" during installation
```

#### **2. Port 8000 Already in Use:**
```cmd
# Method 1: Kill process
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Method 2: Use different port
start.bat 8001
```

#### **3. Virtual Environment Issues:**
```cmd
# Delete and recreate
reset.bat
launch.bat
```

#### **4. Database Corruption:**
```cmd
# 1. Create backup
backup.bat

# 2. Reset database
reset.bat

# 3. Restore from backup
restore.bat
```

#### **5. Package Installation Failures:**
```cmd
# Try minimal setup
quick_setup.bat
```

### **Diagnostic Tools:**
```cmd
# Run system check
check.bat

# Check Django installation
python manage.py check

# Verify database
python manage.py dbshell
```

---

## 📊 **SYSTEM REQUIREMENTS**

### **Minimum:**
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum
- **Storage**: 500MB free space
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+

### **Recommended:**
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.11 or higher
- **RAM**: 8GB or more
- **Storage**: 1GB free space
- **Browser**: Latest Chrome/Firefox/Edge

---

## 🔒 **SECURITY FEATURES**

### **Authentication:**
- Role-based access control (RBAC)
- Secure password hashing (PBKDF2)
- Session management with timeout
- Login attempt limiting

### **Data Protection:**
- SQL injection prevention
- XSS protection
- CSRF tokens
- Secure headers
- Audit logging

### **Compliance:**
- Audit trail for all actions
- User activity logging
- Data validation at all levels
- File integrity checks

---

## 📈 **DEPLOYMENT**

### **Development (Default):**
```cmd
# Already configured for development
launch.bat
```

### **Production Checklist:**
1. Set `DEBUG = False` in `crwb_eft/settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL/MySQL instead of SQLite
4. Set up proper static file serving
5. Configure HTTPS/SSL
6. Set up regular backups with `backup.bat`

### **Backup Strategy:**
```cmd
# Daily automated backup (add to Task Scheduler)
backup.bat

# Weekly full export
python manage.py dumpdata --indent 2 > weekly_backup_$(date +%Y%m%d).json
```

---

## 📝 **API DOCUMENTATION**

### **Available Endpoints:**
```
GET    /api/supplier/{id}/details/    # Supplier information
GET    /api/scheme/{id}/details/      # Scheme details with cost center
GET    /api/scheme/{id}/zone/         # Zone information
```

### **Authentication:**
All API endpoints require session authentication. Use the same login as the web interface.

### **Response Format:**
```json
{
    "success": true,
    "data": {
        "field": "value"
    }
}
```

---

## 🔄 **MAINTENANCE SCHEDULE**

### **Daily:**
- Run `check.bat` for system health
- Verify backups with `backup.bat`
- Check server logs

### **Weekly:**
- Run `update.bat` for package updates
- Review audit logs
- Test backup restoration

### **Monthly:**
- Security review
- Performance optimization
- Database cleanup

---

## 🆘 **SUPPORT & HELP**

### **Quick Help:**
1. **First**: Run `check.bat` for diagnostics
2. **Second**: Check troubleshooting section above
3. **Third**: Create issue on GitHub

### **Common Solutions:**
```cmd
# Most issues can be fixed with:
reset.bat
launch.bat
```

### **Getting Help:**
- **GitHub Issues**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0/issues
- **Documentation**: This README file
- **System Logs**: Check server output in terminal

---

## 📄 **LICENSE & USAGE**

### **Copyright Notice:**
© 2025 CRWB EFT System. All rights reserved.

### **Usage Rights:**
- **Internal Use**: Approved for CRWB operations
- **Modification**: Not permitted without authorization
- **Distribution**: Restricted to authorized personnel only
- **Commercial Use**: Requires written agreement

### **Compliance Requirements:**
- Maintain audit trails
- Regular security assessments
- Data protection compliance
- User access logging

---

## 🙏 **ACKNOWLEDGMENTS**

- **Django Framework** and community
- **Bootstrap Team** for frontend components
- **Python Community** for excellent tools
- **RBM Compliance Teams** for banking standards
- **All Contributors** and testers

---

## 📞 **CONTACT INFORMATION**

### **Development Team:**
- **Repository**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0
- **Issues**: GitHub Issues tab
- **Support**: Internal IT department

### **System Information:**
- **Version**: CRWB EFT System v1.0
- **Last Updated**: January 2025
- **Data Version**: Includes complete original system data
- **Status**: Production Ready

---

## 🎉 **READY TO START?**

```cmd
# Three simple commands:
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
launch.bat
```

**Your complete EFT payment system is ready in minutes, with all your original data preserved!**