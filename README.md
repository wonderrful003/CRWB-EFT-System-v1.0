# CRWB EFT System v1.0

## 🏦 Electronic Funds Transfer System with RBM Compliance

### **One-Command Setup • Complete Data Included • Ready-to-Run**

---

## 🚀 **QUICK START (Recommended)**

### **For Windows Users:**
```cmd
# 1. Clone the repository
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0

# 2. Run ONE command (does everything automatically)
launch.bat
```

### **For Mac/Linux Users:**
```bash
# 1. Clone the repository
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0

# 2. Make scripts executable
chmod +x setup.sh start.sh

# 3. Run setup
./setup.sh

# 4. Start server
./start.sh
```

---

## ⚠️ **IMPORTANT PREREQUISITE: PYTHON 3.9.0**

**This system requires Python 3.9.0 specifically for compatibility.**

### **Check Your Python Version:**
```cmd
python --version
# Should output: Python 3.9.0
```

### **If Python 3.9.0 is NOT installed:**

#### **Windows:**
1. Download Python 3.9.0 from: https://www.python.org/downloads/release/python-390/
2. Run installer
3. **CRITICAL**: Check "Add Python 3.9 to PATH"
4. Complete installation
5. Restart Command Prompt

#### **Mac:**
```bash
# Using Homebrew
brew install python@3.9

# Or download from: https://www.python.org/downloads/release/python-390/
```

#### **Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev

# Set as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```

---

## 📋 **WHAT GETS INSTALLED AUTOMATICALLY**

| Component | Quantity | Status |
|-----------|----------|---------|
| 👤 **Users** | 6 | ✅ Original passwords preserved |
| 🏦 **Banks** | 6 | ✅ SWIFT codes included |
| 📍 **Zones** | 5 | ✅ Original configuration |
| 📋 **Schemes** | 5 | ✅ With default cost centers |
| 💼 **Suppliers** | 5 | ✅ Bank accounts loaded |
| 📊 **Total Records** | 167 | ✅ Everything identical |

**Your complete original system is preserved and ready to use!**

---

## 🔧 **MANUAL SETUP FOR PYTHON 3.9.0 (Step-by-Step)**

### **Step 1: Verify Python 3.9.0**
```cmd
python --version
# MUST show: Python 3.9.0

# If shows a different version:
# Windows: Check PATH or use python3.9 command
# Mac/Linux: Use python3.9 or python3.9 command
```

### **Step 2: Clone Repository**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
```

### **Step 3: Create Virtual Environment with Python 3.9.0**
```cmd
# Windows (using Python 3.9.0 specifically)
python -m venv venv
venv\Scripts\activate

# Mac/Linux (using Python 3.9.0 specifically)
python3.9 -m venv venv
source venv/bin/activate
```

### **Step 4: Install Requirements for Python 3.9.0**
```cmd
# This will install packages compatible with Python 3.9.0
pip install -r requirements.txt

# If requirements.txt fails, install Django 4.2.27 (Python 3.9 compatible):
pip install Django==4.2.27
```

### **Step 5: Setup Database**
```cmd
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### **Step 6: Load Your Data**
```cmd
# Load your complete original system
python manage.py loaddata eft_app/fixtures/all_data.json

# Verify data was loaded
python manage.py shell -c "
from django.contrib.auth.models import User
print(f'✅ Loaded {User.objects.count()} users from your system')
"
```

### **Step 7: Create Admin User (Optional)**
```cmd
# Only needed if data file is missing
python manage.py createsuperuser
# Follow prompts: admin, admin@crwb.gov.mw, admin123
```

### **Step 8: Start Server**
```cmd
python manage.py runserver
```

### **Step 9: Access System**
- **🌐 Application**: http://127.0.0.1:8000
- **🔧 Admin Panel**: http://127.0.0.1:8000/admin
- **👤 Login**: Use your original users or admin/admin123

---

## 🛠️ **PYTHON 3.9.0 SPECIFIC TROUBLESHOOTING**

### **Common Python 3.9.0 Issues:**

#### **1. "Python not found" or wrong version:**
```cmd
# Check all Python installations
where python

# If Python 3.9.0 is installed but not default:
# Windows: Use full path: C:\Python39\python.exe
# Mac/Linux: Use python3.9 command

# Set Python 3.9.0 as default temporarily:
# Windows:
set PATH=C:\Python39;%PATH%

# Mac/Linux:
alias python=python3.9
```

#### **2. "pip not found" with Python 3.9.0:**
```cmd
# Ensure pip is installed for Python 3.9.0
python -m ensurepip --upgrade

# Or download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### **3. Package installation fails with Python 3.9.0:**
```cmd
# Try installing with --no-deps
pip install -r requirements.txt --no-deps

# Then install missing dependencies manually
pip install Django==4.2.27
pip install pillow==9.5.0  # Python 3.9 compatible version
```

#### **4. Virtual environment creation fails:**
```cmd
# Ensure Python 3.9.0 is being used
python --version

