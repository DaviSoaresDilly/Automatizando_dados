from sqlalchemy import Engine
from app.database import get_session
from app.models import Base
from app.populate import populate_data
from app.generate_atendimentos import generate_atendimentos

def reset_database(engine: Engine):
    """Função para dropar e recriar todas as tabelas"""
    print("Excluindo todas as tabelas existentes...")
    Base.metadata.drop_all(engine)  # Excluir todas as tabelas

    print("Criando novas tabelas...")
    Base.metadata.create_all(engine)  # Criar todas as tabelas

def main():
    session = get_session()

    # Resetar o banco de dados (drop + create)
    reset_database(session.bind)

    # População dos dados
    populate_data(session)

    # Geração de atendimentos (simulação com ID)
    generate_atendimentos(session, 50000)

if __name__ == "__main__":
    main()
