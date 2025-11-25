# 🎧 Miglioratore Automatico Audio (Noise Reduction, EQ, Compressore, De-Esser…)
Script Python per elaborare automaticamente file audio applicando una catena di miglioramento professionale della voce.
Progettato per essere semplice da usare, personalizzabile e con una procedura guidata da terminale, proprio come un piccolo "studio" automatico.

## ✨ Funzionalità principali
- 🧭 Interfaccia guidata da terminale, passo dopo passo
- 🎛️ Catena audio completa:
1. Noise Reduction
2. EQ (high-pass, pulizia boxiness, boost intelligibilità)
3. De-Esser
4. Compressore
5. Saturazione leggera
6. Limiter finale
- 🎚️ Parametri regolabili dall’utente
- 📊 Barra di progresso con tqdm
- 🔄 Elaborazione multipla in batch
- 💾 Output automatico in una cartella dedicata

## 🎵 Formati supportati

Lo script elabora i formati più comuni:
. ```.wav```
. ```.mp3```
. ```.flac```
. ```.ogg```
L’output viene salvato con suffisso ```-processed``` e stesso formato originale.

## ⚙️ Installazione
Assicurati di avere Python 3.8+ installato, quindi installa le dipendenze richieste:
```bash
pip install -r requirements.txt 
```
## 🧭 Utilizzo (modalità guidata)
Avvia lo script e segui le istruzioni nel terminale.
La procedura ti chiede:
- 📂 Percorso della cartella sorgente con i file audio
- 💾 Cartella di destinazione
- 🎚️ Quali effetti abilitare o disabilitare (Noise Reduction, EQ, De-Esser, ecc.)
- 🔊 Impostazioni personalizzate (opzionali)
- ▶️ Conferma finale ed elaborazione batch

## 🔧 Catena audio implementata
Lo script riproduce una catena di miglioramento vocale completa:

### 1️⃣ Noise Reduction
Riduce rumori di fondo stabili (ventole, fruscii, ronzio).

### 2️⃣ Equalizzazione
- High-pass a 80–100 Hz
- Riduzione “scatola” 250–400 Hz
- Boost intelligibilità 3–5 kHz

### 3️⃣ De-Esser
Attenua le sibilanti nella zona 4–8 kHz.

### 4️⃣ Compressione
Uniforma la dinamica e rende la voce più stabile.

### 5️⃣ Saturazione
Aggiunge presenza e un tocco “analogico”.

### 6️⃣ Limiter
Blocca i picchi e porta il livello finale a –1 dBFS.

## 📦 Output
Alla fine troverai nella cartella scelta:
- nomefile-processed.wav / .mp3 / ecc.
- Stesso formato dell’audio originale
- Volume, intelligibilità e pulizia nettamente migliorati

🧠 Suggerimenti
- Ottimo per podcast, voiceover, reel, contenuti social, presentazioni e conferenze.
- Per audio molto sporchi, attiva Noise Reduction + Noise Gate insieme.
- Se la voce suona troppo “spinta”, riduci compressione e saturazione.
- Consigliato registrare a 48 kHz per risultati più puliti.
