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

---

## ⚠️ **MANDATORY REQUIREMENT: PYTHON 3.9.0**

### **🔴 YOU MUST INSTALL PYTHON 3.9.0 FIRST!**

#### **Windows Download Link (64-bit):**
**📥 Download: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe**

#### **Installation Steps (CRITICAL):**
1. **Download** the installer from the link above
2. **Run** `python-3.9.0-amd64.exe`
3. **CHECK** ✅ "Add Python 3.9 to PATH" (MUST DO THIS!)
4. **Click** "Install Now"
5. **Restart** Command Prompt after installation
6. **Verify** with: `python --version` (should show "Python 3.9.0")

#### **If Python 3.9.0 is already installed but not detected:**
```cmd
# Check your Python version
python --version

# If it's NOT 3.9.0, you must:
# 1. Uninstall current Python
# 2. Install Python 3.9.0 from the link above
# 3. Follow the installation steps exactly
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

### **Step 1: Install Python 3.9.0**
```cmd
# Download and install from:
# https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
# MUST check "Add Python 3.9 to PATH"
```

### **Step 2: Verify Python 3.9.0**
```cmd
python --version
# MUST show: Python 3.9.0
# If not, restart Command Prompt or reinstall
```

### **Step 3: Clone Repository**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
```

### **Step 4: Create Virtual Environment**
```cmd
python -m venv venv
venv\Scripts\activate
```

### **Step 5: Install Requirements**
```cmd
pip install -r requirements.txt
```

### **Step 6: Setup Database**
```cmd
python manage.py makemigrations
python manage.py migrate
```

### **Step 7: Load Your Data**
```cmd
python manage.py loaddata eft_app/fixtures/all_data.json
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

### **Problem 1: "Python not found" after installing 3.9.0**
```cmd
# Solution:
# 1. Re-run the installer: python-3.9.0-amd64.exe
# 2. Choose "Modify"
# 3. Ensure "Add Python to environment variables" is checked
# 4. Restart Command Prompt
```

### **Problem 2: Wrong Python version shows**
```cmd
# Check all Python installations
where python

# If multiple versions exist:
# 1. Uninstall all other Python versions
# 2. Reinstall ONLY Python 3.9.0
# 3. Restart computer
```

### **Problem 3: Virtual environment creation fails**
```cmd
# Ensure Python 3.9.0 is in PATH
python --version

# If still fails, use full path:
"C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python39\python.exe" -m venv venv
```

---

## 📊 **SYSTEM REQUIREMENTS**

### **Mandatory:**
- **✅ Python Version**: **3.9.0 exactly** (download link above)
- **Operating System**: Windows 10/11 (64-bit)
- **Memory**: 4GB RAM minimum
- **Storage**: 500MB free space

### **Download Links:**
- **Python 3.9.0 (64-bit)**: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
- **Git (for cloning)**: https://git-scm.com/download/win

### **Why Python 3.9.0?**
- ✅ Tested and verified with all dependencies
- ✅ Stable and reliable for production
- ✅ Avoids Python 3.10+ compatibility issues
- ✅ Required for banking system integration

---

## 📁 **AUTOMATED SCRIPTS (Windows)**

### **Main Commands:**

| Command | Purpose | Python 3.9.0 Required |
|---------|---------|------------------------|
| **`launch.bat`** | Complete setup & start server | ✅ Yes |
| **`setup.bat`** | Setup only | ✅ Yes |
| **`start.bat`** | Start server only | ✅ Yes |
| **`python_check.bat`** | Verify Python 3.9.0 | ✅ Yes |

### **Maintenance Commands:**

| Command | Purpose |
|---------|---------|
| **`reset.bat`** | Reset everything |
| **`backup.bat`** | Create data backups |
| **`restore.bat`** | Restore from backup |
| **`check.bat`** | System diagnostics |

---

## 🌐 **ACCESSING THE SYSTEM**

### **After Successful Setup:**
- **🌐 Main Application**: http://127.0.0.1:8000
- **🔧 Admin Panel**: http://127.0.0.1:8000/admin
- **👤 Your Users**: All 6 original users loaded
- **🔑 Admin Fallback**: admin / admin123

### **User Roles:**
1. **👑 System Admin** - Full system access
2. **📊 Accounts Personnel** - Create/manage batches
3. **✅ Authorizer** - Approve/reject batches

---

## 🔒 **SECURITY FEATURES**

### **Built-in Security:**
- ✅ Role-Based Access Control (RBAC)
- ✅ Password hashing with PBKDF2
- ✅ CSRF protection on all forms
- ✅ SQL injection protection
- ✅ Complete audit logging

### **Data Protection:**
- All passwords encrypted
- Audit trail for all user actions
- Data validation at all levels
- Regular backup system

---

## 🎯 **QUICK REFERENCE**

### **Most Common Commands:**
```cmd
# First: Install Python 3.9.0 from:
# https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe

# Then run:
launch.bat

# Or if setup done:
start.bat

# Check Python version:
python_check.bat
```

### **Troubleshooting:**
1. **Python wrong version?** → Reinstall from link above
2. **Setup fails?** → Run `reset.bat` then `launch.bat`
3. **Can't login?** → Use `admin.bat` to create admin

---

## 🎉 **READY TO BEGIN?**

### **📥 STEP 1: Install Python 3.9.0**
**Download: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe**

### **🚀 STEP 2: Clone and Run**
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
launch.bat
```

### **Or Use Automated Setup:**
1. **Download** Python 3.9.0 from the link above
2. **Install** with "Add to PATH" checked
3. **Restart** Command Prompt
4. **Run** these commands:
```cmd
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git
cd CRWB-EFT-System-v1.0
launch.bat
```

**Your complete EFT payment system will be ready in minutes!**

---

## 📞 **SUPPORT**

### **Common Issues & Solutions:**
1. **Python not 3.9.0?** → Download from link above
2. **Installation fails?** → Run `python_check.bat` first
3. **Server won't start?** → Run `reset.bat` then `launch.bat`

### **Getting Help:**
- **GitHub Issues**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0/issues
- **Python 3.9.0 Download**: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe

---

**System Version**: v1.0  
**Python Requirement**: **3.9.0 exactly**  
**Download Link**: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe  
**GitHub**: https://github.com/wonderrful003/CRWB-EFT-System-v1.0  
**Last Updated**: February 2026