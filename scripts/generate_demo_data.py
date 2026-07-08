from backend.database.session import SessionLocal
from backend.services.demo_data_service import DemoDataService

db = SessionLocal()

try:
    service = DemoDataService(db)

    service.generate_demo_data()

    print("Demo data generated successfully.")

finally:
    db.close()