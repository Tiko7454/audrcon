import ffmpeg

# Define the duration of the recording in seconds
duration = 10

# Set up the FFmpeg command to record audio
ffmpeg.input('audio=Microphone').output('output.wav', t=duration).run()
