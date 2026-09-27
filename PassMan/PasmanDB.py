
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import LargeBinary, String
#SQL Datenbank

class Base(DeclarativeBase):
    pass

class PasswordEntry(Base):
    __tablename__ = "passwords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    service: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(String(255))

    nonce: Mapped[bytes] = mapped_column(LargeBinary)

    ciphertext: Mapped[bytes] = mapped_column(LargeBinary)

class vault_metadata(Base):
    __tablename__ = "Vault"
    id: Mapped[int] = mapped_column(primary_key=True)
    salt: Mapped[bytes] = mapped_column(LargeBinary)
    phash: Mapped[str] = mapped_column(String)

