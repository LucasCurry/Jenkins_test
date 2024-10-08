# -------------------------------------------------------------
# Importera bibliotek
# -------------------------------------------------------------
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# Variabler
# -------------------------------------------------------------

amplitude_points_float = []

# -------------------------------------------------------------
# Block 1: Initialisera
# -------------------------------------------------------------

def initialisera():
    # Initialiserar anslutningen till oscilloskopet och returnerar instrumentobjektet
    rm = pyvisa.ResourceManager()

    # Hämta alla tillgängliga resurser för att identifiera oscilloskopet anslutet via USB
    resurser = rm.list_resources()
    print("Tillgängliga resurser:", resurser)

    # Kontrollera att resurser finns
    if not resurser:
        raise ValueError("Inga resurser hittades. Kontrollera anslutningen.")

    # Anslut till första resurser i listan, eller specificera rätt adress om flera finns
    # OBS! Instrumentadressen kan förstås hårdkodas med sin adress
    instrument_adress = resurser[0]
    oscilloskop = rm.open_resource(instrument_adress)

    # Kontrollera att vi är anslutna till rätt instrument genom att fråga om ID
    idn = oscilloskop.query('*IDN?')
    print(f"Ansluten till: {idn}")

    # Ställ in timeout och avslutning för kommunikation
    oscilloskop.timeout = 5000
    oscilloskop.write_termination = '\n'
    oscilloskop.read_termination = '\n'

    oscilloskop.write(":RUN")
    oscilloskop.write(":WAV:FORM ASCII")  # För att hämta data i ASCII-format
    oscilloskop.write(":WAV:SOUR CHAN2")  # Välj kanal 2 (eller den kanal du använder)
    oscilloskop.write(":WAV:POINTS 1000")  # Antal punkter att hämta

    # Ofta behövs mer kod för att ställa in instrumentet inför mätning.
    # Exempel på ytterligare inställningar för oscilloskop är trig, kanal, tidsbas, ...
    # VIssa av dessa inställningar kan göras här, men man kan också behöva justera under mätningen.

    return oscilloskop

# -------------------------------------------------------------
# Block 2: Mätning
# -------------------------------------------------------------
amplitud = []
amplitud_float = []

def mata(oscilloskop):

    # Mät amplituden från oscilloskopets mätfunktion
    try:
        # Ger amplituddata
        raw_data = oscilloskop.query(":WAV:DATA?")

        # Ger frekvensdata
        frequency = float(oscilloskop.query(":MEASure:FREQuency? CHANnel2"))

        amplitude_points = [i for i in raw_data.split(',')]
        amplitude_points.pop(0)
        for i in range(len(amplitude_points)):
            amplitude_points[i].strip()

        for i in amplitude_points:
            amplitude_points_float.append(float(i))

        x_files = open('frekvens.csv', mode = 'w', encoding = 'UTF-8')
        x_files.write(str(frequency))
        x_files.close()

        file = open('amplituder.csv', mode = 'w', encoding = 'UTF-8')
        for i in amplitude_points:
            file.write(str(i) + ',')
        file.close()

        komp_data = list(np.fft.fft(amplitude_points_float))
        komp_data[0] = 0
        plt.plot(np.abs(komp_data[0:31]))
        plt.title('FFT')
        plt.xlabel('Frekvens (Hz)')
        plt.ylabel('Amplitud')
        plt.xticks(np.arange(0, 31, step=5), labels=[str(i*75) for i in range(7)])
        plt.yticks(np.arange(0, 500, step=500), labels=[str(i) for i in range(1)])
        plt.savefig('fft.png')

    except Exception as e:
        print(f"Misslyckades med att mäta amplitud: {e}")

    # Returnera den uppmätta amplituden
    return amplitud

def main():
    # Block 1: Initialisera
    try:
        oscilloskop = initialisera()
    except Exception as e:
        print(f"Initialisering misslyckades: {e}")
        return

    # Block 2: Mätning
    try:
        mata(oscilloskop)
    except Exception as e:
        print(f"Mätning misslyckades: {e}")
        return

    # Stäng anslutningen till oscilloskopet
    oscilloskop.close()

if __name__ == "__main__":
    main()
