import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
import os
import requests
import json
import threading
import time
import pygame
import re

# Funktion för att logga debuginformation live
def logga_debug(meddelande):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    debug_info = f"[{timestamp}] {meddelande}\n"
    print(debug_info.strip())
    root.after(0, lambda: debug_text.insert(tk.END, debug_info))
    root.after(0, lambda: debug_text.see(tk.END))

# Funktion för att läsa API-nyckel från JSON-fil
def ladda_api_nyckel(filnamn="api_key.json"):
    try:
        start_time = time.time()
        with open(filnamn, 'r') as fil:
            data = json.load(fil)
        laddningstid = round((time.time() - start_time) * 1000, 2)
        api_key = data.get("GEMINI_API_KEY")
        if not api_key:
            logga_debug(f"Fel: Ingen 'GEMINI_API_KEY' hittades i {filnamn}")
            return None
        logga_debug(f"API-nyckel laddades från {filnamn} efter {laddningstid} ms")
        return api_key
    except FileNotFoundError:
        logga_debug(f"Fel: Filen {filnamn} hittades inte")
        return None
    except json.JSONDecodeError as e:
        logga_debug(f"Fel: Ogiltig JSON i {filnamn}: {str(e)}")
        return None
    except Exception as e:
        logga_debug(f"Fel vid laddning av {filnamn}: {str(e)}")
        return None

# Funktion för att rensa och förbereda text för mer naturligt tal
def rens_text(text):
    text = re.sub(r'[\*|_]+', '', text)
    text = re.sub(r'#+', '', text)
    text = text.replace(".", ".  ").replace("!", "!  ").replace("?", "?  ")
    text = re.sub(r'\s+', ' ', text).strip()
    logga_debug(f"Rensad och förberedd text för TTS: {text}")
    return text

# Funktion för att spela upp ljud med pygame
def spela_upp_ljud(fil):
    try:
        start_time = time.time()
        pygame.mixer.init()
        pygame.mixer.music.load(fil)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        uppspelningstid = round((time.time() - start_time) * 1000, 2)
        logga_debug(f"Ljudfil {fil} spelades upp framgångsrikt. Uppspelningstid: {uppspelningstid} ms")
        os.remove(fil)
        logga_debug(f"Ljudfil {fil} raderades")
    except Exception as e:
        logga_debug(f"Fel vid ljuduppspelning: {str(e)}")
        root.after(0, lambda: chat_fonster.insert(tk.END, f"Fel vid ljuduppspelning: {str(e)}\n"))

# Funktion för att generera ljudfil
def generera_ljudfil(svar):
    try:
        start_time = time.time()
        rensat_svar = rens_text(svar)
        filnamn = f"svar_{int(time.time())}.mp3"
        tts = gTTS(text=rensat_svar, lang='sv', slow=True)
        tts.save(filnamn)
        genereringstid = round((time.time() - start_time) * 1000, 2)
        logga_debug(f"Ljudfil genererad: {filnamn}. Genereringstid: {genereringstid} ms")
        return filnamn
    except Exception as e:
        logga_debug(f"Fel vid ljudgenerering: {str(e)}")
        root.after(0, lambda: chat_fonster.insert(tk.END, f"Fel vid ljudgenerering: {str(e)}\n"))
        return None

# Funktion för att spela upp svar som tal
def spela_svar(svar):
    filnamn = generera_ljudfil(svar)
    if filnamn:
        threading.Thread(target=spela_upp_ljud, args=(filnamn,)).start()

# Funktion för att skicka API-förfrågan med detaljerad debug
def skicka_fraga(prompt):
    api_key = ladda_api_nyckel("api_key.json")
    if not api_key:
        logga_debug("Fel: Ingen giltig API-nyckel kunde laddas.")
        root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Ingen giltig API-nyckel kunde laddas.\n"))
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    if not prompt:
        logga_debug("Fel: Vänligen ange en fråga!")
        root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Vänligen ange en fråga!\n"))
        return None

    laddnings_label = tk.Label(root, text="Laddar...", font=("Arial", 12), bg="#f0f0f0")
    laddnings_label.pack(pady=5)
    root.update()

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        start_time = time.time()
        logga_debug(f"Skickar API-förfrågan med prompt: {prompt}")
        response = requests.post(url, headers=headers, json=data)
        response_time = round((time.time() - start_time) * 1000, 2)
        response.raise_for_status()
        response_data = response.json()

        logga_debug(f"Svarstid: {response_time} ms")
        logga_debug(f"HTTP-status: {response.status_code}")
        logga_debug("Full API-respons:")
        logga_debug(json.dumps(response_data, indent=2, ensure_ascii=False))

        candidates = response_data.get("candidates")
        if not candidates:
            logga_debug("Fel: Inget svar genererat av API:et.")
            root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Inget svar genererat av API:et.\n"))
            return None

        content = candidates[0].get("content")
        if not content:
            logga_debug("Fel: Inget innehåll i svaret från API:et.")
            root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Inget innehåll i svaret från API:et.\n"))
            return None

        parts = content.get("parts")
        if not parts:
            logga_debug("Fel: Inga delar i svaret från API:et.")
            root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Inga delar i svaret från API:et.\n"))
            return None

        svar = parts[0].get("text", "Inget svar genererat.")
        logga_debug(f"Genererat svar: {svar}")
        return svar

    except requests.exceptions.RequestException as e:
        fel_tid = round((time.time() - start_time) * 1000, 2) if 'start_time' in locals() else 0
        logga_debug(f"Fel uppstod efter {fel_tid} ms: {str(e)}")
        logga_debug(f"HTTP-status: {response.status_code if 'response' in locals() else 'Okänt'}")
        root.after(0, lambda: chat_fonster.insert(tk.END, f"Fel: Ett fel uppstod: {str(e)}\n"))
        return None
    finally:
        laddnings_label.destroy()

