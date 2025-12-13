from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base


class ClienteTreino(Base):
    """
    Essa classe representa a associação entre o Cliente e o Treino.
    """
    __tablename__ = 'cliente_treinos'

    id_cliente = Column(ForeignKey("cliente.id"), primary_key=True)
    id_treino = Column(ForeignKey("treino.id"), primary_key=True)
    dia_semana = Column(String(30), nullable=False)

    # relacionamento ORM.
    cliente = relationship("Cliente", back_populates="cliente_treinos")
    treino = relationship("Treino", back_populates="cliente_treinos")

    def __init__(self, cliente, treino, dia_semana:str):
        """
        Cria o relacionamento entre o Cliente e o Treino

        Arguments:
            cliente: model do cliente.
            treino: model do treino.
            dia_semana: dia da semana que o cliente deverá fazer
                           o exercicio.
        """
        self.cliente = cliente
        self.treino = treino
        self.dia_semana = dia_semana
