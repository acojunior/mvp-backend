from sqlalchemy import Column, String, Integer, DateTime, Date, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import date, datetime
from typing import Optional

from  model import Base, Treino


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    data_nascimento = Column(Date)
    altura = Column(Numeric(1, 2))
    peso = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now)

    # Definição do relacionamento entre o cliente e treino.
    # A relação é representada na tabela cliente_treinos.
    cliente_treinos = relationship(
        "ClienteTreino",
        back_populates="cliente",
        # Deleta em cascata, ou seja, caso seja deletado um cliente
        # as tuplas de relacionamento do mesmo serão deletadas.
        cascade="all, delete-orphan"
    )

    def __init__(self, nome:str, altura:float, peso:float,
                 data_nascimento: Optional[date] = None,
                 data_insercao: Optional[datetime] = None):
        """
        Cria um Cliente

        Arguments:
            nome: nome do cliente.
            data_nascimento: data de nascimento do cliente.
            altura: altura do cliente.
            peso: peso do cliente.
            data_insercao: data de quando o cliente foi inserido à base
        """
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.altura = altura
        self.peso = peso

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

