import psycopg2

try:
    from config.settings import DATABASE, USER, PASSWORD, HOST, PORT
except ImportError:
    print("Warning: settings.py not found, PLEASE COPY settings_example.py TO settings.py")
    from config.settings_example import DATABASE, USER, PASSWORD, HOST, PORT

conn = psycopg2.connect(
    database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
)
cursor = conn.cursor()
