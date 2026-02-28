"""Database utilities"""
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

"""Database manager for handling connections and sessions"""
class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self):
        self.settings = Settings()
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database engine and session"""
        try:
            self.engine = sa.create_engine(
                self.settings.DATABASE_URL,
                echo=self.settings.DEBUG
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()


# Models
class Article(Base):
    """Article model for storing scraped articles"""
    __tablename__ = "articles"
    
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255), nullable=False)
    url = sa.Column(sa.String(512), nullable=False, unique=True)
    category = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text)
    published_date = sa.Column(sa.DateTime)
    scraped_date = sa.Column(sa.DateTime, default=sa.func.now())
    sent = sa.Column(sa.Boolean, default=False)
