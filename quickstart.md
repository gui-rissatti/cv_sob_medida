# Guia de Início Rápido (Quickstart)

Este guia vai te ajudar a rodar o **CV Sob Medida** na sua máquina local em poucos minutos.

## Pré-requisitos

1.  **Git**: Para clonar o repositório.
2.  **Python 3.11+**: Para o backend.
3.  **Node.js 20+**: Para o frontend.
4.  **Google Gemini API Key**: Necessária para a geração de conteúdo. Obtenha em [Google AI Studio](https://aistudio.google.com/app/apikey).

## Passo 1: Clonar o Repositório

```bash
git clone https://github.com/gui-rissatti/vaga_certa.git
cd cv_sob_medida
```

## Passo 2: Configurar o Backend

1.  Navegue até a pasta `backend`:
    ```bash
    cd backend
    ```

2.  Crie um ambiente virtual e ative-o:
    *   **Windows**:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
    *   **Linux/macOS**:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure as variáveis de ambiente:
    *   Copie o arquivo de exemplo:
        ```bash
        cp .env.example .env
        ```
    *   Abra o arquivo `.env` e cole sua `GOOGLE_API_KEY`.

5.  Inicie o servidor:
    ```bash
    uvicorn src.main:app --reload
    ```
    O backend estará rodando em `http://localhost:8000`. Você pode testar acessando `http://localhost:8000/docs`.

## Passo 3: Configurar o Frontend

1.  Abra um novo terminal e navegue até a pasta `frontend`:
    ```bash
    cd frontend
    ```

2.  Instale as dependências:
    ```bash
    npm install
    ```

3.  Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev
    ```
    O frontend estará disponível em `http://localhost:5173`.

## Passo 4: Usar a Aplicação

1.  Abra `http://localhost:5173` no seu navegador.
2.  (Opcional) Clique em "Configurar Currículo Base" e cole o texto do seu CV.
3.  Cole a URL de uma vaga (LinkedIn, Indeed, etc.) no campo principal.
4.  Clique em "Gerar".
5.  Aguarde a análise e geração dos materiais.
6.  Visualize e baixe seu currículo, carta de apresentação e dicas.

## Solução de Problemas Comuns

*   **Erro de CORS**: Certifique-se de que o backend está rodando na porta 8000 e o frontend na 5173.
*   **Erro na API do Google**: Verifique se sua chave de API é válida e tem cota disponível.
*   **Dependências**: Se houver erro na instalação do Python, verifique se você tem o compilador C++ instalado (necessário para algumas libs).

## Próximos Passos

Consulte o `README.md` para mais detalhes sobre a arquitetura e `DEPLOY.md` para colocar em produção.
