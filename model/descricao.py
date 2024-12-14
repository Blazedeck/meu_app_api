from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Descricao(Base):
    __tablename__ = 'descricao'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a descricao e um exercicio.
    # Aqui está sendo definido a coluna 'exercicio' que vai guardar
    # a referencia ao exercicio, a chave estrangeira que relaciona
    # um exercicio a uma descricao.
    exercicio = Column(Integer, ForeignKey("exercicio.pk_exercicio"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma descricao

        Arguments:
            texto: o texto de uma descricao.
            data_insercao: data de quando a descricao foi feita ou inserida
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
