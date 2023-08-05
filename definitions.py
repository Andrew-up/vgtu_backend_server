import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
DATABASE_DIR = os.path.join(ROOT_DIR, "data_base/db.db")
RELEASE_DIR = os.path.join(ROOT_DIR, "Release")
LOG_DIR = os.path.join(ROOT_DIR, 'logging_files')
SECRET_KEY = 'hFGHFEFyr67ggghhPJhdfh123dd'