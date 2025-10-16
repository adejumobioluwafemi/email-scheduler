import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        self.connection_string = self._get_connection_string()

    def _get_connection_string(self):
        """
        Get database connection string from environment variable
        """

        # remote
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
        
        # local
        return (
            f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
            f"{os.getenv('DB_PASSQORD', 'Password@123')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '5432')}/"
            f"{os.getenv('DB_NAME', 'emailschedulerdb')}"
        )
    
    def get_connection(self):
        """
        get db connection with retry logic
        """

        try: 
            conn=psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def init_db(self):
        """
        Initialise db tables
        """
        conn = self.get_connection()

        try:
            with conn.cursor() as cursor:
                # schedule emails table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scheduled_emails (
                        id SERIAL PRIMARY KEY,
                        job_id TEXT UNIQUE NOT NULL,
                        recipient_name TEXT NOT NULL,
                        recipient_email TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        body TEXT NOT NULL,
                        scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
                        status TEXT DEFAULT 'scheduled',
                        smtp_config JSONB NOT NULL,
                        attachments JSONB DEFAULT '[]',
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        sent_at TIMESTAMP WITH TIME ZONE,
                        error_message TEXT,
                        user_id TEXT DEFAULT 'default_user',
                        retry_count INTEGER DEFAULT 0
                    )       
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_scheduled_status_time 
                    ON scheduled_emails(status, scheduled_time)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_scheduled_user 
                    ON scheduled_emails(user_id, scheduled_time)
                ''')
            conn.commit()
            logger.info("Database initialised successfully")

        except Exception as e:
            conn.rollback()
            logger.error(f"Database initialization failed: {e}")
            raise
        finally:
            conn.close()

# Global database instance
db = DatabaseManager()
                
    