# If using Python 3.9 but command shows different:
# Windows: python -3.9 -m venv venv
# Mac/Linux: python3.9 -m venv venv
```

---

## 📊 **SYSTEM REQUIREMENTS - PYTHON 3.9.0 SPECIFIC**

### **Mandatory Requirements:**
- **✅ Python Version**: **3.9.0** (NOT 3.10, NOT 3.11, NOT 3.12, NOT 3.13)
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Memory**: 4GB RAM
- **Storage**: 500MB free space

### **Recommended Setup:**
- **Python**: 3.9.0 (exactly)
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Memory**: 8GB RAM or more
- **Storage**: 1GB free space

### **Why Python 3.9.0?**
- ✅ Tested and verified with Django 4.2.27
- ✅ Compatible with all 44+ packages in requirements.txt
- ✅ Stable and reliable for production
- ✅ Avoids Python 3.10+ breaking changes

---

## 📁 **AUTOMATED SCRIPTS (Windows) - Python 3.9.0 Compatible**

### **Setup & Launch Commands:**

| Command | Purpose | Python 3.9.0 Compatible |
|---------|---------|-------------------------|
| **`launch.bat`** | Complete setup & start server | ✅ Yes |
| **`setup.bat`** | Setup only (no server start) | ✅ Yes |
| **`start.bat`** | Start server only | ✅ Yes |
| **`quick_setup.bat`** | Fast minimal setup | ✅ Yes |

### **Maintenance Commands:**

| Command | Purpose | Python 3.9.0 Compatible |
|---------|---------|-------------------------|
| **`reset.bat`** | Reset everything | ✅ Yes |
| **`backup.bat`** | Create data backups | ✅ Yes |
| **`restore.bat`** | Restore from backup | ✅ Yes |
| **`update.bat`** | Update packages | ✅ Yes |

### **Administration Commands:**

| Command | Purpose | Python 3.9.0 Compatible |
|---------|---------|-------------------------|
| **`admin.bat`** | Create new admin user | ✅ Yes |
| **`check.bat`** | System diagnostics | ✅ Yes |
| **`runserver.bat`** | Just run server | ✅ Yes |

---

## 🌐 **ACCESSING THE SYSTEM**

### **After Successful Setup:**

#### **Web Interface:**
- **Main Application**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin
- **Default Port**: 8000 (change with `runserver 8001`)

#### **Login Credentials:**
- **Your Original Users**: All 6 users from your system are loaded
- **Admin Fallback**: admin / admin123 (if data file missing)
- **Test Users**: Created automatically if no data file

#### **User Roles:**
1. **👑 System Admin** - Full system access
2. **📊 Accounts Personnel** - Create/manage batches
3. **✅ Authorizer** - Approve/reject batches

---

## 🔄 **DEVELOPER WORKFLOW WITH PYTHON 3.9.0**

### **For Code Contributors:**

```bash
# 1. Install Python 3.9.0 first
# 2. Fork repository
# 3. Clone your fork
git clone https://github.com/YOUR-USERNAME/CRWB-EFT-System-v1.0.git

# 4. Create virtual environment with Python 3.9.0
python3.9 -m venv venv
source venv/bin/activate

# 5. Install requirements
pip install -r requirements.txt

# 6. Create feature branch
git checkout -b feature/new-feature

# 7. Make changes and test
python manage.py runserver

# 8. Export updated data (if database changed)
python manage.py dumpdata --indent 2 > eft_app/fixtures/all_data.json

# 9. Commit and push
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature

# 10. Create Pull Request on GitHub
```

### **Database Management:**

```bash
# Export current data
python manage.py dumpdata --indent 2 > backup.json

# Import data
python manage.py loaddata backup.json

# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Reset database (WARNING: deletes all data)
python manage.py flush
```

---

## 🔒 **SECURITY FEATURES**

### **Built-in Security:**
- ✅ Role-Based Access Control (RBAC)
- ✅ Password hashing with PBKDF2
- ✅ CSRF protection on all forms
- ✅ XSS prevention
- ✅ SQL injection protection
- ✅ Session management with timeout
- ✅ Login attempt limiting

### **Data Protection:**
- All passwords encrypted
- Audit trail for all user actions
- Data validation at application level
- Secure file handling
- Regular backup system

### **Compliance Features:**
- Complete audit logging
- User activity monitoring
- Data integrity checks
- Export validation
- Bank compliance standards

---

## 📈 **PERFORMANCE OPTIMIZATION**

### **For Better Performance:**

```bash
# 1. Collect static files
python manage.py collectstatic

# 2. Use production database (for deployment)
# Change to PostgreSQL or MySQL in settings.py

# 3. Enable caching
# Add cache configuration in settings.py

# 4. Optimize database
python manage.py dbshell
# Then run: ANALYZE;
```

### **Monitoring Tools:**
```bash
# Check system performance
check.bat

