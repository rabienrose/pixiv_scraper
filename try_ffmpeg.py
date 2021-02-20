import ffmpeg
file="flask/static/pic/67435200_p0.jpg"
out_file="flask/static/pic/67435200_p0_small.jpg"
probe = ffmpeg.probe(file)
video_stream = probe["streams"][0]
width = int(video_stream['width'])
height = int(video_stream['height'])
if width>height:
    new_height=480
    new_width=int(height*(width/height))
else:
    new_width=480
    new_height=int(new_width*(height/width))
print(new_width)
print(new_height)
(
    ffmpeg
    .input(file)
    .filter('scale', new_width, new_height)
    .output(out_file)
    .run()
)
