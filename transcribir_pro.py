import os
from pyannote.audio import Pipeline
from pydub import AudioSegment
import speech_recognition as sr

def diarize_audio(file_path):
    # Load pre-trained pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token="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")
    
    # Apply the pipeline to an audio file
    diarization = pipeline(file_path)
    
    # Save diarization results to a text file
    diarization_path = "diarization.txt"
    with open(diarization_path, "w") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.write(f"{turn.start:.1f} {turn.end:.1f} {speaker}\n")
    
    return diarization

def transcribe_segments(diarization, file_path):
    # Convert M4A to WAV
    audio = AudioSegment.from_file(file_path, format="m4a")
    wav_path = "converted_audio.wav"
    audio.export(wav_path, format="wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    audio_file = sr.AudioFile(wav_path)

    # Create a dictionary to hold the transcription for each speaker
    transcriptions = {}

    with audio_file as source:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # Extract audio segment
            start = int(turn.start * 1000)
            end = int(turn.end * 1000)
            segment = audio[start:end]
            segment.export("segment.wav", format="wav")

            # Transcribe the audio segment
            with sr.AudioFile("segment.wav") as segment_source:
                audio_data = recognizer.record(segment_source)
                try:
                    text = recognizer.recognize_google(audio_data, language="es-ES")
                    if speaker not in transcriptions:
                        transcriptions[speaker] = []
                    transcriptions[speaker].append(text)
                except sr.UnknownValueError:
                    transcriptions[speaker].append("[inaudible]")
                except sr.RequestError as e:
                    transcriptions[speaker].append(f"[error: {e}]")

    return transcriptions

def save_transcriptions(transcriptions, output_path):
    with open(output_path, "w") as f:
        for speaker, texts in transcriptions.items():
            f.write(f"Speaker {speaker}:\n")
            for text in texts:
                f.write(f"{text}\n")
            f.write("\n")

if __name__ == "__main__":
    file_path = "./Y2meta.m4a"  # Reemplaza esto con la ruta a tu archivo M4A
    diarization = diarize_audio(file_path)
    transcriptions = transcribe_segments(diarization, file_path)
    output_path = "/home/lferreyra/prueba-nico/transcripcion/transcripcion_pro.txt"  # Ruta del archivo de salida
    save_transcriptions(transcriptions, output_path)
    print(f"Transcription saved to {output_path}")
