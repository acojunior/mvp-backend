# API Backend - SGCT

Sistema de Gerenciamento de Clientes e Treinos

Este MVP faz parte da Sprint de **Desenvolvimento Full Stack Básico** 

Esse sistema serve para uma academia gerenciar seus clientes/alunos, treinos e exercicios.

Cada cliente pode ser relacionado a um ou mais treinos de acordo com os dias da semana.
Cada treino é composto por um ou mais exercicios.

---

## Modelos e relacionamentos

São 3 entidades: Cliente, Treino e Exercício.
Existem dois relacionamentos N:N: Cliente x Treino e Treino x Exercícios.
Ao todo são 5 tabelas: clientes, treinos, exercicios, cliente_treinos e treino_exercicios

## Endpoints

São 5 endpoints por entidades:
 - POST: Adicionar um item ao banco de dados;
 - GET (/entidade no singular): Apresenta as informações de um item em especifico.
 - GET (/entidades no plural): Apresenta uma listagem dos itens daquela tabela.
 - PUT: Atualiza o item no banco de dados;
 - DELETE: Exclui o item do banco de dados;

## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
