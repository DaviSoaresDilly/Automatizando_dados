# main.py
from backend.app.database import get_session
from .models import Base
from .populate import populate_data
from .generate_atendimentos import generate_atendimentos

def main():
    session = get_session()

    # Criação das tabelas
    Base.metadata.create_all(session.bind)

    # População dos dados
    populate_data(session)

    # Geração de atendimentos
    generate_atendimentos(session, 100)

if __name__ == "__app__":
    main()
