import cv2

# Open the USB camera (0 for default camera)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture
ret, frame = camera.read()

if ret:
    # Save the frame
    cv2.imwrite('captured_image.jpg', frame)
    print("Image saved successfully.")
else:
    print("Error: Could not capture image.")

# Release the camera resource
camera.release()
cv2.destroyAllWindows()
