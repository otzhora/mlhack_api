from flask import Flask, escape, request
from flask_cors import CORS
import cv2 
import utils

import time

app = Flask(__name__, static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

links = {
    "lr_video_route": '',
    "hr_video_route": '',
    "future_hr_path": '',
    "name": ""
}

video_info = {}

@app.route('/video', methods=['POST'])
def post_video(): 
    video = request.files['file']
    video.save(f'./static/videos/lr_{video.filename}')
    links["lr_video_route"] = f'/videos/lr_{video.filename}'
    links["future_hr_path"] = f'/videos/hr_{video.filename}'

    lr_video = cv2.VideoCapture(f'./static/videos/lr_{video.filename}')
    video_info = {
        "fps": lr_video.get(cv2.CAP_PROP_FPS),
        "width": lr_video.get(cv2.CAP_PROP_FRAME_WIDTH),
        "height": lr_video.get(cv2.CAP_PROP_FRAME_HEIGHT),
        "name": video.filename
    }
    images = utils.FrameCapture(lr_video)

    # TODO SR
    hr_images = images

    utils.makevideo(hr_images, f'./static/videos/hr_{video_info["name"]}', video_info)
    links["hr_video_route"] = links["future_hr_path"]
    return "200"


@app.route('/hr_video', methods=['GET'])
def get_video():
    print(links["hr_video_route"], links["lr_video_route"])
    if(links["hr_video_route"] == '' or links["lr_video_route"] == ''):
        return "NO"
    
    return links
