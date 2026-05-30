from database import engine, Base
from models import Like,User, Movie, Review 

def create_tables():
    print("⏳ Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
