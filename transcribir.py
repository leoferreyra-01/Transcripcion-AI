import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(file_path, output_path):
    # Convert M4A to WAV
    audio = AudioSegment.from_file(file_path, format="m4a")
    wav_path = "converted_audio.wav"
    audio.export(wav_path, format="wav")
    print ("Audio transformado a .wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    # Transcribe the audio file
    try:
        text = recognizer.recognize_google(audio_data, language="es-ES")
        print("Transcription: ")
        print(text)

        # Save the transcription to a text file
        with open(output_path, "w") as file:
            file.write(text)
        print(f"Transcription saved to {output_path}")

    except sr.UnknownValueError:
        print("Lo siento, no pude entender el audio.")
    except sr.RequestError as e:
        print(f"Error al solicitar los resultados del servicio de reconocimiento de Google; {e}")

if __name__ == "__main__":
    file_path = "./Charla con laura garutti.m4a"  # Reemplaza esto con la ruta a tu archivo M4A
    output_path = "/home/lferreyra/prueba-nico/transcripcion/transcripcion.txt"  # Ruta del archivo de salida
    transcribe_audio(file_path, output_path)
