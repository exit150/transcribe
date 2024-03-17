from datetime import timedelta
import whisper
import streamlit as st
from tempfile import NamedTemporaryFile


st.title("Whisper App")

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    st.audio(audio_file)

def segments_to_srt(segments):
    srt_content = ""  # Initialize an empty string to store the SRT content

    for segment in segments:
        startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
        endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segmentId = segment['id'] + 1
        segment_srt = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        srt_content += segment_srt  # Append each segment's SRT content to the main string

    print("SRT content generated successfully")
    return srt_content  # Return the accumulated SRT content directly


model = whisper.load_model("small.en")
st.success("Whisper model loaded")

if st.button("Generate Audio"):
    if audio_file is not None:
        st.write("Transcribing Audio")
        with NamedTemporaryFile(suffix="mp3") as temp:
            temp.write(audio_file.getvalue())
            temp.seek(0)
            transcription = model.transcribe(temp.name)
            st.success("Transcription complete")
            transcription_segments = transcription["segments"]
            srt = segments_to_srt(transcription_segments)
            st.code(srt)
    else:
        st.error("Please upload audio first")
