from pydantic import BaseModel


class DescricaoSchema(BaseModel):
    """ Define como uma nova descricao a ser inserida deve ser representada
    """
    exercicio_id: int = 1
    texto: str = "Inserir descricao bem explicativa para a execucao do exercicio"
