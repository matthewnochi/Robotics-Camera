import cv2
import numpy as np
import base64
from panorama import stitch_panorama

# openCV image to base64 string
def encode_image(img):
    # encode to JPEG
    _, buffer = cv2.imencode('.jpg', img)

    # convert to bytes
    img_bytes = buffer.tobytes()
    return base64.b64encode(img_bytes).decode('utf-8')

cap = cv2.VideoCapture(0) 
images = []

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Video Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    # Capture current frame
    if key == ord('c'): 
        print("Photo captured")
        images.append(frame)

    # Exit the loop and start stitching
    elif key == ord('q'):
        print("Stitching images...")
        base64_images = [encode_image(img) for img in images]
        stitched_string = stitch_panorama(base64_images, 0) 

        img_data = base64.b64decode(stitched_string) # decode to bytes
        np_img = np.frombuffer(img_data, dtype=np.uint8) # convert to numpy array
        
        # Show the stitched image
        cv2.imshow("Panorama", cv2.imdecode(np_img, cv2.IMREAD_COLOR))
        
        cv2.waitKey(0)
        break

cap.release()
cv2.destroyAllWindows()
