from skimage import metrics
import numpy as np
import matplotlib.pyplot as plt
import cv2


e1 = cv2.getTickCount()

# Load images and convert to grayscale
image1 = cv2.imread('frame1.png')
image2 = cv2.imread('frame2.png')

shape = image1.shape
print(shape)

image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images
(score, diff) = metrics.structural_similarity(
    image1_gray, image2_gray, full=True)
img = 255 - (diff * 255).astype("uint8")

kernel = np.ones((10, 10), np.uint8)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
dilation = cv2.dilate(opening, kernel, iterations=10)
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

# Apply thresholding
ret, thresh1 = cv2.threshold(closing, 50, 255, cv2.THRESH_BINARY)

cv2.imwrite('diff.png', thresh1)

# Find contours in thresh_gray after closing the gaps
contours, hier = cv2.findContours(
    thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Draw the contours on the image
for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # draw a green rectangle to visualize the bounding rect
    cv2.rectangle(image2, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # draw point
    cv2.circle(image2, (x+w//2, y+h//2), 5, (0, 0, 255), -1)

e2 = cv2.getTickCount()
time = (e2 - e1) / cv2.getTickFrequency()

print("Time taken : {} seconds".format(time))

# show
cv2.imwrite('result.png', image2)
