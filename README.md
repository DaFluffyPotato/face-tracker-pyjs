# face-tracker-pyjs
## Heavily based on face-api.js!!! (also scuffed)

This collection of scripts uses both javascript and python because face-api.js was the best facial landmarking software I could find. I added some math on top of face-api.js to get the position/orientation data from the landmarks. This repository isn't a working codebase. It's a collection of the majority of the code I used (I gutted out some parts I don't want published). The code here provides much of the base functionality though.

*face-api.js is a client-side webbrowser based facial tracking library.*

See [face-api.js](https://github.com/justadudewhohacks/face-api.js) for more info.

## Features
- facial orientation tracking
- facial position tracking
- emotion tracking
- pygame 3D polygon rendering

## More Info

I modified the example code to forward the client-side tracking data to the node.js server, which then saves it to the `out.json` file. My python script then reads that file to generate the avatar.

If you run the example with the commands in the original repo, go to [http://localhost:3000/webcam_face_landmark_detection](http://localhost:3000/webcam_face_landmark_detection) to forward the data to the json file. The example was modified primarily for this page. It's also worth noting that I set the opacity of the video feed to 0 to prevent accidental face reveals.

The main script for rendering the avatar is `face_processor.py`. Please note that I gutted `face_processor.py` and `poly_3d.py` to remove my personal "model", so you'll have to modify it to make your own.
