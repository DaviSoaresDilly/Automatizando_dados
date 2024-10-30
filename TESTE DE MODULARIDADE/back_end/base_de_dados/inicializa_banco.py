# base_de_dados/inicializa_banco.py
from base_de_dados.database import engine
from back_end.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
