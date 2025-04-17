import cv2
import numpy as np

# Load an image
img = cv2.imread('invoices_as_images/654 Sign 20240683_page_1.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply denoising
denoised = cv2.fastNlMeansDenoising(gray, h=30)

# Apply binary threshold (you can also try adaptive thresholding for messy scans)
_, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Combine all contour points
    x, y, w, h = cv2.boundingRect(np.vstack(contours))

    # Draw rectangle on original for visualization (optional)
    preview = img.copy()
    cv2.rectangle(preview, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Before Cropping", preview)

    # Crop image
    cropped_img = img[y:y+h, x:x+w]
    cv2.imshow("After Cropping", cropped_img)

    cropped_img_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Cropped Grayscale", cropped_img_gray)
    cv2.imwrite("cropped_invoice_gray.jpg", cropped_img_gray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No content found in image.")