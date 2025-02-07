# AI Video Creator

Este projeto é um criador automático de vídeos utilizando IA para gerar narrações e conteúdo.

## Pré-requisitos

1. **Python**
   - Baixe e instale o Python 3.8 ou superior do [site oficial do Python](https://www.python.org/downloads/)
   - Durante a instalação, certifique-se de marcar a opção "Add Python to PATH"
   - Para verificar se a instalação foi bem sucedida, abra o terminal e digite:
     ```
     python --version

2. **Extensão para python vsCODE**
   - Baixe e instale "@category:debuggers Python" no vs CODE

## Configuração do Projeto

1. **Clone o repositório**
   ```
   git clone [URL_DO_REPOSITÓRIO]
   cd ai-video-creating
   ```

2. **Instale as dependências**
   ```
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione suas chaves de API:
     ```
     OPENAI_API_KEY=sua_chave_aqui
     ELEVENLABS_API_KEY=sua_chave_aqui
     ```

## Como Usar

1. **Execute o script principal**
   ```
   python main.py
   ```

2. **Siga as instruções no terminal**
   - Você será solicitado a fornecer:
     - Tema do texto
     - Objetivo do texto
     - Emoção desejada
     - Estilo de narração
     - Idioma
     - Duração do script

## Estrutura do Projeto

```
ai-video-creating/
├── auth_settings/      # Configurações de autenticação
├── prompts/           # Templates de prompts para IA
├── services/         # Serviços de integração (OpenAI, ElevenLabs, etc.)
├── main.py           # Script principal
└── requirements.txt  # Dependências do projeto
```

## Solução de Problemas

1. **FFmpeg não encontrado**
   - Verifique se o FFmpeg está corretamente adicionado ao PATH do sistema
   - Reinicie o terminal após adicionar ao PATH

2. **Erro de API Key**
   - Verifique se o arquivo `.env` está configurado corretamente
   - Confirme se as chaves de API são válidas

3. **Dependências faltando**
   - Execute novamente:
     ```
     pip install -r requirements.txt
     ```

## Suporte

Se encontrar algum problema ou tiver dúvidas, por favor, abra uma issue no repositório.
