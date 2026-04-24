# 🎙️ Voice Kity Assistant

Assistente de voz inteligente para busca de produtos a partir de comandos falados.

## 🚀 Funcionalidades
- Captura de áudio
- Transcrição com Whisper
- Interpretação de intenção
- Busca inteligente
- Resposta por voz

## 🧱 Arquitetura (MVC)

### Model
- catalog_pdf.py
- catalog_store.py
- intent.py

### Controller
- voice_app.py

### View
- Voz + Console

## 📦 Instalação

```bash
pip install -r requirements.txt
```

## ▶️ Execução

```bash
python voice_app.py
```

## 🗣️ Exemplos
- "Quero Malbec"
- "Floratta até 150 reais"
- "Encerrar"

## 💡 Melhorias
- NLP com IA
- Streaming de áudio
- API REST

## 📌 Conclusão
Pipeline completo:
Voz → IA → Busca → Resposta
