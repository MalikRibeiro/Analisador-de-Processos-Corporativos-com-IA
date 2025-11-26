# Analisador de Processos Corporativos com IA

**Corporate Process Analyzer AI** é uma ferramenta avançada de *Process Mining* e Automação que utiliza Inteligência Artificial (Google Gemini) para analisar fluxos de trabalho corporativos. A ferramenta grava a tela do usuário, registra interações e, ao final, gera um relatório detalhado com diagramas de fluxo e sugestões de automação.

## 🚀 Funcionalidades

*   **Gravação Inteligente**: Captura de vídeo da tela e logs de ações (cliques, teclas) e janelas ativas.
*   **Análise com IA**: Utiliza o modelo **Gemini 2.5 Flash** (com fallback para versões anteriores) para entender o processo executado.
*   **Relatórios Profissionais**: Gera relatórios em **HTML** moderno, contendo:
    *   Descrição passo a passo do processo.
    *   Identificação de gargalos e ineficiências.
    *   **Diagramas de Fluxo (Mermaid.js)** renderizados automaticamente.
    *   Sugestões concretas de automação (RPA, Python, API).
*   **Interface Minimalista**: GUI intuitiva baseada em etapas (Gravação -> Análise -> Resultados), desenvolvida com `customtkinter`.
*   **Multi-idioma**: Suporte para análise em Português, Inglês e Espanhol.
*   **Gestão de Histórico**: Arquivos de vídeo e relatórios são salvos com timestamp para evitar sobrescrita.

## 🛠️ Instalação

1.  **Pré-requisitos**:
    *   Python 3.10 ou superior.
    *   Uma chave de API do Google Gemini (Google AI Studio).

2.  **Clone o repositório** (ou baixe os arquivos):
    ```bash
    git clone <url-do-repositorio>
    cd CorporateProcessAnalyzer
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração da API Key**:
    *   Você pode criar um arquivo `.env` na raiz do projeto com o conteúdo:
        ```env
        GOOGLE_API_KEY=sua_chave_aqui
        ```
    *   OU, ao iniciar o aplicativo, clique no ícone de engrenagem (⚙️) e cole sua chave.

## ▶️ Como Usar

1.  Execute o aplicativo:
    ```bash
    python gui_app.py
    ```

2.  **Etapa 1: Início**
    *   Selecione o idioma desejado para o relatório.
    *   Clique em **"🔴 Iniciar Gravação"**.

3.  **Etapa 2: Gravação**
    *   A janela mostrará um cronômetro gigante.
    *   Minimize a janela e execute o processo de negócio que deseja analisar.
    *   Quando terminar, restaure a janela e clique em **"⏹ Parar e Analisar"**.

4.  **Etapa 3: Análise**
    *   Aguarde enquanto a IA processa o vídeo e os logs. Isso pode levar alguns minutos dependendo da duração.

5.  **Etapa 4: Resultados**
    *   Ao finalizar, você verá uma tela de sucesso.
    *   Clique em **"✨ Visualizar Relatório"** para abrir o HTML no seu navegador padrão.
    *   Os relatórios ficam salvos na pasta `reports/`.

## 📂 Estrutura do Projeto

*   `gui_app.py`: Interface gráfica principal (Entry Point).
*   `app/`: Módulos principais.
    *   `screen_recorder.py`: Gravação de tela com OpenCV/MSS.
    *   `action_logger.py`: Registro de inputs de teclado e mouse.
    *   `process_miner.py`: Monitoramento de janelas ativas.
    *   `process_analyst_agent.py`: Integração com a API do Google Gemini.
    *   `automation_advisor.py`: Geração de relatórios HTML.
*   `data/`: Armazena os vídeos gravados (`.mp4`).
*   `reports/`: Armazena os relatórios gerados (`.html`).

## 💻 Tecnologias

*   **Python 3.12**
*   **CustomTkinter**: Interface Gráfica.
*   **Google Generative AI (Gemini)**: Cérebro da análise.
*   **OpenCV & MSS**: Captura de vídeo de alta performance.
*   **Pynput**: Monitoramento de periféricos.
*   **Mermaid.js**: Renderização de diagramas.

---
Desenvolvido para otimizar processos corporativos com o poder da IA.
