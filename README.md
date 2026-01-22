# Gerenciando Projetos

Aplicativo construido em Django.

## Da escolha da Stack

Como era necessária a construção do frontend puro, é melhor que 
fosse gerado direto do servidor.

Sobre a escolha do PostgreSQL, foi para evitar maiores dores de 
cabeça com relação à migrações, uma vez que o SQLite não
possui ```ALTER TABLE```.


## Configurações Iniciais

Primeiramente, é importante que as bibliotecas sejam
instaladas na máquina, ou container, que irá executar
a aplicação.

Para isso, faça:

```{bash}
    cd manager
    pip install -r requirements.txt
```

### psycopg2

É provável que seja necessária a instalação de algumas
bibliotecas, caso utilize linux devido a necessidade
de "buildar" o **psycopg2**.

Em uma máquina com Ubuntu instalado, pastaram duas:

```{bash}
sudo apt install libpq-dev
sudo apt install build-essential
```


## Como realizar as migrações

Primeiramente é necessário ter um banco de dados PostgreSQL
rodando na máquina, o que é bem simples se utilizar o
```docker-compose.yml``` qque acompanha o projeto.

```{bash}
docker compose up -d db
```

Finalmente, você pode preencher um arquivo
```.env``` dentro da pasta ```manager``` como
está de exemplo no arquivo ```env.example```
com as variáveis não setadas.

Agora, basta um

```{bash}
python manager/manager.py migrate
```

para realizar todas as migrações.

## Para Rodar o Projeto

Para executar, basta fazer:

```{bash}
python manager/manager.py runserver
```

que o servidor django abrirá na porta 8000.


## Via Docker

Por alguns motivos, incluindo o build do 
**psycopg2** foi adicionado a solução por
rodar o projeto localmente via Docker.

Para tal, pode-se utilizar o arquivo
```docker-compose.yml``` executando os
três comandos abaixo:

```{bash}
docker compose build server

docker compose up -d db

docker compose up -d server
```


## Para editar tarefas de um Projeto

No sistema existe uma tela com a descrição do projeto. 
Nela, é possível ver as tarefas associadas.

Para modificar o status de uma tarefa
basta clicar e arrastar para a coluna pertencente.
