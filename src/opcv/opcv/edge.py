import cv2
import numpy as np

# Read the image
image = cv2.imread('slanted.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise and improve edge detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use the Canny edge detector to find edges
edges = cv2.Canny(blurred, 50, 150)

# Use the Hough Line Transform to detect lines in the edge map
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
print (lines)

# Draw the detected lines on a copy of the original image
image_with_lines = image.copy()

if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the original image, the edge map, and the result with detected lines
cv2.imshow('Original Image', image)
cv2.imshow('Edge Map', edges)
cv2.imshow('Image with Lines', image_with_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()
