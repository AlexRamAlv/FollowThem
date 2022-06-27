from sqlalchemy import ForeignKey, Column, Integer, DateTime, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from app.models.pydantic_models import Received

Base = declarative_base()

# class Actions:


class Administrator(Base):
    __tablename__ = "administrators"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(100), nullable=False)
    last_name = Column("last_name", String(100), nullable=False)
    password_hash = Column("password_hash", String(256), nullable=True)
    creation_date = Column("creation_date", DateTime(), nullable=False)
    last_seen = Column("last_seen", DateTime(), nullable=True)
    update_date = Column("update_date", DateTime(), nullable=True)

    def __repr__(self) -> str:
        return "Admin(name=%s, last_name= %s)" % (self.name, self.last_name)

    @property
    def password(self):
        raise AttributeError("This is not an readable property!")

    @password.setter
    def password(self, password):
        self.password_hash = f"hashed-password: {password}"


class Provider(Base):
    __tablename__ = "providers"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    created_by_id = Column(
        "created_by_id", ForeignKey("administrators.id"), nullable=False
    )
    updated_by_id = Column(
        "updated_by_id", ForeignKey("administrators.id"), nullable=True
    )
    name = Column("name", String(100), nullable=False)
    creation_date = Column("creation_date", DateTime(), nullable=False)
    update_date = Column("update_date", DateTime(), nullable=True)
    requests = relationship(
        "Request", secondary="request_providers", back_populates="providers"
    )

    def __repr__(self) -> str:
        return "Provider(name= %s)" % (self.name)


class Requester(Base):
    __tablename__ = "requesters"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    created_by_id = Column(
        "created_by_id", ForeignKey("administrators.id"), nullable=False
    )
    updated_by_id = Column(
        "updated_by_id", ForeignKey("administrators.id"), nullable=True
    )
    name = Column("name", String(100), nullable=False)
    last_name = Column("last_name", String(100), nullable=False)
    work_as = Column("work_as", String(100), nullable=False)
    department = Column("department", String(100), nullable=False)
    creation_date = Column("creation_date", DateTime(), nullable=False)
    update_date = Column("update_date", DateTime(), nullable=True)
    requests = relationship("Request", backref="requesters")


    def __repr__(self) -> str:
        return "Requester (name=%s, last_name=%s)" % (self.name, self.last_name)


class Request(Base):
    __tablename__ = "requests"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    created_by_id = Column(
        "created_by_id", ForeignKey("administrators.id"), nullable=False
    )
    updated_by_id = Column(
        "updated_by_id", ForeignKey("administrators.id"), nullable=True
    )
    requester_id = Column(
        "requester_id", ForeignKey("requesters.id", ondelete="CASCADE"), nullable=False
    )
    request_number = Column("request_number", String(50), nullable=False)
    description = Column("description", String(100), nullable=False)
    comments = Column("comments", Text(), nullable=False)
    requested_at = Column("requested_at", DateTime(), nullable=True)
    received = Column("received", String(25), nullable=False, default=Received.NO)
    purchase_order_number = Column("purchase_order_number", String(50), nullable=True)
    creation_date = Column("creation_date", DateTime(), nullable=False)
    update_date = Column("update_date", DateTime(), nullable=True)
    providers = relationship(
        "Provider", secondary="request_providers", back_populates="requests"
    )

    def __repr__(self) -> str:
        return "Request (id=%s, request_number=%s)" % (self.id, self.request_number)


# association table
request_providers = Table(
    "request_providers",
    Base.metadata,
    Column("request_id", ForeignKey("requests.id", ondelete="CASCADE"), primary_key=True),
    Column("provider_id", ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True),
)
