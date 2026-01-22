# 🎙️ Voice Kity Assistant

Assistente de voz offline para consulta de catálogo de e-commerce, utilizando **STT (Whisper)**, **processamento de intenção em PT-BR**, **cache de catálogo real (Kyte)** e **TTS**, tudo **100% gratuito** e rodando localmente.

> Projeto desenvolvido como evolução prática de um laboratório de Voz + IA, com foco em integração real, robustez e portfólio profissional.

---

## 🚀 Funcionalidades

- 🎤 Captura de voz pelo microfone (Windows / WASAPI)
- 🧠 Transcrição de fala com **Whisper local**
- 🔍 Entendimento de intenção e filtros em português  
  - Ex: “creme para olhos até cem reais”
- 💰 Reconhecimento de valores falados (“cem”, “cento e cinquenta”, “150”)
- 🛍️ Consulta a **catálogo real de e-commerce (Kyte)** via cache local
- 🔊 Resposta por voz com **Text-to-Speech offline**
- ♻️ Atualização manual do catálogo (modo humano – Cloudflare safe)

---

## 🧩 Arquitetura do Projeto

Voz (microfone)
→ Whisper (Speech-to-Text)
→ Parser de intenção + filtros
→ Busca em catálogo cacheado (JSON)
→ Formatação da resposta
→ Text-to-Speech
→ Voz


---

## 🗂️ Estrutura de Arquivos

voice-kity-assistant/
├─ .venv/
├─ pw_profile/
├─ catalog_cache.json
├─ voice_app.py
├─ intent.py
├─ catalog_store.py
├─ kity_source_human.py
├─ README.md
└─ debug/
├─ listar_mics.py
├─ test.wav
└─ user.wav


---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Whisper (faster-whisper)
- SoundDevice / PortAudio
- Playwright
- pyttsx3
- JSON
- Regex + parsing semântico em PT-BR

---

## ⚙️ Instalação

### Criar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate
Instalar dependências
pip install faster-whisper sounddevice scipy numpy pyttsx3 playwright
python -m playwright install chromium
▶️ Como Usar
Rodar o assistente
python voice_app.py
Exemplos de comandos de voz:

“Quero creme para olhos”

“Tem algo até cem reais?”

“Me mostra um produto até cento e cinquenta”

Atualizar o catálogo
python kity_source_human.py
O navegador abrirá

Resolva o Cloudflare manualmente

Quando os produtos aparecerem, volte ao terminal e pressione ENTER

O arquivo catalog_cache.json será atualizado

📌 Observações
O projeto não burla proteções

Funciona offline após o cache

Whisper pode ser trocado (base, small) conforme desempenho

📈 Evoluções Futuras
Memória curta de contexto

Integração com LLM local (Ollama)

Abertura de links por voz

Logs de interação

Interface web ou desktop

🎯 Objetivo
Demonstrar um pipeline completo de voz com IA, integrando áudio real, NLP em português e dados reais de e-commerce, com foco em aprendizado aplicado e portfólio profissional.

👩‍💻 Autoria
Desenvolvido por Bianca Casemira
Brasil


---

### 3️⃣ Salve o arquivo
Pronto.  
No **GitHub**, isso vai renderizar **perfeitinho**, com títulos, listas, código, tudo certo.

---

## 🔎 Como saber se está OK
Abra o `README.md`:
- no VS Code → Preview
- ou suba no GitHub

Se aparecer bonito, **não quebrou nada** 💙

---

## Quer que eu faça agora?
Posso:
- ✔️ simplificar o README
- ✔️ deixar mais **corporativo**
- ✔️ traduzir para **inglês**
- ✔️ criar versão **README + README.en.md**

Só me diz 👍
::contentReference[oaicite:0]{index=0}
