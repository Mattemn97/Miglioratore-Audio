import os
import numpy as np
from pydub import AudioSegment, effects
from scipy.signal import butter, lfilter
from tqdm import tqdm
import noisereduce as nr

# ==================================================
# FILTRI & FUNZIONI TECNICHE
# ==================================================

# High-Pass Filter (per togliere rimbombi)
def highpass(data, sr, cutoff=80):
    b, a = butter(2, cutoff / (0.5 * sr), btype='high', analog=False)
    return lfilter(b, a, data)

# Low-Mid reduction (rimozione "scatola")
def remove_boxiness(data, sr, freq_low=200, freq_high=400, gain_db=-3):
    # banda di riduzione
    b, a = butter(
        2,
        [freq_low / (0.5 * sr), freq_high / (0.5 * sr)],
        btype='band'
    )
    filtered = lfilter(b, a, data)
    factor = 10 ** (gain_db / 20)
    return data + (filtered * factor)

# Boost intelligibilità (3–5 kHz)
def boost_presence(data, sr, freq_low=3000, freq_high=5000, gain_db=3):
    b, a = butter(
        2,
        [freq_low / (0.5 * sr), freq_high / (0.5 * sr)],
        btype='band'
    )
    boosted = lfilter(b, a, data)
    factor = 10 ** (gain_db / 20)
    return data + (boosted * factor)


# ==================================================
# FUNZIONE PRINCIPALE DI MIGLIORAMENTO AUDIO
# ==================================================
def auto_migliora_audio(in_path, out_path,
                        do_noise, do_eq, do_deesser, do_comp, do_sat, do_limit):

    audio = AudioSegment.from_file(in_path)
    sr = audio.frame_rate
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    # 1️⃣ Noise Reduction
    if do_noise:
        samples = nr.reduce_noise(y=samples, sr=sr)

    # 2️⃣ EQ (High-pass + Boxiness + Presence)
    if do_eq:
        samples = highpass(samples, sr)
        samples = remove_boxiness(samples, sr)
        samples = boost_presence(samples, sr)

    # 3️⃣ De-Esser (molto leggero)
    if do_deesser:
        # Riduce solo frequenze 5–8 kHz
        b, a = butter(2, [5000/(sr*0.5), 8000/(sr*0.5)], btype='band')
        ess = lfilter(b, a, samples)
        samples -= ess * 0.4

    # 4️⃣ Compressione
    if do_comp:
        audio = AudioSegment(
            samples.astype(np.int16).tobytes(),
            frame_rate=sr,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
        audio = effects.compress_dynamic_range(audio)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    # 5️⃣ Saturazione leggera
    if do_sat:
        samples = samples * 1.02
        samples = np.tanh(samples) * 32767

    # 6️⃣ Limiter
    if do_limit:
        peak = np.max(np.abs(samples))
        if peak > 0:
            samples = samples * (30000 / peak)

    # Riconversione finale
    out_audio = AudioSegment(
        samples.astype(np.int16).tobytes(),
        frame_rate=sr,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    out_audio.export(out_path, format="wav")


# ==================================================
# INTERFACCIA UTENTE (STILE MATTEO™)
# ==================================================
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🎧 ===========================================")
    print("        AUTO-MIGLIORAMENTO AUDIO PRO")
    print("=========================================== 🎧\n")

    print("Questo programma ottimizza automaticamente file audio,")
    print("applicando noise reduction, EQ, compressione, de-esser e limiter.\n")

    folder_src = input("📂 Cartella SORGENTE audio: ").strip('"')
    folder_dst = input("💾 Cartella DESTINAZIONE audio migliorato: ").strip('"')

    if not os.path.exists(folder_src):
        print("\n❌ Cartella sorgente non trovata.")
        return

    if not os.path.exists(folder_dst):
        os.makedirs(folder_dst)
        print("📁 Creata cartella destinazione.\n")

    # Scelte utente
    print("\n🔧 Quali miglioramenti applicare? [s/n]\n")
    do_noise   = input("   ➤ Noise Reduction: ").lower() == "s"
    do_eq      = input("   ➤ Equalizzazione (HPF + boxiness + presence): ").lower() == "s"
    do_deesser = input("   ➤ De-Esser: ").lower() == "s"
    do_comp    = input("   ➤ Compressore: ").lower() == "s"
    do_sat     = input("   ➤ Saturazione leggera: ").lower() == "s"
    do_limit   = input("   ➤ Limiter finale: ").lower() == "s"

    files = [f for f in os.listdir(folder_src)
             if f.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a'))]

    if not files:
        print("\n❌ Nessun file audio trovato.")
        return

    print(f"\n🎵 Trovati {len(files)} file audio. Inizio elaborazione...\n")

    for f in tqdm(files, ncols=100, desc="Elaborazione"):
        in_file = os.path.join(folder_src, f)
        name, ext = os.path.splitext(f)
        out_file = os.path.join(folder_dst, f"{name} - edit.wav")

        auto_migliora_audio(
            in_file, out_file,
            do_noise, do_eq, do_deesser, do_comp, do_sat, do_limit
        )

    print("\n✅ Tutti gli audio sono stati elaborati!")
    print(f"📁 File finali in: {folder_dst}")
    print("\nGrazie per aver usato l’audio-miglioratore di Matteo™ 😎")

# ==================================================
if __name__ == "__main__":
    main()
