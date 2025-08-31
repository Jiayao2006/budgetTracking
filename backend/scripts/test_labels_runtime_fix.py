from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os, sys, pathlib

# Ensure backend root on path
backend_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_root))

# Use local sqlite for smoke test
url = os.getenv('DATABASE_URL', 'sqlite:///./budget.db')
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql://')
engine = create_engine(url, connect_args={'check_same_thread': False} if url.startswith('sqlite') else {})
Session = sessionmaker(bind=engine)

# Mimic ensure_label_column from labels router
from app.models import Base
Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    # Drop label column if exists (only works for sqlite variant by recreating not trivial) - skip for simplicity
    pass

from app.routers.labels import ensure_label_column

session = Session()
ensure_label_column(session)
print('ensure_label_column executed without error')
