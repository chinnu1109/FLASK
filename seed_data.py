from sqlalchemy import create_engine, text

# Connect to the database "event_management"
engine = create_engine(
    "mysql+pymysql://root:Sivasai%4012345@localhost:3306/event_management",
    echo=True,
    isolation_level="AUTOCOMMIT"
)

def seed_data():
    with engine.connect() as conn:
        print("Inserting sample data...")
        
        # Check if table is empty to avoid duplicates (optional, but good practice)
        result = conn.execute(text("SELECT COUNT(*) FROM events"))
        count = result.scalar()
        if count > 0:
            print(f"Table already has {count} rows. Skipping seed.")
            return

        # Insert data
        conn.execute(text("""
            INSERT INTO events (event_name, event_date, venue, description, organizer, contact_email)
            VALUES 
            ('Techriya', '2024-03-15', 'Convention Center', 'The latest in technology innovations.', 'Tech Events LLC', 'info@techexpo.com'),
            ('Music Festival', '2024-05-20', 'City Park', 'A day of live music and entertainment.', 'Music Events Inc', 'info@musicfest.com'),
            ('Health Seminar', '2024-06-10', 'Wellness Center', 'Learn about leading a healthy lifestyle.', 'Wellness Foundation', 'info@healthseminar.org')
        """))
        print("Sample data inserted successfully.")

if __name__ == "__main__":
    seed_data()
