
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
    catalog = load_catalog_from_pdf("BOTICÁRIO - CICLO 06.pdf")
    print(f"📦 Catálogo carregado: {len(catalog)} itens")

    speak("Assistente pronto. Diga o que você procura.")

    while True:
        record_wav("user.wav", seconds=5, mic_id=MIC_ID)

        text = transcribe("user.wav")
        print("📝 Você disse:", text)

        if not text:
            speak("Não entendi. Pode repetir?")
            continue

        q = parse_query(text)

        # ⚠️ sair vem primeiro
        if q.intent == "sair":
            speak("Encerrando. Até mais!")
            break

        if q.intent != "buscar":
            speak("Diga o nome de um produto. Por exemplo: Malbec ou Floratta Red.")
            continue

        found = search_catalog(catalog, q.keyword, q.max_price)

        answer = format_answer(found)

        print("🤖", answer)
        speak(answer)

        time.sleep(1)


if __name__ == "__main__":
    main()