# View Django debug toolbar (when DEBUG=True)
# Install: pip install django-debug-toolbar

# Monitor database queries
python manage.py shell_plus --print-sql
```

---

## 🚀 **DEPLOYMENT GUIDE**

### **Development Deployment (Default):**
Already configured for local development. Just run:
```cmd
launch.bat
```

### **Production Deployment Steps:**

#### **1. Environment Preparation:**
```bash
# Clone repository
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0

# Create production environment with Python 3.9.0
python3.9 -m venv venv_prod
source venv_prod/bin/activate  # or venv_prod\Scripts\activate
```

#### **2. Configuration:**
Edit `crwb_eft/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
# Change database to PostgreSQL/MySQL
# Set up email configuration
# Configure static files for production
```

#### **3. Production Dependencies:**
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # For PostgreSQL
```

#### **4. Database Setup:**
```bash
python manage.py migrate
python manage.py loaddata eft_app/fixtures/all_data.json
python manage.py collectstatic --noinput
```

#### **5. Start Production Server:**
```bash
# Using Gunicorn
gunicorn crwb_eft.wsgi:application --bind 0.0.0.0:8000

# Using uWSGI
uwsgi --http :8000 --module crwb_eft.wsgi
```

#### **6. Web Server Configuration (Nginx):**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /path/to/CRWB-EFT-System-v1.0/static/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔄 **BACKUP & RECOVERY**

### **Regular Backups:**
```cmd
# Manual backup
backup.bat

# Scheduled backup (Windows Task Scheduler)
# Create task to run backup.bat daily

# Database export
python manage.py dumpdata --indent 2 > backup_%date%.json
```

### **Restore Procedure:**
```cmd
# 1. Stop server
# 2. Restore from backup
restore.bat

# Or manually:
python manage.py loaddata backup_file.json

# 3. Verify data
python manage.py shell -c "
from django.contrib.auth.models import User
print(f'Users restored: {User.objects.count()}')
"
```

### **Disaster Recovery:**
1. **Data Loss**: Use `restore.bat` with latest backup
2. **System Crash**: Run `reset.bat` then `launch.bat`
3. **Database Corruption**: Delete `db.sqlite3` and restore from backup

---

## 📞 **SUPPORT & MAINTENANCE**

### **Getting Help:**

#### **1. Self-Help:**
```cmd
# Run diagnostics
check.bat

# Check server logs
# Look at terminal output when running launch.bat

# Verify installation
python manage.py check
```

#### **2. Common Python 3.9.0 Solutions:**
- **Can't login**: Use `admin.bat` to create new admin
- **Server won't start**: Verify Python 3.9.0 is installed correctly
- **Data missing**: Run `restore.bat` with backup file
- **Package errors**: Check Python version is exactly 3.9.0

#### **3. Contact Support:**
- **GitHub Issues**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0/issues
- **Documentation**: This README file
- **System Logs**: Check terminal output for errors

### **Regular Maintenance:**

#### **Daily:**
```cmd
# Check system health
check.bat

# Create backup
backup.bat
```

#### **Weekly:**
```cmd
# Update packages
update.bat

# Clean up old backups
# Delete backup files older than 30 days
```

#### **Monthly:**
- Review audit logs
- Check disk space
- Update security settings
- Test restore procedure

---

## 📄 **LICENSE & COMPLIANCE**

### **License Information:**
- **Software**: Proprietary, all rights reserved
- **Usage**: Internal CRWB operations only
- **Modification**: Not permitted without authorization
- **Distribution**: Restricted to authorized personnel

### **Compliance Requirements:**
- Maintain complete audit trails
- Regular security assessments
- Data protection compliance
- User access monitoring
- Backup verification

### **Data Privacy:**
- All user data encrypted
- Access logs maintained
- Export controls in place
- Regular security updates

---

## 🎯 **QUICK REFERENCE**

### **Most Common Commands:**
```cmd
# First time setup
launch.bat

# Setup without starting server
setup.bat
start.bat

# Troubleshooting
reset.bat
check.bat

# Data management
backup.bat
restore.bat
```

### **Access URLs:**
- **Application**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **API Docs**: Included in application

### **Default Credentials:**
- **Admin**: admin / admin123 (if no data file)
- **Your Users**: All original users loaded from your system

---

## 🎉 **READY TO BEGIN?**

### **First: Install Python 3.9.0**
Download from: https://www.python.org/downloads/release/python-390/

### **Then choose your setup method:**

#### **Option 1: Automated Setup (Recommended)**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
launch.bat
```

#### **Option 2: Manual Setup**
Follow the **Manual Setup** section above for step-by-step instructions.

#### **Option 3: Quick Test**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
quick_setup.bat
```

**Your complete EFT payment system with all your original data will be ready in minutes!**

---

**System Version**: v1.0  
**Python Requirement**: 3.9.0 (exactly)  
**Last Updated**: January 2025  
**GitHub**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0  
**Support**: Check troubleshooting section or create GitHub issue