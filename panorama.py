import numpy as np
import cv2 
import glob
import imutils

image_paths = glob.glob('pictures/*.jpg')
images = []

for img in image_paths:
    images.append(cv2.imread(img))

panorama = cv2.Stitcher_create()

error, stitched_img = panorama.stitch(images)

if not error:

    cv2.imwrite("Panorama.jpg", stitched_img)

    # adding border 10px black border
    stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))

    # convert to grayscale then threshold (black or white only)
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray, 0, 255 , cv2.THRESH_BINARY)[1] 

    # finding all black outlines
    contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # picking the biggest outline (assumed to be the photo)
    area = max(contours, key=cv2.contourArea)

    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(area) # finding the smallest rectangle from the countour
    cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    sub = mask.copy()
    # shrinking the mask until it fits perfectly
    while cv2.countNonZero(sub) > 0: 
        mask = cv2.erode(mask, None)
        sub = cv2.subtract(mask, thresh_img)

    # a second contour for cleaning up the mask after erosion 
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    area = max(contours, key=cv2.contourArea)

    # cropping original image
    x, y, w, h = cv2.boundingRect(area)
    stitched_img = stitched_img[y:y + h, x:x + w]

    cv2.imwrite("PanoramaProcessed.jpg", stitched_img)
    cv2.imshow("new", stitched_img)
    cv2.waitKey(0)

else:
    print("Images could not be stitched!")