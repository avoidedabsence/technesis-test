from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import List

Base = declarative_base(cls=AsyncAttrs)

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
        nullable=False
    )

    items: Mapped[List["Item"]] = relationship(
        "Item",
        cascade="all, delete-orphan",
        passive_deletes=True,
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
    
    price: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    site: Mapped[Site] = relationship(
        "Site"
    )
