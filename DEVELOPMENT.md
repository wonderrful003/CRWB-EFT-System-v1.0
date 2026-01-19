markdown
# Development Guide

## Git Workflow

### 1. Always Start Fresh
```bash
# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature/feature-name
2. Make Changes
bash
# Add files
git add .

# Commit
git commit -m "Description of changes"
3. Push Changes
bash
git push origin feature/feature-name
4. Create Pull Request on GitHub
Database Migrations
bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Check migration status
python manage.py showmigrations
Testing
bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test eft_app
Code Standards
Follow Django coding style

Use meaningful variable names

Add comments for complex logic

Update requirements.txt after new installations

text

## **Step 18: Final Verification**

```bash
# Check everything is committed
git status

# Should show: "nothing to commit, working tree clean"

# Check git log
git log --oneline --graph

# Check remote
git remote -v
# Should show origin pointing to your GitHub repo

# Test pushing
git push
# Should show "Everything up-to-date"
Step 19: Test Clone (Optional but Recommended)
Test that others can clone your repository properly:

bash
# Go to a different directory
cd C:\Users\dell\Desktop

# Create test clone
git clone https://github.com/wonderrful003/CRWB-EFT-System-v1.0.git test-clone

cd test-clone

# Verify structure
dir /a

# Should see all files but NOT venv folder