from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from config import engine, SessionLocal  

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))  

class LoginHistory(Base):
    __tablename__ = "login_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    login_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))  
    ip_address = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)  




