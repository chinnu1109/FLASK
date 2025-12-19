from sqlalchemy import create_engine, text

# Connect to MySQL server (no database selected yet) usually to 'sys' or just base url
# However, create_engine needs a db usually. We can connect to empty or 'mysql'.
# Using logic to connect without DB first to create it.
engine_server = create_engine(
    "mysql+pymysql://root:Sivasai%4012345@localhost:3306",
    echo=True,
    isolation_level="AUTOCOMMIT"
)

def init_db():
    with engine_server.connect() as conn:
        # Create Database
        conn.execute(text("CREATE DATABASE IF NOT EXISTS event_management"))
        print("Database 'event_management' checked/created.")
        
        # Use the database
        conn.execute(text("USE event_management"))
        
        # Create Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_name VARCHAR(255) NOT NULL,
                event_date VARCHAR(50), 
                venue VARCHAR(255),
                description TEXT,
                organizer VARCHAR(255),
                contact_email VARCHAR(255)
            )
        """))
        print("Table 'events' checked/created.")

if __name__ == "__main__":
    init_db()
