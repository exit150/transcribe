from datetime import timedelta

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
