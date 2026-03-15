import sys
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    from app.database import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash
except ImportError as e:
    logging.error(f"Import failed: {e}")
    sys.exit(1)

def seed():
    try:
        db = SessionLocal()
        users_to_seed = [
            {
                "name": "System Admin",
                "email": "admin@example.com",
                "password": "admin123",
                "role": "Admin"
            },
            {
                "name": "System Director",
                "email": "director@example.com",
                "password": "director123",
                "role": "Director"
            },
            {
                "name": "Dam Operator",
                "email": "operator@example.com",
                "password": "operator123",
                "role": "Operator"
            },
            {
                "name": "Agricultural Officer",
                "email": "officer@example.com",
                "password": "officer123",
                "role": "Officer"
            }
        ]

        for u in users_to_seed:
            user = db.query(User).filter(User.email == u["email"]).first()
            if not user:
                logging.info(f"Creating {u['role']} user: {u['email']}")
                user = User(
                    email=u["email"],
                    password_hash=get_password_hash(u["password"]),
                )
                db.add(user)
            
            # Always update these fields to ensure latest state
            user.name = u["name"]
            user.role = u["role"]
            user.status = 'active'
            user.mfa_enabled = (u["role"] == "Director")
            if u["role"] == "Director":
                user.mfa_secret = "JBSWY3DPEHPK3PXP"
            
            logging.info(f"✅ {u['role']} ({u['email']}) synchronized.")
        
        db.commit()
    except Exception as e:
        logging.error(f"Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
