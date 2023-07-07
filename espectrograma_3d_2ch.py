import matplotlib.pyplot as plt
import numpy as np
import librosa
import pyaudio

from mpl_toolkits.mplot3d import Axes3D

def calcular_espectrograma(audio_left, audio_right, sr):
    # Calcular el espectrograma de frecuencia
    Sxx_left = np.abs(librosa.stft(audio_left))
    Sxx_right = np.abs(librosa.stft(audio_right))
    Sxx_db_left = librosa.amplitude_to_db(Sxx_left, ref=np.max)
    Sxx_db_right = librosa.amplitude_to_db(Sxx_right, ref=np.max)

    # Obtener los valores de frecuencia y tiempo
    f = librosa.fft_frequencies(sr=sr)
    t = librosa.frames_to_time(np.arange(Sxx_left.shape[1]), sr=sr)

    # Mostrar los espectrogramas en 3D
    fig = plt.figure(figsize=(12, 8))
    ax_left = fig.add_subplot(121, projection='3d')  # Subplot para el canal izquierdo
    ax_right = fig.add_subplot(122, projection='3d')  # Subplot para el canal derecho

    T, F = np.meshgrid(t, f)
    ax_left.plot_surface(T.T, F.T, Sxx_db_left.T, cmap='inferno', edgecolor='none', alpha=0.7)
    ax_right.plot_surface(T.T, F.T, Sxx_db_right.T, cmap='inferno', edgecolor='none', alpha=0.7)

    ax_left.set_xlabel('Tiempo [s]')
    ax_left.set_ylabel('Frecuencia [Hz]')
    ax_left.set_zlabel('Amplitud [dB]')
    ax_left.set_title('Espectrograma Canal Izquierdo')

    ax_right.set_xlabel('Tiempo [s]')
    ax_right.set_ylabel('Frecuencia [Hz]')
    ax_right.set_zlabel('Amplitud [dB]')
    ax_right.set_title('Espectrograma Canal Derecho')

    plt.tight_layout()  # Ajustar el espacio entre subplots
    plt.show()

    return f, t, Sxx_left, Sxx_right

def capturar_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    DURACION = 20  # Duración de la captura de audio en segundos

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Capturando audio...")

    frames = []
    for i in range(0, int(RATE / CHUNK * DURACION)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finalizada la captura de audio.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio = audio.astype(np.float32) / np.iinfo(np.int16).max  # Convertir a punto flotante y escalar entre -1 y 1

    # Dividir el audio en canales izquierdo y derecho
    audio_left = audio[::2]
    audio_right = audio[1::2]

    return audio_left, audio_right, RATE

# Capturar audio del micrófono
audio_left, audio_right, sr = capturar_audio()

# Calcular espectrograma
f, t, Sxx_left, Sxx_right = calcular_espectrograma(audio_left, audio_right, sr)

