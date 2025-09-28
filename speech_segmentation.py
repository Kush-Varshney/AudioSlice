
import webrtcvad
from pydub import AudioSegment
import json
import os
import argparse

def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file and saves it as a WAV file.
    """
    print(f"Extracting audio from {video_path}...")
    audio = AudioSegment.from_file(video_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(audio_path, format="wav")
    print(f"Audio extracted and saved to {audio_path}")
    return audio_path

def detect_speech_segments(audio_path, aggressiveness=1):
    """
    Detects speech segments in an audio file using WebRTCVAD.
    """
    print(f"Detecting speech segments in {audio_path}...")
    audio = AudioSegment.from_wav(audio_path)
    vad = webrtcvad.Vad(aggressiveness)
    
    frame_duration_ms = 30  # VAD can handle 10, 20, or 30 ms frames
    frame_length = int(audio.frame_rate * (frame_duration_ms / 1000.0) * 2)
    
    speech_timestamps = []
    in_speech = False
    start_time = 0
    
    for i in range(0, len(audio.raw_data), frame_length):
        frame = audio.raw_data[i:i+frame_length]
        if len(frame) < frame_length:
            break
            
        is_speech = vad.is_speech(frame, audio.frame_rate)
        
        current_time = (i + frame_length / 2) / len(audio.raw_data) * audio.duration_seconds
        
        if not in_speech and is_speech:
            in_speech = True
            start_time = current_time
        elif in_speech and not is_speech:
            in_speech = False
            speech_timestamps.append({"start": start_time, "end": current_time})
            
    if in_speech:
        speech_timestamps.append({"start": start_time, "end": audio.duration_seconds})
        
    with open("speech_timestamps.json", "w") as f:
        json.dump(speech_timestamps, f, indent=2)
        
    print("Speech segments detected and saved to speech_timestamps.json")
    return speech_timestamps

def segment_and_export_clips(audio_path, timestamps, output_dir="segments"):
    """
    Segments an audio file into clips based on timestamps and exports them.
    """
    print(f"Segmenting audio and exporting clips to ./{output_dir}/ ...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    audio = AudioSegment.from_wav(audio_path)
    
    for i, segment in enumerate(timestamps):
        start_ms = segment["start"] * 1000
        end_ms = segment["end"] * 1000
        clip = audio[start_ms:end_ms]
        clip.export(os.path.join(output_dir, f"segment_{i+1:02d}.wav"), format="wav")
        
    print("Segmentation and export complete.")

def main():
    parser = argparse.ArgumentParser(description="Speech Segmentation from Audio")
    parser.add_argument("input_file", help="Input video or audio file")
    parser.add_argument("--aggressiveness", type=int, default=1, choices=[0, 1, 2, 3], help="VAD aggressiveness (0-3)")
    args = parser.parse_args()
    
    input_file = args.input_file
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return

    # 1. Extract Audio
    audio_path = "extracted_audio.wav"
    if input_file.endswith((".mp4", ".mov", ".avi", ".mkv")):
        extract_audio(input_file, audio_path)
    elif input_file.endswith((".wav", ".mp3", ".flac")):
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(audio_path, format="wav")
    else:
        print("Unsupported file format. Please provide a video or audio file.")
        return

    # 2. Detect Speech Segments
    timestamps = detect_speech_segments(audio_path, args.aggressiveness)
    
    # 3. Segment and Export Audio Clips
    segment_and_export_clips(audio_path, timestamps)

if __name__ == "__main__":
    main()
