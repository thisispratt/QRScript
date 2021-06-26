from flask import Flask, render_template, jsonify, request,send_file
import qrcode
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip
from moviepy.video.fx.all import resize
from PIL import Image
from os import remove


app = Flask(__name__)

def generate_QR(data, limit=1000, type_="<NOTE>"):
	qr_content = []
	i = 0
	l = len(data)
	while i <= l:
		qr_content.append(data[i:i+limit])
		i=i+limit
	n_qr = len(qr_content)
	qr = []
	for i in range(n_qr):
		prefix = type_ + str(i+1) + "/" + str(n_qr) + "\n"
		qr_content[i] = prefix + qr_content[i]
		im = qrcode.make(qr_content[i])
		im = im.resize((1290, 1290))
		rgbimg = Image.new("RGB", im.size)
		rgbimg.paste(im)
		path = "%s.jpg" % str(i+1)
		for j in range(3):
			qr.append(path)
		rgbimg.save(path, format=im.format)		
	return qr

@app.route("/", methods=["GET", "POST"])
def home():
	if request.method == "GET":
		return render_template("home.html")
	else:
		data = request.form.get("data")
		video = request.files.get("video")
		video.save("video.mp4")
		qr_codes = generate_QR(data)
		clip = ImageSequenceClip(qr_codes, durations=[5]*len(qr_codes), with_mask=False,fps=1)
		clip1 = VideoFileClip("video.mp4")
		clip1 = resize(clip1, (1290, 1290))
		final_clip = concatenate_videoclips([clip1, clip], method="compose")
		final_clip.write_videofile("result.mp4")
		for path in set(qr_codes):
			remove(path)
		return send_file("result.mp4", mimetype="video/*", as_attachment=True)

if __name__ == "__main__":
	app.run()

"""		
	

clip = ImageSequenceClip(["1.jpg", "2.jpg", "3.jpg"]*5, durations=[5,5,5]*5, with_mask=False,fps=1)
#clip.write_videofile("video2.mp4",fps=1)

clip1 = VideoFileClip("video1.mp4")
#clip2 = VideoFileClip("video2.mp4")
clip1 = resize(clip1, (1290, 1290))
final_clip = concatenate_videoclips([clip1, clip], method="compose")
final_clip.write_videofile("result.mp4")
"""
