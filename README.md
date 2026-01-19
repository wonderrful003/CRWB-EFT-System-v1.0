# CRWB EFT System

Electronic Funds Transfer system for Central Region Water Board with RBM compliance.

## Quick Start

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/crwb-eft-system.git
cd crwb-eft-system

# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver