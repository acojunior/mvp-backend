from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Treino, Exercicio, TreinoExercicio, Cliente, ClienteTreino
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API do sistema de gerenciamento de Cliente e Treinos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
exercicio_tag = Tag(name="Exercício", description="Adição, visualização e remoção de Exercícios à base")
treino_tag = Tag(name="Treino", description="Adição, visualização e remoção de Treino à base")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de Cliente à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/exercicio', tags=[exercicio_tag],
          responses={"200": ExercicioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_exercicio(form: ExercicioSchema):
    """Adiciona um novo Exercício à base de dados

    Retorna uma representação dos exercícios.
    """
    exercicio = Exercicio(nome=form.nome)
    logger.debug(f"Adicionando exercício de nome: '{exercicio.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando exercício
        session.add(exercicio)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado exercício de nome: '{exercicio.nome}'")
        return apresenta_exercicio(exercicio), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Exercício de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar exercício '{exercicio.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar exercício '{exercicio.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/exercicios', tags=[exercicio_tag],
         responses={"200": ListagemExerciciosSchema, "404": ErrorSchema})
def get_exercicios():
    """Faz a busca por todos os exercícios cadastrados

    Retorna uma representação da listagem de exercícios.
    """
    logger.debug(f"Coletando exercícios ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    exercicios = session.query(Exercicio).all()

    if not exercicios:
        # se não há exercícios cadastrados
        return {"exercicios": []}, 200
    else:
        logger.debug(f"%d exercícios econtrados" % len(exercicios))
        # retorna a representação de produto
        print(exercicios)
        return apresenta_exercicios(exercicios), 200


@app.get('/exercicio', tags=[exercicio_tag],
         responses={"200": ExercicioViewSchema, "404": ErrorSchema})
def get_exercicio(query: ExercicioBuscaSchema):
    """Faz a busca por um Exercício a partir do id do exercício

    Retorna uma representação dos exercícios.
    """
    exercicio_id = query.id
    logger.debug(f"Coletando dados sobre exercício #{exercicio_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    exercicio = session.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    if not exercicio:
        # se o exercício não foi encontrado
        error_msg = "Exercício não encontrado na base :/"
        logger.warning(f"Erro ao buscar exercício '{exercicio_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Exercício econtrado: '{exercicio.id}'")
        # retorna a representação de exercício
        return apresenta_exercicio(exercicio), 200


@app.put('/exercicio', tags=[exercicio_tag],
         responses={"200": ExercicioViewSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_exercicio(form: ExercicioUpdateSchema):
    """Atualiza um Exercício existente na base de dados

    Retorna uma representação do exercício atualizado.
    """
    exercicio_id = form.id
    logger.debug(f"Atualizando exercício #{exercicio_id}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando o exercício
        exercicio = session.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        
        if not exercicio:
            # se o exercício não foi encontrado
            error_msg = "Exercício não encontrado na base :/"
            logger.warning(f"Erro ao atualizar exercício '{exercicio_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        
        # atualizando o nome do exercício
        exercicio.nome = form.nome
        session.commit()
        logger.debug(f"Exercício #{exercicio_id} atualizado com sucesso")
        return apresenta_exercicio(exercicio), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Exercício de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao atualizar exercício '{exercicio_id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o exercício :/"
        logger.warning(f"Erro ao atualizar exercício '{exercicio_id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/exercicio', tags=[exercicio_tag],
            responses={"200": ExercicioDelSchema, "404": ErrorSchema})
def del_exercicio(query: ExercicioBuscaSchema):
    """Deleta um Exercício a partir do id de exercício informado

    Retorna uma mensagem de confirmação da remoção.
    """
    exercicio_id = query.id
    print(exercicio_id)
    logger.debug(f"Deletando dados sobre exercício #{exercicio_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    exercicio = session.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
    if exercicio:
        # usando o session para deletar para ativar o efeito cascata
        session.delete(exercicio)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado exercício #{exercicio_id}")
        return {"mesage": "Exercício removido", "id": exercicio_id}
    else:
        # se o exercício não foi encontrado
        error_msg = "Exercício não encontrado na base :/"
        logger.warning(f"Erro ao deletar exercício #'{exercicio_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/treino', tags=[treino_tag],
          responses={"200": TreinoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_treino(body: TreinoSchema):
    """Adiciona um novo Treino à base de dados

    Retorna uma representação dos treinos.
    """
    treino = Treino(nome=body.nome)
    logger.debug(f"Adicionando treino de nome: '{treino.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # verifica se o exercicio enviado está cadastrado na base
        for item in body.exercicios:
            exercicio = session.get(Exercicio, item.id_exercicio)
            if not exercicio:
                error_msg = "Exercicio não localizado :/"
                logger.warning(f"Erro ao adicionar treino '{treino.nome}', {error_msg}")
                return {"mesage": error_msg}, 400

            treino.treino_exercicios.append(
                TreinoExercicio(
                    treino=treino,
                    exercicio=exercicio,
                    series=item.series,
                    repeticoes=item.repeticoes
                )
            )
        session.add(treino)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado treino de nome: '{treino.nome}'")
        return apresenta_treino(treino), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Treino de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar treino '{treino.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar treino '{treino.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/treinos', tags=[treino_tag],
         responses={"200": ListagemTreinosSchema, "404": ErrorSchema})
def get_treinos():
    """Faz a busca por todos os Treino cadastrados

    Retorna uma representação da listagem de treinos.
    """
    logger.debug(f"Coletando treinos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    treinos = session.query(Treino).all()

    if not treinos:
        # se não há treinos cadastrados
        return {"treinos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(treinos))
        # retorna a representação de treino
        print(treinos)
        return apresenta_treinos(treinos), 200


@app.get('/treino', tags=[treino_tag],
         responses={"200": TreinoViewSchema, "404": ErrorSchema})
def get_treino(query: TreinoBuscaSchema):
    """Faz a busca por um Treino a partir do id do treino

    Retorna uma representação dos treinos e exercícios associados.
    """
    treino_id = query.id
    logger.debug(f"Coletando dados sobre treino #{treino_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    treino = session.query(Treino).filter(Treino.id == treino_id).first()

    if not treino:
        # se o treino não foi encontrado
        error_msg = "Treino não encontrado na base :/"
        logger.warning(f"Erro ao buscar treino '{treino_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Treino econtrado: '{treino.id}'")
        # retorna a representação de treino
        return apresenta_treino(treino), 200


@app.put('/treino', tags=[treino_tag],
         responses={"200": TreinoViewSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_treino(body: TreinoUpdateSchema):
    """Atualiza um treino existente na base de dados

    Retorna uma representação do treino atualizado.
    """
    treino_id = body.id
    logger.debug(f"Atualizando treino #{treino_id}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando o treino
        treino = session.query(Treino).filter(Treino.id == treino_id).first()
        
        if not treino:
            # se o treino não foi encontrado
            error_msg = "Treino não encontrado na base :/"
            logger.warning(f"Erro ao atualizar treino '{treino_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        
        # atualizando o nome do treino
        if (treino.nome != body.nome):
            treino.nome = body.nome

        treino.treino_exercicios.clear()
        # verifica se o exercicio enviado está cadastrado na base
        for item in body.exercicios:
            exercicio = session.get(Exercicio, item.id_exercicio)
            if not exercicio:
                error_msg = "Exercicio não localizado :/"
                logger.warning(f"Erro ao atualizar treino '{treino.nome}', {error_msg}")
                return {"mesage": error_msg}, 400

            treino.treino_exercicios.append(
                TreinoExercicio(
                    treino=treino,
                    exercicio=exercicio,
                    series=item.series,
                    repeticoes=item.repeticoes
                )
            )

        session.commit()
        logger.debug(f"Treino #{treino_id} atualizado com sucesso")
        return apresenta_treino(treino), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Treino de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao atualizar treino '{treino_id}' '{body.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o treino :/"
        logger.warning(f"Erro ao atualizar treino '{treino_id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/treino', tags=[treino_tag],
            responses={"200": TreinoDelSchema, "404": ErrorSchema})
def del_treino(query: TreinoBuscaSchema):
    """Deleta um Treino a partir do id de treino informado

    Retorna uma mensagem de confirmação da remoção.
    """
    treino_id = query.id
    print(treino_id)
    logger.debug(f"Deletando dados sobre treino #{treino_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    treino = session.query(Treino).filter(Treino.id == treino_id).first()
    if treino:
        session.delete(treino)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado treino #{treino_id}")
        return {"mesage": "Treino removido", "nome": treino.nome}
    else:
        # se o treino não foi encontrado
        error_msg = "Treino não encontrado na base :/"
        logger.warning(f"Erro ao deletar treino #'{treino_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(body: ClienteSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação dos clientes.
    """
    
    cliente = Cliente(
        nome=body.nome, 
        data_nascimento=body.data_nascimento, 
        peso=body.peso, 
        altura=body.altura
    )
    logger.debug(f"Adicionando cliente de nome: '{cliente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # verifica se o treino enviado está cadastrado na base
        for item in body.treinos:
            treino = session.get(Treino, item.id_treino)
            if not treino:
                error_msg = "Treino não localizado :/"
                logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
                return {"mesage": error_msg}, 400

            cliente.cliente_treinos.append(
                ClienteTreino(
                    cliente=cliente,
                    treino=treino,
                    dia_semana=item.dia_semana
                )
            )

        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente de nome: '{cliente.nome}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os Clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(clientes))
        # retorna a representação de cliente
        print(clientes)
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um Cliente a partir do id do cliente

    Retorna uma representação dos clientes e exercícios associados.
    """
    cliente_id = query.id
    logger.debug(f"Coletando dados sobre cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{cliente.id}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200


@app.put('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_cliente(body: ClienteUpdateSchema):
    """Atualiza um cliente existente na base de dados

    Retorna uma representação do cliente atualizado.
    """
    cliente_id = body.id
    logger.debug(f"Atualizando cliente #{cliente_id}")
    try:
        # criando conexão com a base
        session = Session()
        # buscando o cliente
        cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not Cliente:
            # se o Cliente não foi encontrado
            error_msg = "Cliente não encontrado na base :/"
            logger.warning(f"Erro ao atualizar cliente '{cliente_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        
        # atualizando o nome do cliente
        if (cliente.nome != body.nome):
            cliente.nome = body.nome
        
        cliente.data_nascimento = body.data_nascimento
        cliente.peso = body.peso
        cliente.altura = body.altura

        cliente.cliente_treinos.clear()
        # verifica se o treino enviado está cadastrado na base
        for item in body.treinos:
            treino = session.get(Treino, item.id_treino)
            if not treino:
                error_msg = "Treino não localizado :/"
                logger.warning(f"Erro ao atualizar cliente '{cliente.nome}', {error_msg}")
                return {"mesage": error_msg}, 400

            cliente.cliente_treinos.append(
                ClienteTreino(
                    cliente=cliente,
                    treino=treino,
                    dia_semana=item.dia_semana
                )
            )

        session.commit()
        logger.debug(f"Cliente #{cliente_id} atualizado com sucesso")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao atualizar cliente '{cliente_id}' '{body.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o cliente :/"
        logger.warning(f"Erro ao atualizar cliente '{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um Cliente a partir do id de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_id = query.id
    print(cliente_id)
    logger.debug(f"Deletando dados sobre cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente #{cliente_id}")
        return {"mesage": "Cliente removido", "nome": cliente.nome}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404


