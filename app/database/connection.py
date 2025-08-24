from contextlib import contextmanager
from typing import Generator

from loguru import logger
from sqlmodel import Session, SQLModel
from sqlmodel import create_engine as sqlmodel_create_engine

from app.core.settings import settings

engine = None
SessionLocal = None


def init_database():
    global engine, SessionLocal

    try:
        database_url = f"sqlite:///{settings.DATABASE_PATH}"
        engine = sqlmodel_create_engine(
            database_url, echo=settings.DATABASE_ECHO, connect_args={"check_same_thread": False}
        )

        SessionLocal = Session

        SQLModel.metadata.create_all(bind=engine)
        logger.info(f"Database initialized successfully at {database_url}")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_engine():
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return engine


def get_session_factory():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return SessionLocal


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def close_database():
    global engine
    if engine:
        engine.dispose()
        logger.info("Database connection closed")
