import cv2
import numpy as np
from panorama import stitch_panorama

cap = cv2.VideoCapture(0) 
images = []

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Video Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    # If the 'c' key is pressed, capture the current frame and store it in the images array
    if key == ord('c'): 
        print("Photo captured")
        images.append(frame)

    # If the 'q' key is pressed, exit the loop and start stitching
    elif key == ord('q'):
        print("Stitching images...")
        stitched_image = stitch_panorama(images) 
        
        # Show the stitched image
        cv2.imshow("Panorama", stitched_image)
        
        # Wait for any key press to close the stitched image
        cv2.waitKey(0)
        break

cap.release()
cv2.destroyAllWindows()
