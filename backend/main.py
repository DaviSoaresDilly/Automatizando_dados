# main.py

from sqlalchemy import Engine
from app.database import get_session, create_app
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
    app = create_app()  # Crie a aplicação Flask
    with app.app_context():  # Ative o contexto da aplicação
        session = get_session()

        # Verifique se o engine está corretamente configurado
        engine = session.get_bind()
        if engine is None:
            raise RuntimeError("Engine não configurado corretamente na sessão.")

        # Resetar o banco de dados (drop + create)
        reset_database(engine)

        # População dos dados
        populate_data(session)

        # Geração de atendimentos (simulação com ID)
        generate_atendimentos(session, 100)

if __name__ == "__main__":
    main()