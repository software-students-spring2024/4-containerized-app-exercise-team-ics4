import mediapipe as mp
import cv2

# connect to pymongo
from pymongo import MongoClient
print("Connecting to Mongo...")
client = MongoClient("localhost", 27017)
print("Connected to Mongo!")
db = client.camera_live_feed
db['status'].drop() # clear past data

# initial status
obj = {
    "loading": True,
    "gesture": "",
    "confidence": 0
}
set_loading = False
collection = db.status
collection.insert_one(obj)
print("Added initial status.")

def update_gesture(gesture=None, confidence=None):
    update_data = {}
    if gesture is not None:
        update_data["gesture"] = gesture
    if confidence is not None:
        update_data["confidence"] = confidence
    collection.update_one({}, {"$set": update_data})

# set up recognizer
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# instantiate video
print("Starting video capture...")
video = cv2.VideoCapture(0)

# callback for live feed
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print(result.gestures)
    if(len(result.gestures) > 0):
        data = result.gestures[0][0]
        score = data.score
        category_name = data.category_name
        update_gesture(gesture=category_name, confidence=score)
        print("updated data!")

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

# main loop
timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()
        cv2.imshow("video", frame)
        if(set_loading==False):
            # done loading
            print("Done loading.")
            collection.update_one({"loading": True}, {"$set": {"loading": False}})
            set_loading=True

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(mp_image, timestamp)

        if cv2.waitKey(5) & 0xFF == 27:
            break

# cleanup
video.release()
cv2.destroyAllWindows()