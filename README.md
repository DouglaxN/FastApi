# API de Estudantes com FastAPI e PostgreSQL

Projeto prático de estudo utilizando FastAPI, SQLAlchemy e PostgreSQL para implementar um relacionamento 1:1 (Um para Um) entre `Estudante` e `Perfil`.

## Tecnologias

- Python 3
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (`psycopg`)
- Pydantic
- Uvicorn
- python-dotenv

## Estrutura do Projeto

- `database.py`: conexão com o banco de dados PostgreSQL via variável de ambiente (`DATABASE_URL`) e configuração da sessão do SQLAlchemy.
- `models.py`: tabelas `estudantes` e `perfis` mapeadas no SQLAlchemy. A relação 1:1 é garantida pelo `uselist=False` no `relationship` e `unique=True` na chave estrangeira `estudante_id`.
- `schemas.py`: modelos do Pydantic para validação dos dados de entrada (`EstudanteCreate`, `PerfilCreate`) e formatação da resposta (`Estudante`, `Perfil`).
- `main.py`: inicialização da aplicação e rotas de criação e listagem.

## Como rodar

1. Crie e ative o ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instale os pacotes necessários:

```powershell
pip install fastapi uvicorn sqlalchemy "psycopg[binary]" python-dotenv pydantic
```

3. Crie um arquivo `.env` na raiz do projeto com a URL do seu banco PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/nome_do_banco
```

4. Suba o servidor:

```powershell
uvicorn main:app --reload
```

A documentação interativa (Swagger) fica disponível em `http://127.0.0.1:8000/docs`.

## Rotas

### `POST /estudantes/`
Cadastra um estudante e seu perfil juntos na mesma requisição.

Exemplo de JSON de envio:
```json
{
  "nome": "Douglas",
  "email": "douglas@gmail.com",
  "perfil": {
    "idade": 20,
    "endereco": "Rua Imaginária, 236"
  }
}
```

### `GET /estudantes/`
Lista todos os estudantes cadastrados trazendo os dados do perfil na mesma consulta com `joinedload`.

## Anotações de estudo

- O `Base.metadata.create_all(bind=engine)` só cria as tabelas caso elas ainda não existam no banco. Se uma coluna nova for adicionada no `models.py` depois que a tabela já foi criada no PostgreSQL, é necessário atualizar a tabela no banco (`ALTER TABLE`) ou recriá-la.
- No Pydantic v2, usa-se `.model_dump()` no lugar de `.dict()` para converter o schema em dicionário, e `from_attributes = True` na classe `Config`.
- O `joinedload(models.Estudante.perfil)` faz o `JOIN` direto no SQL para evitar consultas repetidas ao banco quando listamos os estudantes.
