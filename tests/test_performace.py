# tests/test_performance.py
import pytest
import time
import psutil
from app.database import create_app, get_session
from app.generate_atendimentos import generate_atendimentos

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def session(app):
    session = get_session()
    yield session
    session.close()

def test_memory_usage(session):
    # Monitora o uso de memória antes e após a geração de atendimentos
    process = psutil.Process()
    mem_before = process.memory_info().rss  # Memória usada antes da execução
    generate_atendimentos(session, 1000)
    mem_after = process.memory_info().rss  # Memória usada após a execução

    # Assegura que o uso de memória não aumenta drasticamente
    assert (mem_after - mem_before) < (100 * 1024 * 1024), "Uso de memória excedeu 100 MB"

def test_cpu_usage(session):
    # Monitora o uso de CPU durante a geração de atendimentos
    process = psutil.Process()
    cpu_before = process.cpu_percent(interval=None)

    start_time = time.time()
    generate_atendimentos(session, 1000)
    end_time = time.time()

    cpu_after = process.cpu_percent(interval=1)  # Monitorar em intervalos de 1 segundo
    execution_time = end_time - start_time

    # Verifica que o uso de CPU não excedeu 80% e a execução não levou mais de 60 segundos
    assert cpu_after < 80, "Uso de CPU excedeu 80%"
    assert execution_time < 60, "Tempo de execução excedeu 60 segundos"

def test_large_batch_performance(session):
    # Teste de desempenho para geração de 10.000 atendimentos
    start_time = time.time()
    generate_atendimentos(session, 10000)
    end_time = time.time()

    execution_time = end_time - start_time
    # Assegura que a geração de 10.000 atendimentos demora menos de 3 minutos
    assert execution_time < 180, "A geração de 10.000 atendimentos foi muito lenta"