# Funktion för att lyssna på röstinmatning med debug
def lyssna():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as källa:
            logga_debug("Lyssnar på röstinmatning...")
            root.after(0, lambda: chat_fonster.insert(tk.END, "\n[Du pratar...]\n"))
            start_time = time.time()
            r.adjust_for_ambient_noise(källa)
            justeringstid = round((time.time() - start_time) * 1000, 2)
            logga_debug(f"Justering av bakgrundsljud klar efter: {justeringstid} ms")
            try:
                start_time = time.time()
                ljud = r.listen(källa, timeout=10)
                lyssningstid = round((time.time() - start_time) * 1000, 2)
                logga_debug(f"Ljud inspelat efter: {lyssningstid} ms")
                start_time = time.time()
                text = r.recognize_google(ljud, language='sv-SE')
                igenkänningstid = round((time.time() - start_time) * 1000, 2)
                logga_debug(f"Röstigenkänning lyckades efter {igenkänningstid} ms: {text}")
                root.after(0, lambda: chat_fonster.insert(tk.END, f"Du: {text}\n"))
                svar = skicka_fraga(text)
                if svar:
                    root.after(0, lambda: chat_fonster.insert(tk.END, f"Bot: {svar}\n\n"))
                    spela_svar(svar)
            except sr.UnknownValueError:
                logga_debug("Röstigenkänning misslyckades: Okänt värde.")
                root.after(0, lambda: chat_fonster.insert(tk.END, "Jag förstod inte vad du sa.\n"))
            except sr.RequestError as e:
                logga_debug(f"Röstigenkänning misslyckades: {str(e)}")
                root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Problem med röstigenkänningstjänsten.\n"))
    except sr.Microphone.MicrophoneError:
        logga_debug("Fel: Kunde inte hitta eller använda mikrofonen.")
        root.after(0, lambda: chat_fonster.insert(tk.END, "Fel: Kunde inte använda mikrofonen.\n"))

# Funktion för att hantera textinmatning
def skicka_text():
    text = prompt_text.get("1.0", tk.END).strip()
    if text:
        logga_debug(f"Textinmatning: {text}")
        root.after(0, lambda: chat_fonster.insert(tk.END, f"Du: {text}\n"))
        prompt_text.delete("1.0", tk.END)
        svar = skicka_fraga(text)
        if svar:
            root.after(0, lambda: chat_fonster.insert(tk.END, f"Bot: {svar}\n\n"))
            spela_svar(svar)

# Skapa huvudfönstret
root = tk.Tk()
root.title("Chatt med röst och text")
root.geometry("1000x800")
root.configure(bg="#f0f0f0")

# Skapa chattfönster (övre delen)
chat_label = tk.Label(root, text="Chatt", font=("Arial", 12, "bold"), bg="#f0f0f0")
chat_label.pack(pady=5)
chat_fonster = scrolledtext.ScrolledText(root, height=20, width=80, state=tk.NORMAL, bg="#ffffff", font=("Arial", 12))
chat_fonster.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

# Skapa debugfönster (nedre delen)
debug_label = tk.Label(root, text="Debug Loggar", font=("Arial", 12, "bold"), bg="#f0f0f0")
debug_label.pack(pady=5)
debug_text = scrolledtext.ScrolledText(root, height=10, width=80, state=tk.NORMAL, bg="#f0f0f0", font=("Arial", 10))
debug_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

# Skapa ram för inmatning och knappar
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=5, fill=tk.X)

# Skapa textruta för inmatning
prompt_text = tk.Text(input_frame, height=2, width=60, bg="#ffffff", font=("Arial", 12))
prompt_text.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

# Skapa knappar
skicka_knapp = tk.Button(input_frame, text="Skicka 📧", command=skicka_text, bg="#4CAF50", fg="black")
skicka_knapp.pack(side=tk.LEFT, padx=5)

lyssna_knapp = tk.Button(input_frame, text="Prata 🎤", command=lyssna, bg="#008CBA", fg="black")
lyssna_knapp.pack(side=tk.LEFT, padx=5)

# Starta Tkinter-loopen
root.mainloop()
