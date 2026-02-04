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

## 🔧 **MANUAL SETUP (Step-by-Step)**

### **If the automated scripts don't work, follow these manual steps:**

### **Step 1: Clone Repository**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
```

### **Step 2: Create Virtual Environment**
```cmd
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Requirements**
```cmd
pip install -r requirements.txt

# If requirements.txt fails, install Django only:
pip install Django==4.2.27
```

### **Step 4: Setup Database**
```cmd
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### **Step 5: Load Your Data**
```cmd
# Load your complete original system
python manage.py loaddata eft_app/fixtures/all_data.json

# Verify data was loaded
python manage.py shell -c "
from django.contrib.auth.models import User
print(f'Loaded {User.objects.count()} users from your system')
"
```

### **Step 6: Create Admin User (Optional)**
```cmd
# Only needed if data file is missing
python manage.py createsuperuser
# Follow prompts: admin, admin@crwb.gov.mw, admin123
```

### **Step 7: Start Server**
```cmd
python manage.py runserver
```

### **Step 8: Access System**
- **🌐 Application**: http://127.0.0.1:8000
- **🔧 Admin Panel**: http://127.0.0.1:8000/admin
- **👤 Login**: Use your original users or admin/admin123

---

## 📁 **AUTOMATED SCRIPTS (Windows)**

### **Setup & Launch Commands:**

| Command | Purpose | Best For |
|---------|---------|----------|
| **`launch.bat`** | Complete setup & start server | First-time users |
| **`setup.bat`** | Setup only (no server start) | Separate setup & run |
| **`start.bat`** | Start server only | After setup |
| **`quick_setup.bat`** | Fast minimal setup | Quick testing |

### **Maintenance Commands:**

| Command | Purpose |
|---------|---------|
| **`reset.bat`** | Reset everything (clean slate) |
| **`backup.bat`** | Create data backups |
| **`restore.bat`** | Restore from backup |
| **`update.bat`** | Update all packages |

### **Administration Commands:**

| Command | Purpose |
|---------|---------|
| **`admin.bat`** | Create new admin user |
| **`check.bat`** | System diagnostics |
| **`runserver.bat`** | Just run server |

---

## 🛠️ **TROUBLESHOOTING**

### **Common Installation Issues:**

#### **1. "Python not found" Error:**
```cmd
# Check Python installation
python --version

# If not installed:
# 1. Download from https://python.org
# 2. During installation, CHECK "Add Python to PATH"
# 3. Restart Command Prompt and try again
```

#### **2. "pip install" Fails:**
```cmd
# Try upgrading pip first
python -m pip install --upgrade pip

# Install Django only
pip install Django==4.2.27

# Or install from requirements without dependencies
pip install -r requirements.txt --no-deps
```

#### **3. Database Errors:**
```cmd
# Delete corrupted database
del db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Reload data
python manage.py loaddata eft_app/fixtures/all_data.json
```

#### **4. Port 8000 Already in Use:**
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID [PID] /F

# Or use different port
python manage.py runserver 8001
```

#### **5. Virtual Environment Issues:**
```cmd
# Delete and recreate
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
```

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

## 🔄 **DEVELOPER WORKFLOW**

### **For Code Contributors:**

```bash
# 1. Fork repository
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/CRWB-EFT-System-v1.0.git

# 3. Create feature branch
git checkout -b feature/new-feature

# 4. Make changes and test
launch.bat

# 5. Export updated data (if database changed)
python manage.py dumpdata --indent 2 > eft_app/fixtures/all_data.json

# 6. Commit and push
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature

# 7. Create Pull Request on GitHub
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

## 📊 **SYSTEM REQUIREMENTS**

### **Minimum Requirements:**
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python Version**: 3.9 or higher
- **Memory**: 4GB RAM
- **Storage**: 500MB free space
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### **Recommended Specifications:**
- **Operating System**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python Version**: 3.11 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 1GB free space
- **Browser**: Latest version of Chrome/Firefox

### **Network Requirements:**
- Localhost access (for development)
- Port 8000 open (or alternative port)
- No external dependencies required

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

# Create production environment
python -m venv venv_prod
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

#### **2. Common Solutions:**
- **Can't login**: Use `admin.bat` to create new admin
- **Server won't start**: Run `reset.bat` then `launch.bat`
- **Data missing**: Run `restore.bat` with backup file
- **Slow performance**: See Performance Optimization section

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

### **Option 1: Automated Setup (Recommended)**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
launch.bat
```

### **Option 2: Manual Setup**
Follow the **Manual Setup** section above for step-by-step instructions.

### **Option 3: Quick Test**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
quick_setup.bat
```

**Your complete EFT payment system with all your original data will be ready in minutes!**

---

**System Version**: v1.0  
**Last Updated**: January 2025  
**GitHub**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0  
**Support**: Check troubleshooting section or create GitHub issue