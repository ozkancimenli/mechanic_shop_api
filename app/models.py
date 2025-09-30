from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from .extensions import db

class Base(DeclarativeBase):
    pass

# --- MODELS ---

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = relationship(back_populates="customer")

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary="service_mechanics", back_populates="tickets"
    )

class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = relationship(
        secondary="service_mechanics", back_populates="mechanics"
    )

# Association table
service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)
