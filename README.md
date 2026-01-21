# Gerenciando Projetos

Aplicativo construido em Django.

## Da escolha da Stack

Como era necessária a construção do frontend puro, é melhor que 
fosse gerado direto do servidor.

Sobre a escolha do PostgreSQL, foi para evitar maiores dores de 
cabeça com relação à migrações, uma vez que o SQLite não
possui ```ALTER TABLE```.

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
