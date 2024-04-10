import mediapipe as mp
import cv2

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

import os

# get the current working directory
current_working_directory = os.getcwd()
print(current_working_directory)

video = cv2.VideoCapture(0)

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()
    print(result.gestures)
    # cv2.imwrite('somefile.jpg', imright)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=current_working_directory+'\gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)

        if cv2.waitKey(5) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()