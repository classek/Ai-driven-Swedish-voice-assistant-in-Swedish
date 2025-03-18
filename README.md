Chatt med Röst och Text

Detta är ett Python-projekt som skapar en interaktiv chattapplikation med både text- och röstinmatning. Applikationen använder Googles Text-to-Speech (gTTS) för att generera tal, Gemini API för att generera svar, och har ett inbyggt debugfönster för att visa detaljerad loggning i realtid.

Funktioner
Textinmatning: Skriv en fråga och få svar som både visas och läses upp.
Röstinmatning: Använd mikrofonen för att ställa frågor med röstigenkänning på svenska.
Talsyntes: Svar omvandlas till tal med gTTS för en naturligare upplevelse.
Debugloggar: Realtidsloggning av API-svarstider, HTTP-status, ljudgenerering och mer i ett dedikerat fönster.
API-nyckelhantering: Läser API-nyckeln från en JSON-fil (api_key.json).
Skärmdump
(Lägg till en skärmdump här om du har en, t.ex. via GitHubs bilduppladdning)

Krav
För att köra projektet behöver du följande bibliotek:

Python 3.6+
tkinter (vanligtvis förinstallerat med Python)
speechrecognition
gtts
requests
pygame
