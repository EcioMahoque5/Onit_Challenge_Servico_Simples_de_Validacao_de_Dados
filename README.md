# Serviço Simples de Validação de Dados

Esta aplicação é uma API desenvolvida em Flask que valida dados contra esquemas predefinidos. O serviço aceita um esquema (definindo os tipos de dados e restrições) e os dados a serem validados no corpo da requisição (payload) e retorna se os dados são válidos ou não, juntamente com mensagens de erro específicas.

---

## Passos para Executar a Aplicação

1. **Crie um Ambiente Virtual**

   - No diretório do projeto, crie um ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **Linux/Mac**:
       ```bash
       source venv/bin/activate
       ```

2. **Crie o arquivo `.env`**

   - Na raiz do projeto, crie um arquivo chamado `.env`.
   - Adicione a variável `SECRET_KEY` com um valor qualquer:
     ```env
     SECRET_KEY=sua_chave_secreta_aqui
     ```

3. **Instale os Pacotes Necessários**

   - Certifique-se de estar com o ambiente virtual ativado.
   - Instale os pacotes listados no arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Execute a Aplicação**

   - No terminal, com o ambiente virtual ativado, execute o arquivo principal:
     ```bash
     python main.py
     ```
   - A aplicação será iniciada no endereço padrão: `http://127.0.0.1:5000`.

---

## Endpoints Disponíveis

### 1. **Validação de Dados**

- **URL**: `/api/schema_validation`
- **Método**: `POST`
- **Descrição**: Valida os dados fornecidos com base no esquema especificado.
- **Cabeçalho**:

  ```json
  Content-Type: application/json
  ```

- **Body (JSON)**:

```json
{
  "schema": {
    "name": {
      "type": "string",
      "required": true,
      "min_length": 3,
      "max_length": 50
    },
    "age": { "type": "number", "required": true, "min": 18, "max": 100 },
    "email": { "type": "email", "required": true },
    "is_active": { "type": "boolean", "required": true }
  },
  "data": {
    "name": "John Doe",
    "age": 25,
    "email": "john.doe@example.com",
    "is_active": true
  }
}
```

- **Resposta de Sucesso (200)**:

  ```json
  {
    "success": true,
    "message": "Data is valid!"
  }
  ```

- **Resposta de Erro (400 - Errors de Validação)**:

```json
{
  "success": false,
  "message": "Validations errors",
  "errors": {
    "age": ["age must be between 18 and 100!"],
    "is_active": ["is_active must be a valid boolean value (true/false)."]
  }
}
```

## Estrutura do Projeto

. ├── app/
│ ├── init.py
│ ├── configs.py
│ ├── routes.py
│ └── validators.py
├── venv/
├── .env
├── main.py
├── requirements.txt
└── README.md


## Observações

- Certifique-se de que a variável `SECRET_KEY` está configurada no arquivo `.env` antes de executar a aplicação.
- Sempre ative o ambiente virtual antes de instalar os pacotes ou executar a aplicação:
  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/Mac**:
    ```bash
    source venv/bin/activate
    ```

---


## Demonstração

- **Local**: `http://127.0.0.1:5000/api/schema_validation`
- **Hospedado**: `https://validacao-de-dados-ecio-mahoque.onrender.com/api/schema_validation`
