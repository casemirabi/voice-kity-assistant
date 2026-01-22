from asyncio import sleep
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3

from faster_whisper import WhisperModel

from catalog_store import load_catalog, search_catalog
from intent import parse_query

MIC_ID = 11   # Grupo de microfones (Intel) WASAPI
OUT_ID = 10   # Alto-falantes (Realtek) WASAPI

whisper = WhisperModel("small", device="cpu", compute_type="int8")

def speak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

MIC_ID = 11
OUT_ID = 10

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

MIC_ID = 11   # Intel WASAPI input
OUT_ID = 10   # Realtek WASAPI output

def record_wav(filename: str = "user.wav", seconds: int = 5):
    dev = sd.query_devices(MIC_ID)
    fs = int(dev.get("default_samplerate", 48000))
    max_in = int(dev.get("max_input_channels", 0))

    print(f"🎙️ Input device {MIC_ID}: {dev.get('name')} | max_in={max_in} | fs={fs}")

    # Se max_in vier 0, a gente NÃO confia nele e tenta abrir mesmo assim com 1 ou 2 canais.
    # E força device no rec pra não usar default errado.
    for ch in ([max_in] if max_in in (1,2) else [1, 2]):
        try:
            print(f"   tentando gravar com channels={ch} ...")
            audio = sd.rec(
                int(seconds * fs),
                samplerate=fs,
                channels=ch,
                dtype="int16",
                device=MIC_ID
            )
            sd.wait()

            # converte para mono se vier stereo
            if ch > 1:
                audio = np.mean(audio, axis=1).astype("int16")

            write(filename, fs, audio)
            print("✅ Áudio salvo:", filename)
            return
        except Exception as e:
            print("   falhou:", repr(e))

    raise RuntimeError("Não consegui abrir o microfone. Verifique se o MIC_ID está correto e se não há apps usando o microfone.")



def transcribe(wav_path: str) -> str:
    segments, info = whisper.transcribe(wav_path, language="pt")
    text = " ".join(seg.text.strip() for seg in segments).strip()
    # se vier muito curto, trata como "não entendi"
    if len(text) < 4:
        return ""
    return text

def format_answer(found):
    if not found:
        return "Não encontrei nada com esses filtros. Quer tentar outro termo ou um preço máximo?"
    lines = []
    for p in found:
        price = f"R$ {p.price:.2f}".replace(".", ",")
        lines.append(f"{p.name} por {price}.")
    return "Encontrei: " + " ".join(lines) + " Quer que eu filtre por preço ou por nome?"

def main():
    catalog = load_catalog()
    print(f"📦 Catálogo carregado: {len(catalog)} itens")

    speak("Assistente pronto. Diga o que você procura. Você tem cinco segundos por tentativa.")

    while True:
        record_wav("user.wav", seconds=5)
        text = transcribe("user.wav")
        sleep(10)
        print("📝 Você disse:", text)

        if not text and text is None:
            speak("Não entendi. Pode repetir?")
            continue

        q = parse_query(text)

        if q.intent == "sair":
            speak("Encerrando. Até mais!")
            break

        '''
        if q.intent == "atualizar":
            speak("Para atualizar, rode o script kity_source_human e aperte enter quando a página carregar.")
            continue
        '''

        #if q.intent != "buscar":
        #    speak("Eu ajudo a buscar produtos. Diga, por exemplo: quero creme para olhos até cem reais.")
        #    continue

        found = search_catalog(catalog, keyword=q.keyword, max_price=q.max_price, limit=3)
        answer = format_answer(found)

        print("🤖", answer)
        speak(answer)

if __name__ == "__main__":
    main()
