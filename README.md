# 🎵 LyricFlow

LyricFlow é uma aplicação desktop que exibe as letras das músicas que você está ouvindo no Spotify em tempo real, sincronizadas palavra por palavra — flutuando na sua tela enquanto você trabalha, estuda ou joga.

---

## ✨ Como funciona

- Detecta automaticamente a música tocando no Spotify
- Busca a letra sincronizada via [lrclib.net](https://lrclib.net)
- Exibe a letra em sobreposição na tela, sempre no topo
- Troca automaticamente quando a música muda
- A janela é arrastável e sem bordas, para não atrapalhar

---

## 🛠️ Stack utilizada

- **Python 3.10+**
- **PyQt6** — interface gráfica e renderização
- **Spotipy** — integração com a API do Spotify
- **lrclib.net API** — letras sincronizadas (LRC)
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **Threading** — busca assíncrona para não travar a UI

---

## ✅ Pré-requisitos

### 1. Spotify Premium
A API de playback do Spotify só funciona com conta **Premium**.

### 2. Criar um app no Spotify Developer

1. Acesse [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Faça login com sua conta Spotify
3. Clique em **"Create App"**
4. Preencha:
   - **App name:** LyricFlow (ou qualquer nome)
   - **Redirect URI:** `http://127.0.0.1:8888/callback`
5. Salve e abra o app criado
6. Copie o **Client ID** e o **Client Secret**

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/wiwu2004/lyricFlow.git
cd lyricflow
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Abra o `.env` e preencha com suas credenciais do Spotify Developer:

```
SPOTIPY_CLIENT_ID=seu_client_id_aqui
SPOTIPY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

---

## ▶️ Como usar

1. Abra o Spotify e coloque uma música para tocar
2. Com o ambiente virtual ativado, execute:

```bash
python main.py
```

3. Na primeira execução, uma janela do navegador vai abrir pedindo autorização do Spotify — basta aceitar
4. A legenda vai aparecer flutuando na tela, sincronizada com a música
5. Arraste a janela para onde preferir na tela

---

## 📁 Estrutura do projeto

```
lyricflow/
├── main.py            # Ponto de entrada
├── ui.py              # Interface gráfica e lógica de exibição
├── spotify_service.py # Integração com a API do Spotify
├── lrc_service.py     # Busca e parsing de letras sincronizadas
├── requirements.txt   # Dependências do projeto
├── .env.example       # Modelo do arquivo de configuração
├── .gitignore
└── README.md
```

---

## 📝 Observações

- Se a música não tiver letra sincronizada disponível no lrclib.net, nada será exibido
- A janela fica sempre no topo da tela e é transparente no fundo
- O token de autenticação do Spotify é salvo localmente em `.cache` após a primeira autorização — não compartilhe esse arquivo
