from app.database import SessionLocal, engine
from app.models import User, Base
from app.auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)
print('Tables created!')

# Create admin
db = SessionLocal()
try:
    existing = db.query(User).filter(User.email == 'admin@budgettracker.com').first()
    if existing:
        print('Admin already exists')
    else:
        admin = User(
            email='admin@budgettracker.com',
            full_name='System Administrator',
            hashed_password=get_password_hash('admin123'),
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print('✅ Admin created successfully!')
        print('📧 Email: admin@budgettracker.com')
        print('🔑 Password: admin123')
finally:
    db.close()
