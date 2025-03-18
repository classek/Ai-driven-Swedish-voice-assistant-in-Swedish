Chatt med röst och text

Detta projekt är en interaktiv chattapplikation med stöd för både text- och röstinmatning. Applikationen använder Googles generativa AI-tjänst för att generera svar och text-till-tal (TTS) för att läsa upp svaren.

Funktioner

Textchatt: Skicka textmeddelanden och få svar från AI.

Röstchatt: Tala direkt till applikationen och få svar i både text och ljud.

Debug-loggar: Realtidsloggning av processer och API-respons.

Text-till-tal (TTS): Genererar och spelar upp ljudsvar.

Installation

Krav

Python 3.x

Pip (Python Package Installer)

Installera beroenden

Kör följande kommando för att installera alla nödvändiga paket:

pip install tkinter speechrecognition gtts pygame requests

API-nyckel

För att använda AI-tjänsten behöver du en API-nyckel från Google Gemini. Skapa eller ladda ner  api_key.json i projektets rotmapp med följande innehåll:

{
    "GEMINI_API_KEY": "DIN_API_NYCKEL_HÄR"
}

Googla Gemeni Api nyckel

Användning

Starta applikationen

Kör följande kommando:

python app.py

Gränssnitt

Skriv en fråga i textrutan och klicka "Skicka".

Tryck "Prata" och tala in din fråga via mikrofonen.

Svaret visas i chatten och kan spelas upp som ljud.

Teknisk information

Tkinter används för GUI.

SpeechRecognition används för röstigenkänning.

gTTS (Google Text-to-Speech) används för att skapa ljudsvar.

Pygame används för att spela upp ljud.

Requests används för API-anrop.

Felsökning

Kontrollera att api_key.json finns och innehåller en giltig API-nyckel.

Se till att mikrofonen fungerar och är korrekt konfigurerad.

Kontrollera att alla beroenden är installerade.
