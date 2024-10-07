# main.py
from backend.database import get_session
from backend.models import Base
from backend.populate import populate_data
from backend.generate_atendimentos import generate_atendimentos

def main():
    session = get_session()

    # Criação das tabelas
    Base.metadata.create_all(session.bind)

    # População dos dados
    populate_data(session)

    # Geração de atendimentos
    generate_atendimentos(session, 100)

if __name__ == "__main__":
    main()
