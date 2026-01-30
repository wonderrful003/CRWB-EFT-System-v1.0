import psycopg2

try:
    conn = psycopg2.connect(
        dbname='crwb_eft_system',
        user='eft_user',
        password='SecurePassword123!',
        host='localhost',
        port=5432
    )
    print('✅ PostgreSQL connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Failed: {e}')