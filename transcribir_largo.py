import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(file_path, segment_length=60000):  # Segment length in milliseconds (60000 ms = 1 min)
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path, format="m4a")
    duration = len(audio)
    transcripts = []

    for i in range(0, duration, segment_length):
        segment = audio[i:i+segment_length]
        segment.export("segment.wav", format="wav")

        with sr.AudioFile("segment.wav") as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data, language='es-ES')
                print(f"Segment {i // segment_length + 1}: {transcript}")
                transcripts.append(transcript)
            except sr.UnknownValueError:
                transcripts.append("[Inaudible]")
                print(f"Segment {i // segment_length + 1}: [Inaudible]")
            except sr.RequestError:
                transcripts.append("[Error]")
                print(f"Segment {i // segment_length + 1}: [Error]")

    return " ".join(transcripts)

file_path = './Charla con laura garutti.m4a'
output_path = "/home/lferreyra/prueba-nico/transcripcion/transcripcion_largo.txt"
transcription = transcribe_audio(file_path)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(transcription)

print(f"Transcription saved to {output_path}")
