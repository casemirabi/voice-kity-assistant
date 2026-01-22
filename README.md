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

