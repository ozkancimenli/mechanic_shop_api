from datetime import datetime
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


class MechanicServiceTicket(Base):   # 🔧 Junction model with extra field
    __tablename__ = "mechanic_service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey("mechanics.id"), nullable=False)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    mechanic: Mapped["Mechanic"] = relationship(back_populates="mechanic_tickets")
    ticket: Mapped["ServiceTicket"] = relationship(back_populates="mechanic_tickets")


class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    mechanic_tickets: Mapped[List["MechanicServiceTicket"]] = relationship(back_populates="ticket")


class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    mechanic_tickets: Mapped[List["MechanicServiceTicket"]] = relationship(back_populates="mechanic")
