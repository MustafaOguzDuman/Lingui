import os


def set_values():
    os.environ['URL'] = 'lingui-db.cfedbgvglaar.eu-central-1.rds.amazonaws.com'
    os.environ['USERNAME'] = 'postgres'
    os.environ['PASSWORD'] = 'lingui123'
    os.environ['DATABASE_NAME'] = 'lingui'