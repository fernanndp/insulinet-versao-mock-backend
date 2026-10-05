from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MovementType(str, Enum):
    STOCK_IN = "STOCK_IN"
    DOSE = "DOSE"
    DISCARD = "DISCARD"
    ADJUSTMENT = "ADJUSTMENT"


class ContainerStatus(str, Enum):
    SEALED = "SEALED"
    OPEN = "OPEN"
    EMPTY = "EMPTY"
    DISCARDED = "DISCARDED"


class InsulinType(str, Enum):
    REGULAR = "Regular"
    NPH = "NPH"
    GLARGINA = "Glargina"
    LISPRO = "Lispro"


class AvailabilityLevel(str, Enum):
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    CRITICO = "critico"
    INDISPONIVEL = "indisponivel"


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    insulins: Mapped[list["Insulin"]] = relationship(
        back_populates="user"
    )


class Insulin(Base):
    __tablename__ = "insulin"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    insulin_type: Mapped[InsulinType | None] = mapped_column(
        SqlEnum(
            InsulinType,
            name="insulin_type_mock",
        ),
        nullable=True,
    )

    concentration_units_per_ml: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    container_volume_ml: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    open_validity_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=28,
        server_default=text("28"),
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(
        back_populates="insulins"
    )

    movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="insulin",
        cascade="all, delete-orphan",
    )

    containers: Mapped[list["InsulinContainer"]] = relationship(
        back_populates="insulin",
        cascade="all, delete-orphan",
    )


class InsulinContainer(Base):
    __tablename__ = "insulin_container"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    insulin_id: Mapped[int] = mapped_column(
        ForeignKey("insulin.id"),
        nullable=False,
    )

    initial_units: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    status: Mapped[ContainerStatus] = mapped_column(
        SqlEnum(
            ContainerStatus,
            name="container_status",
        ),
        nullable=False,
        default=ContainerStatus.SEALED,
    )

    opened_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    insulin: Mapped["Insulin"] = relationship(
        back_populates="containers"
    )

    movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="container",
        cascade="all, delete-orphan",
    )


class StockMovement(Base):
    __tablename__ = "stock_movement"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    insulin_id: Mapped[int] = mapped_column(
        ForeignKey("insulin.id"),
        nullable=False,
    )

    container_id: Mapped[int] = mapped_column(
        ForeignKey("insulin_container.id"),
        nullable=False,
    )

    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("stock_movement.id"),
        nullable=True,
    )

    movement_type: Mapped[MovementType] = mapped_column(
        SqlEnum(
            MovementType,
            name="movement_type",
        ),
        nullable=False,
    )

    quantity_units: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    occurred_time_known: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    insulin: Mapped["Insulin"] = relationship(
        back_populates="movements"
    )

    container: Mapped["InsulinContainer"] = relationship(
        back_populates="movements",
        foreign_keys=[container_id],
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class Uaps(Base):
    __tablename__ = "uaps"

    id_uaps: Mapped[int] = mapped_column(
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    bairro: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    endereco: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    estoque: Mapped[list["EstoqueUaps"]] = relationship(
        back_populates="uaps",
        cascade="all, delete-orphan",
    )


class EstoqueUaps(Base):
    __tablename__ = "estoque_uaps"

    id_estoque: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_uaps: Mapped[int] = mapped_column(
        ForeignKey("uaps.id_uaps"),
        nullable=False,
        index=True,
    )

    tipo: Mapped[InsulinType] = mapped_column(
        SqlEnum(
            InsulinType,
            name="insulin_type_mock",
        ),
        nullable=False,
    )

    apresentacao: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    quantidade_disponivel: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    nivel_disponibilidade: Mapped[AvailabilityLevel] = mapped_column(
        SqlEnum(
            AvailabilityLevel,
            name="availability_level",
        ),
        nullable=False,
    )

    lote: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    validade: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    uaps: Mapped["Uaps"] = relationship(
        back_populates="estoque"
    )