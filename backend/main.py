# main.py
from app.database import get_session
from app.models import Base
from app.populate import populate_data, reset_database
from app.generate_atendimentos import generate_atendimentos

def main():
    session = get_session()

    # Excluir tabelas antigas
    print("Excluindo todas as tabelas existentes...")
    reset_database(session)

    # Criar novas tabelas
    print("Criando novas tabelas...")
    Base.metadata.create_all(session.bind)

    # População dos dados
    populate_data(session)

    # Geração de atendimentos
    generate_atendimentos(session, 100)

if __name__ == "__main__":
    main()
