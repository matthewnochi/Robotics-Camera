import cv2
import os
import time

cap = cv2.VideoCapture(0)  # Use 0 for webcam or adjust if using Raspberry Pi camera

if not os.path.exists('pictures'):
    os.makedirs('pictures')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show the frame
    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    # Break the loop on pressing 'q'
    if key == ord('q'):
        break

    # Take a picture on pressing 'p'
    if key == ord('p'):
        # Generate a filename using a timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f'pictures/photo_{timestamp}.jpg'

        # Save the frame as an image
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")

cap.release()
cv2.destroyAllWindows()
