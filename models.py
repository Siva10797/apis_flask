from sqlalchemy import Column, Integer, String, DateTime,BigInteger,TIMESTAMP,JSON,CheckConstraint,ForeignKey,Text,Boolean,func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    enrolled = Column(String(50), nullable=True)
    role_id = Column(Integer, ForeignKey("user_roles.role_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("UserRole", back_populates="users")
    application_users = relationship("ApplicationUser", back_populates="user")  
    
    
class UserRole(Base):
    __tablename__ = 'user_roles'

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)

    
    users = relationship("User", back_populates="role")


#---------------Application and ApplicationUser Models----------------
    
class Application(Base):
    __tablename__ = 'applications'

    application_id = Column(Integer, primary_key=True, index=True)
    application_name = Column(String(100), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    configurations = relationship("Configurations", back_populates="application", cascade="all, delete-orphan")
    application_users = relationship("ApplicationUser", back_populates="application", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Application(name={self.application_name})>"


# class ApplicationUser(Base):
#     __tablename__ = 'application_users'

#     application_id = Column(Integer, ForeignKey('applications.application_id'), nullable=False)
#     user_id = Column(Integer, nullable=False)

#     # Corrected column name to match database
#     role_in_app = Column(String(50))  

#     assigned_at = Column(DateTime, default=datetime.utcnow)

#     application = relationship("Application", back_populates="application_users")

class ApplicationUser(Base):
    __tablename__ = 'application_users'

    application_id = Column(Integer, ForeignKey("applications.application_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_in_app = Column(String(50), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="application_users")
    application = relationship("Application", back_populates="application_users")

    __table_args__ = (
        PrimaryKeyConstraint('application_id', 'user_id'),
    )



#---------------Configurations Model----------------

class Configurations(Base):
    __tablename__ = 'configurations'

    config_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.application_id'))
    document_name = Column(String(100), nullable=False)
    document_type = Column(String(255), nullable=False)
    document_path = Column(String(255), nullable=False)
    version = Column(String(20), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="configurations")

    def __repr__(self):
        return f"<Configurations(document_name={self.document_name}, version={self.version})>"
    
    


#---------------Customer and CustomerDepartment Models----------------

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class CustomerDepartment(Base):
    __tablename__ = 'customer_departments'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    department_id = Column(Integer)


#---------------Department and DepartmentApplication Models----------------

class DepartmentApplication(Base):
    __tablename__ = 'department_applications'
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer)
    application_id = Column(Integer, ForeignKey('applications.application_id'))
    

class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
#---------------GitConnection and JIRAConnection Models----------------

class GitConnection(Base):
    __tablename__ = 'git_connections'

    git_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.application_id', ondelete="CASCADE"), nullable=False)
    repo_url = Column(String, nullable=False)
    auth_type = Column(String(10), nullable=False)  # Must be HTTPS or SSH
    username = Column(String(100))  # For HTTPS
    access_token = Column(Text)     # Encrypted in prod
    ssh_key = Column(Text)          # Encrypted in prod
    ssh_passphrase = Column(Text)   # Optional
    default_branch = Column(String(50), default='main')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = relationship("Application")
    
    
class JIRAConnection(Base):
    __tablename__ = 'jira_connections'

    jira_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.application_id', ondelete='CASCADE'), nullable=False)
    jira_base_url = Column(Text, nullable=False)
    project_key = Column(String(50), nullable=False)
    auth_type = Column(String(20), default='API_TOKEN')  # 'API_TOKEN' or 'OAUTH'
    jira_email = Column(String(150))
    jira_api_token = Column(Text)  # For API_TOKEN
    oauth_client_id = Column(Text)  # Optional for OAuth
    oauth_client_secret = Column(Text)  # Optional for OAuth
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = relationship("Application")



#---------------DiscoveryQuerySession and DiscoveryQueryMessage Models----------------

# class DiscoveryQuerySession(Base):
#     __tablename__ = "DiscoveryQuerySession"

#     Id = Column(Integer, primary_key=True, autoincrement=True)
#     UserId = Column(Integer, nullable=False)
#     Title = Column(Text, nullable=False)
#     IsFavorite = Column(Boolean, nullable=False, default=False)
#     CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
#     # Add this line
#     ApplicationId = Column(Integer, ForeignKey('applications.application_id'), nullable=False)
    
    
class DiscoveryQuerySession(Base):
    __tablename__ = 'DiscoveryQuerySession'

    Id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, ForeignKey("users.user_id"))
    Title = Column(String)
    IsFavorite = Column(Boolean, default=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
    


class DiscoveryQueryMessage(Base):
    __tablename__ = 'DiscoveryQueryMessage'

    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, nullable=False)
    Sender = Column(Text, nullable=False)
    Content = Column(Text, nullable=False)
    Metadata = Column(JSON)
    CreatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("Sender IN ('user', 'assistant')", name='sender_check'),
    )