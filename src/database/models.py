from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import List

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    
    domain: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", onupdate="RESTRICT", ondelete="CASCADE"),
        nullable=False
    )

    items: Mapped[List["Item"]] = relationship(
        cascade="all, delete-orphan",
        lazy="subquery"
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    
    site_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sites.id", onupdate="RESTRICT", ondelete="CASCADE"),
        nullable=False
    )
    
    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    xpath: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False
    )
    
    sites: Mapped[List["Site"]] = relationship(
        cascade="all, delete-orphan",
        lazy="subquery"
    )