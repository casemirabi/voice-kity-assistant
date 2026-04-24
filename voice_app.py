
#C:\wamp64\www\projetos\projetos\voice-kity-assistant\.venv\Scripts\python.exe voice_app.py

import time
import wave
import numpy as np
import sounddevice as sd
import pyttsx3

from faster_whisper import WhisperModel

from catalog_pdf import load_catalog_from_pdf
from catalog_store import search_catalog
from intent import parse_query

# Use None para automático
MIC_ID = None

whisper = WhisperModel("small", device="cpu", compute_type="int8")


def speak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def write_wav(filename: str, fs: int, audio: np.ndarray):
    audio = np.asarray(audio, dtype=np.int16)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())


def record_wav(filename="user.wav", seconds=5, mic_id=None):
    if mic_id is None:
        dev = sd.query_devices(kind="input")
        device = None
        print(f"🎙️ Microfone padrão: {dev['name']}")
    else:
        dev = sd.query_devices(mic_id)
        device = mic_id
        print(f"🎙️ Microfone {mic_id}: {dev['name']}")

    fs = int(dev.get("default_samplerate", 44100))

    audio = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype="int16",
        device=device
    )
    sd.wait()

    write_wav(filename, fs, audio)
    print("✅ Áudio salvo:", filename)


def transcribe(path: str) -> str:
    segments, _ = whisper.transcribe(path, language="pt")
    text = " ".join(seg.text.strip() for seg in segments).strip()

    if len(text) < 3:
        return ""

    return text


def format_answer(found):
    if not found:
        return "Não encontrei um produto parecido. Tente dizer: Malbec, Floratta Red ou informe um preço máximo."

    return "Encontrei:\n" + "\n".join(
        f"{p.name} por R$ {p.price:.2f}".replace(".", ",")
        for p in found
    )


def main():
    CATALOG_PATH = "BOTICÁRIO - CICLO 06.pdf"

    # Carregar catálogo com tratamento de erro
    try:
        catalog = load_catalog_from_pdf(CATALOG_PATH)
        print(f"📦 Catálogo carregado: {len(catalog)} itens")
    except Exception as e:
        print("❌ Erro ao carregar catálogo:", e)
        speak("Não consegui carregar o catálogo.")
        return

    speak("Assistente pronto. Diga o que você procura.")

    fail_count = 0

    while True:
        # Captura e transcrição com proteção
        try:
            record_wav("user.wav", seconds=5, mic_id=MIC_ID)
            text = transcribe("user.wav")
        except Exception as e:
            print("❌ Erro de áudio:", e)
            speak("Tive um problema ao ouvir você. Tente novamente.")
            continue

        print(f"📝 Você disse: {text}")

        # Falha de entendimento
        if not text:
            fail_count += 1
            if fail_count >= 3:
                speak("Encerrando por falta de resposta.")
                break
            speak("Não entendi. Pode repetir?")
            continue

        fail_count = 0

        text = text.lower().strip().replace(".", "")
        
        # Interpretar intenção
        q = parse_query(text)

        if not q:
            speak("Não entendi o que você quis dizer.")
            continue

        #print(f"[INTENT] {q.intent} | keyword={q.keyword} | max_price={q.max_price}")

        # Sair
        if q.intent == "sair" or q.intent == "encerrar":
            speak("Encerrando. Até mais!")
            break
        
        # Fora do escopo
        if q.intent != "buscar":
            speak("Você pode pedir algo como Malbec, Floratta ou definir um preço máximo.")
            continue

        # Buscar produtos
        found = search_catalog(catalog, q.keyword, q.max_price)

        if not found:
            speak("Não encontrei produtos com esse critério.")
            continue

        # Resposta
        answer = format_answer(found)

        print(f"🤖 {answer}")
        speak(answer)

        print(f"🤖Quer buscar outro produto ou quer encerrar?")
        speak(f"🤖Quer buscar outro produto ou quer encerrar?")


if __name__ == "__main__":
    main()