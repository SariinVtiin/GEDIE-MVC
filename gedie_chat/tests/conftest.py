"""
Fixtures para os testes GEDIE.
Cria um engine SQLite em memória, monkey-patcha o SessionLocal global
e gera uma sessão isolada para cada teste.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------- #
# Engine + SessionLocal (function-scoped → ok com monkeypatch)
# -------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def _engine_and_session(monkeypatch):
    # Importes tardios (evita efeitos colaterais antes do patch)
    from src.models.base_model import Base
    import src.config.database_config as db_conf

    engine = create_engine("sqlite:///:memory:")
    TestSessionLocal = sessionmaker(bind=engine)

    # Monkey-patch: controllers que importam db_conf usarão esta session
    monkeypatch.setattr(db_conf, "engine", engine, raising=False)
    monkeypatch.setattr(db_conf, "SessionLocal", TestSessionLocal, raising=False)

    # Cria todas as tabelas definidas nos models
    Base.metadata.create_all(bind=engine)

    yield engine, TestSessionLocal

    engine.dispose()

# -------------------------------------------------------------------- #
# Sessão de banco a cada teste
# -------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def db_session(_engine_and_session):
    _, TestSessionLocal = _engine_and_session
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()
