import torch
import whisper
from pyannote.audio import Pipeline
from transformers import pipeline as hf_pipeline

print("🚀 Using device:", "cuda" if torch.cuda.is_available() else "cpu")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper
print("🔄 Loading Whisper model...")
whisper_model = whisper.load_model("base").to(device)
print("✅ Whisper loaded")

# Load Speaker Diarization
print("🔄 Loading Speaker Diarization model...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

pipeline.to(torch.device(device))
print("✅ Speaker diarization model loaded")

# Load Summarizer
print("🔄 Loading summarizer model...")
summarizer = hf_pipeline("summarization", model="facebook/bart-large-cnn", device=0 if device=="cuda" else -1)
print("✅ Summarizer loaded")


def process_audio(file_path):
    print("🎧 Running Whisper Transcription...")
    transcript = whisper_model.transcribe(file_path)["text"]

    print("👥 Running Speaker Diarization...")
    diarization = pipeline(file_path)

    speaker_segments = {}

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segment_text = transcript  # simplified mapping

        if speaker not in speaker_segments:
            speaker_segments[speaker] = segment_text
        else:
            speaker_segments[speaker] += " " + segment_text

    final_output = []

    for speaker, text in speaker_segments.items():
        print(f"📝 Generating summary for {speaker}")
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

        final_output.append({
            "speaker": speaker,
            "text": text,
            "summary": summary
        })

    return {
        "full_transcript": transcript,
        "speakers": final_output
    }
