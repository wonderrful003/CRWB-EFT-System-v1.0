# CRWB EFT System v1.0 Documentation

## Electronic Funds Transfer System with RBM Compliance

### Overview
The CRWB EFT System is a Django-based web application designed for electronic payment processing with banking system compliance requirements. It streamlines payment batch creation, approval workflows, and generates compliant payment files for banking systems.

### Technology Stack
- **Backend Framework**: Django 4.2
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite3 (Development)
- **Authentication**: Django Auth with custom permission system
- **File Formats**: TXT and CSV generation

## Table of Contents

1. [Installation Guide](#installation-guide)
2. [System Features](#system-features)
3. [User Roles and Permissions](#user-roles-and-permissions)
4. [Usage Instructions](#usage-instructions)
5. [Development Guide](#development-guide)
6. [Database Schema](#database-schema)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)
9. [Deployment Guidelines](#deployment-guidelines)
10. [Contributing](#contributing)

---

## Installation Guide

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git version control
- Modern web browser

### Step 1: Clone Repository
```bash
git clone [repository-url]
cd project-directory
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
1. Copy environment configuration template
2. Update settings as needed
3. Set up database connection

### Step 5: Initialize Database
```bash
# Apply database migrations
python manage.py migrate

# Load initial data
python manage.py seed_data

# Create admin user
python manage.py createsuperuser
```

### Step 6: Start Development Server
```bash
python manage.py runserver
```
Access the application at: `http://127.0.0.1:8000`

---

## System Features

### Authentication & Security
- Role-based access control system
- Secure password hashing
- Session management with timeout
- Audit trail for all system activities

### Master Data Management
- **Banks**: Manage banking institutions with identification codes
- **Suppliers**: Maintain vendor and beneficiary information
- **Zones**: Organize operational areas
- **Schemes**: Payment categorization and tracking
- **Accounts**: Debit account management

### Payment Processing
- Batch-based transaction processing
- Real-time amount calculation
- Multi-currency support
- Transaction validation

### Approval Workflow
- Multi-level approval system
- Review and approval tracking
- Audit logs for compliance
- Notification system

### File Generation
- Compliant file format generation
- Automatic sequence numbering
- Format validation
- Batch export functionality

### Reporting & Analytics
- Role-specific dashboards
- Transaction statistics
- Activity monitoring
- Batch status tracking

---

## User Roles and Permissions

### System Administrator
**Access Level**: Full system access
**Responsibilities**:
- User management and role assignment
- System configuration
- Master data maintenance
- System monitoring and troubleshooting
- Access to administrative functions

### Accounts Personnel
**Access Level**: Transaction processing
**Responsibilities**:
- Create and manage payment batches
- Add and edit transaction details
- Submit batches for approval
- View transaction history
- Generate preliminary reports

### Authorizer
**Access Level**: Approval and review
**Responsibilities**:
- Review pending payment batches
- Approve or reject submissions
- View approval history
- Export approved files
- Cannot modify transaction details

---

## Usage Instructions

### Creating Payment Batches
1. Log in with Accounts Personnel credentials
2. Navigate to "Create Batch" section
3. Enter batch identification details
4. Add individual transactions
5. Review batch summary
6. Submit for approval

### Transaction Entry
Each transaction requires:
- Account information
- Beneficiary details
- Payment scheme
- Transaction amount
- Reference information
- Description/narration

### Approval Process
1. Batch submitted by Accounts Personnel
2. Appears in Authorizer's pending queue
3. Authorizer reviews transaction details
4. Authorizer approves or rejects with comments
5. Status updates accordingly

### File Export Process
1. Navigate to approved batches section
2. Select batch for export
3. Choose file format (TXT/CSV)
4. Download generated file
5. File ready for banking system upload

---

## Development Guide

### Project Structure
```
project-root/
│
├── project_name/          # Django project configuration
│   ├── settings.py       # Application settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
│
├── app_name/             # Main application
│   ├── models.py        # Database models
│   ├── views.py         # Business logic
│   ├── forms.py         # Form definitions
│   ├── urls.py          # Application URLs
│   ├── admin.py         # Admin interface
│   └── templates/       # HTML templates
│
├── templates/            # Base templates
├── static/              # Static assets
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

### Setting Up Development Environment
```bash
# Clone repository
git clone [repository-url]

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run complete test suite
python manage.py test

# Run specific application tests
python manage.py test app_name

# Run tests with coverage
coverage run manage.py test
coverage report
```

### Code Standards
- Follow Django coding style guidelines
- Use meaningful variable and function names
- Add comments for complex business logic
- Maintain consistent indentation (4 spaces)
- Update documentation with code changes

### Database Migrations
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Create data migrations
python manage.py makemigrations --empty app_name
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/feature-description

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Description of changes made"

# Push to remote repository
git push origin feature/feature-description

# Create pull request for code review
```

---

## Database Schema

### Core Models

#### Batch Model
- **Purpose**: Stores payment batch information
- **Fields**: Batch identifier, creation date, status, totals
- **Relationships**: Links to transactions and users

#### Transaction Model
- **Purpose**: Individual payment records
- **Fields**: Amount, reference, narration, sequence
- **Relationships**: Links to batches, suppliers, accounts

#### Supplier Model
- **Purpose**: Vendor and beneficiary information
- **Fields**: Supplier code, name, bank details
- **Relationships**: Links to transactions and banks

#### User Management
- **Purpose**: System user accounts and permissions
- **Fields**: Username, email, role assignments
- **Relationships**: Links to created batches and approvals

### Database Operations
```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json

# Database shell access
python manage.py dbshell

# Reset database (development only)
python manage.py flush
```

---

## API Documentation

### Available Endpoints

#### Supplier Information
```
GET /api/supplier/{id}/details/
```
**Response Format:**
```json
{
    "bank_name": "Bank Name",
    "bank_code": "BANKCODE",
    "account_number": "1234567890",
    "account_name": "Account Holder Name"
}
```

#### Scheme Details
```
GET /api/scheme/{id}/details/
```
**Response Format:**
```json
{
    "scheme_code": "SCHEME001",
    "scheme_name": "Scheme Description",
    "zone_code": "ZONE01"
}
```

### Authentication
All API endpoints require user authentication. The system uses session-based authentication.

### Error Responses
Common HTTP status codes:
- `200`: Successful request
- `400`: Bad request
- `401`: Unauthorized access
- `404`: Resource not found
- `500`: Internal server error

---

## Troubleshooting

### Common Issues and Solutions

#### Database Connection Problems
**Symptoms**: Migration errors, database access failures
**Solutions**:
- Verify database file permissions
- Check database path in settings
- Ensure sufficient disk space
- Run database integrity checks

#### Static File Issues
**Symptoms**: Missing CSS/JS, broken page styling
**Solutions**:
```bash
# Collect static files
python manage.py collectstatic

# Check static file configuration
# Verify file permissions
# Clear browser cache
```

#### Permission Errors
**Symptoms**: Access denied, unauthorized actions
**Solutions**:
- Verify user role assignments
- Check group permissions
- Review access control settings
- Clear user sessions if needed

#### Server Configuration
**Symptoms**: Port conflicts, server won't start
**Solutions**:
```bash
# Check port availability
netstat -ano | findstr :8000

# Use alternative port
python manage.py runserver 8001

# Check firewall settings
# Verify Python installation
```

### Logging and Debugging
- Enable debug mode in development
- Check Django server logs
- Review application logs
- Use Django debug toolbar
- Monitor system performance

### Performance Optimization
- Implement database indexing
- Use query optimization
- Cache frequently accessed data
- Optimize static file delivery
- Monitor memory usage

---

## Deployment Guidelines

### Production Checklist

#### Environment Configuration
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set up production database
- Configure static and media files
- Set up email services

#### Security Settings
- Generate strong `SECRET_KEY`
- Enable HTTPS/SSL
- Configure security middleware
- Set up proper file permissions
- Implement rate limiting

#### Database Setup
- Use production database (PostgreSQL/MySQL)
- Configure database backups
- Set up replication if needed
- Implement connection pooling

#### Web Server Configuration
- Use production WSGI server (Gunicorn/uWSGI)
- Configure reverse proxy (Nginx/Apache)
- Set up SSL certificates
- Configure load balancing if needed

### Deployment Steps
1. **Prepare Environment**
   ```bash
   # Clone repository
   git clone [repository-url]
   
   # Set up virtual environment
   python -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Settings**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit production settings
   nano .env
   ```

3. **Initialize Database**
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Create admin user
   python manage.py createsuperuser
   ```

4. **Set Up Web Server**
   ```bash
   # Configure Gunicorn
   gunicorn project_name.wsgi:application --bind 0.0.0.0:8000
   
   # Configure Nginx
   # Set up SSL certificates
   # Configure domain names
   ```

### Monitoring and Maintenance
- Set up error monitoring
- Configure log rotation
- Schedule regular backups
- Monitor system performance
- Update dependencies regularly
- Security patch management

### Backup Strategy
- Daily database backups
- Weekly full system backups
- Off-site backup storage
- Regular backup testing
- Disaster recovery planning

---

## Contributing

### Development Process
1. **Fork Repository**: Create personal fork
2. **Create Branch**: Feature or bugfix branch
3. **Make Changes**: Implement features/fixes
4. **Add Tests**: Include test coverage
5. **Submit PR**: Pull request with description

### Code Review Guidelines
- Follow existing code patterns
- Include appropriate tests
- Update documentation
- Address security considerations
- Consider performance impacts

### Testing Requirements
- Unit tests for new functionality
- Integration tests for workflows
- Security testing for new features
- Performance testing for changes

### Documentation Updates
- Update README for new features
- Add API documentation
- Update deployment guides
- Include usage examples

### Issue Reporting
- Use clear, descriptive titles
- Include steps to reproduce
- Add relevant logs/screenshots
- Specify environment details
- Suggest possible solutions

---

## Support and Maintenance

### Getting Help
- Check documentation first
- Review troubleshooting section
- Search existing issues
- Contact development team

### Regular Maintenance Tasks
- Security updates
- Dependency updates
- Database optimization
- Log file management
- Backup verification

### Update Procedures
- Test updates in staging
- Schedule maintenance windows
- Communicate changes to users
- Monitor after updates
- Have rollback plan ready

### Performance Monitoring
- Regular system health checks
- Monitor response times
- Track resource usage
- User feedback collection
- Error rate monitoring

---

## License and Copyright

### Usage Rights
This software is proprietary and protected by copyright. All rights reserved.

### Restrictions
- No redistribution without permission
- No modification of source code
- No reverse engineering
- Commercial use requires license agreement

### Compliance Requirements
- Follow organizational policies
- Maintain audit trails
- Protect sensitive data
- Regular security assessments

---

## Acknowledgments

- Django framework and community
- Bootstrap development team
- All contributors and testers
- Banking system compliance teams

---

**Documentation Version**: 1.0  
**Last Updated**: [Current Date]  
**System Version**: CRWB EFT System v1.0  

For additional support or to report issues, please contact the development team or refer to the internal support channels.