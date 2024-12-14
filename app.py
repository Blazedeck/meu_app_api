from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Exercicio, Descricao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
exercicio_tag = Tag(name="Exercicio", description="Adição, visualização e remoção de exercicios à base")
descricao_tag = Tag(name="Descricao", description="Adição de uma descricao à um exercicio cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_exercicio(form: ExercicioSchema):
    """Adiciona um novo Exercicio à base de dados

    Retorna uma representação dos exercicios e descricoes associadas.
    """
    exercicio = Exercicio(
        nome=form.nome,
        series=form.series,
        repeticoes=form.repeticoes,
        quilos=form.quilos)
    logger.debug(f"Adicionando exercicios de nome: '{exercicio.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando exercicio
        session.add(exercicio)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado exercicio de nome: '{exercicio.nome}'")
        return apresenta_exercicio(exercicio), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Exercicio de mesmo nome já salvo na base"
        logger.warning(f"Erro ao adicionar exercicio '{exercicio.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item"
        logger.warning(f"Erro ao adicionar exercicio '{exercicio.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/exercicios', tags=[exercicio_tag],
         responses={"200": ListagemExerciciosSchema, "404": ErrorSchema})
def get_exercicios():
    """Faz a busca por todos os Exercicios cadastrados

    Retorna uma representação da listagem de exercicios.
    """
    logger.debug(f"Coletando exercicios ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    exercicios = session.query(Exercicio).all()

    if not exercicios:
        # se não há exercicios cadastrados
        return {"exercicios": []}, 200
    else:
        logger.debug(f"%d exercicios econtrados" % len(exercicios))
        # retorna a representação de exercicio
        print(exercicios)
        return apresenta_exercicios(exercicios), 200


@app.get('/exercicio', tags=[exercicio_tag],
         responses={"200": ExercicioViewSchema, "404": ErrorSchema})
def get_exercicio(query: ExercicioBuscaSchema):
    """Faz a busca por um Exercicio a partir do nome do exercicio

    Retorna uma representação dos exercicios e comentários associados.
    """
    exercicio_nome = query.nome
    logger.debug(f"Coletando dados sobre exercicio #{exercicio_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    exercicio = session.query(Exercicio).filter(Exercicio.nome == exercicio_nome).first()

    if not exercicio:
        # se o exercicio não foi encontrado
        error_msg = "Exercicio não encontrado na base :/"
        logger.warning(f"Erro ao buscar exercicio '{exercicio_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Exercicio econtrado: '{exercicio.nome}'")
        # retorna a representação de exercicio
        return apresenta_exercicio(exercicio), 200


@app.delete('/exercicio', tags=[exercicio_tag],
            responses={"200": ExercicioDelSchema, "404": ErrorSchema})
def del_exercicio(query: ExercicioBuscaSchema):
    """Deleta um Exercicio a partir do nome de exercicio informado

    Retorna uma mensagem de confirmação da remoção.
    """
    exercicio_nome = unquote(unquote(query.nome))
    print(exercicio_nome)
    logger.debug(f"Deletando dados sobre exercicio #{exercicio_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Exercicio).filter(Exercicio.nome == exercicio_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado exercicio #{exercicio_nome}")
        return {"mesage": "Exercicio removido", "id": exercicio_nome}
    else:
        # se o exercicio não foi encontrado
        error_msg = "Exercicio não encontrado na base :/"
        logger.warning(f"Erro ao deletar exercicio #'{exercicio_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/descricao', tags=[descricao_tag],
          responses={"200": ExercicioViewSchema, "404": ErrorSchema})
def add_descricao(form: DescricaoSchema):
    """Adiciona de uma nova descricao à um exercicio cadastrado na base identificado pelo id

    Retorna uma representação dos exercicios e dedcricoes associadas.
    """
    exercicio_id  = form.exercicio_id
    logger.debug(f"Adicionando descricoes ao exercicio #{exercicio_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo exercicio
    exercicio = session.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    if not exercicio:
        # se exercicio não for encontrado
        error_msg = "Exercicio não encontrado na base"
        logger.warning(f"Erro ao adicionar descricao ao exercicio '{exercicio_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando a descricao
    texto = form.texto
    descricao = Descricao(texto)

    # adicionando o descricao ao exercicio
    exercicio.adiciona_descricao(descricao)
    session.commit()

    logger.debug(f"Adicionado descricao ao exercicio #{exercicio_id}")

    # retorna a representação de exercicio
    return apresenta_exercicio(exercicio), 200
