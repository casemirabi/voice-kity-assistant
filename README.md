# 🎙️ Voice Kity Assistant

Assistente de voz para busca de produtos em catálogo, utilizando:

- 🎤 Captura de áudio (microfone)
- 🧠 Transcrição com Whisper (faster-whisper)
- 🛍️ Busca inteligente em catálogo (PDF ou JSON)
- 🔊 Resposta por voz (TTS)

---

## 🚀 Funcionalidades

- Buscar produtos por voz:
  - "Quero Malbec"
  - "Procuro Floratta Red"
  - "Perfume até 100 reais"

- Filtrar por:
  - Nome
  - Preço máximo

- Tolerância a erros de fala:
  - "Mal bake" → Malbec
  - "Floreta" → Floratta

---

## ▶️ Como rodar

python voice_app.py

---

## ⚙️ Instalação

pip install -r requirements.txt

---

## 📦 Fonte de dados

PDF ou JSON

---

## ⚠️ Limitações

- Dependente do microfone
- Whisper pode errar nomes
- PDF pode ter ruído

---

## 👨‍💻 Autor

Projeto experimental de assistente de voz.
Desenvolvido por Bianca Melo
