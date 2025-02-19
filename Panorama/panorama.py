import numpy as np
import cv2 
import imutils

# images - an array of images to be stitched together
# yaw - a value from -3.14 rad to 3.14 rad representing direction (0 = North)
# requires compass.png to be in same directory
def stitch_panorama(images, yaw=None): 

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

        # no compass if yaw isn't inputed
        if (yaw = None): 
            return stitched_img

        # adding and rotating compass
        compass = cv2.imread("compass.png", cv2.IMREAD_UNCHANGED)
        # if compass is too small
        # compass_size = (450, 450)
        # compass = cv2.resize(compass, compass_size)

        center = (compass.shape[1] // 2, compass.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, np.degrees(yaw), 1)
        rotated_compass = cv2.warpAffine(compass, rotation_matrix, (compass.shape[1], compass.shape[0]))

        # positioning compass
        stitched_height, stitched_width = stitched_img.shape[:2]
        compass_height, compass_width = rotated_compass.shape[:2]
        x_offset = stitched_width - compass_width - 10 
        y_offset = stitched_height - compass_height - 10 

        if rotated_compass.shape[2] == 4:
            # split channels
            bgr_compass = rotated_compass[:, :, :3]
            alpha_compass = rotated_compass[:, :, 3]

            # create mask
            _, alpha_mask = cv2.threshold(alpha_compass, 1, 255, cv2.THRESH_BINARY)

            # region of interest
            roi = stitched_img[y_offset:y_offset + compass_height, x_offset:x_offset + compass_width]

            # mask to combine images
            masked_compass = cv2.bitwise_and(bgr_compass, bgr_compass, mask=alpha_mask)
            masked_roi = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(alpha_mask))

            # adding compass
            stitched_img[y_offset:y_offset + compass_height, x_offset:x_offset + compass_width] = cv2.add(masked_compass, masked_roi)
        else:
            # overlay directly if non-transparent
            stitched_img[y_offset:y_offset + compass_height, x_offset:x_offset + compass_width] = rotated_compass

        return stitched_img
        
    else:
        # can't find enough points to stitch photos together
        print("Images could not be stitched!")
        return None