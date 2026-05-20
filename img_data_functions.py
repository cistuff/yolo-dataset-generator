import numpy as np
import cv2

image_functions = []

# Add image modification functions to array
def register(func):
    image_functions.append(func)

# Distort image

@register
def bgr2rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

@register
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

@register
def gaussian_blur(image):
    return cv2.GaussianBlur(image, (15, 15), 0)  

@register
def median_blur(image):
    return cv2.medianBlur(image, 11)

@register
def bilateral_blur(image):
    return cv2.bilateralFilter(image, 15, 150, 150)

# Warp image

def warp_left(img):
    height, width = img.shape[:2]

    # specify input coordinates for corners of red quadrilateral in order TL, TR, BR, BL as x,
    input = np.float32([[0,0], [width, 0], [width, height], [0, height]])

    # specify output coordinates for corners of red quadrilateral in order TL, TR, BR, BL as x,
    output = np.float32([[0,height*.05-1], [width*.8-1,0], [width-1,height*.95-1], [width*.2-1,height-1]])

    matrix = cv2.getPerspectiveTransform(input, output)

    return cv2.warpPerspective(img, matrix, (width, height), cv2.INTER_LINEAR)
register(warp_left)

def warp_right(img):
    height, width = img.shape[:2]

    # specify input coordinates for corners of red quadrilateral in order TL, TR, BR, BL as x,
    input = np.float32([[0,0], [width, 0], [width, height], [0, height]])

    # specify output coordinates for corners of red quadrilateral in order TL, TR, BR, BL as x,
    output = np.float32([[width*.2-1,0], [width-1,height*.05-1], [width*.8-1,height-1], [0,height*.95-1]])

    matrix = cv2.getPerspectiveTransform(input, output)

    return cv2.warpPerspective(img, matrix, (width, height), cv2.INTER_LINEAR)
register(warp_right)

def warp_clockwise(img):
    warp_left(img)
    return cv2.rotate(warp_left(img), cv2.ROTATE_90_CLOCKWISE)
register(warp_clockwise)

def warp_counterclockwise(img):
    return cv2.rotate(warp_right(img), cv2.ROTATE_90_COUNTERCLOCKWISE)
register(warp_counterclockwise)

# Make image transparent

def transparent(img):
    # Convert image to image gray
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Applying thresholding technique
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

    # Use cv2.split() to split channels of colored image
    b, g, r = cv2.split(img)

    # Making list of Red, Green, Blue channels and alpha
    rgba = [b, g, r, alpha]

    # Using cv2.merge() to merge rgba into a coloured/multi-channeled image
    return cv2.merge(rgba, 4)

# Overlay image onto background function

def overlay_image(img, overlay_data):
    background_img = overlay_data['background_img']
    new_height = overlay_data['new_height']
    new_width = overlay_data['new_width']
    x_offset = overlay_data['x_offset']
    y_offset = overlay_data['y_offset']
    warp_type = overlay_data['warp_type']

    # Resize image
    img = cv2.resize(img, (new_height, new_width))

    # Warp image
    if warp_type == 'left':
        img = warp_left(img)
    elif warp_type == 'right':
        img = warp_right(img)
    elif warp_type == 'clockwise':
        img = warp_clockwise(img)
    elif warp_type == 'counterclockwise':
        img = warp_counterclockwise(img)

    y1, y2 = y_offset, y_offset + img.shape[0]
    x1, x2 = x_offset, x_offset + img.shape[1]

    alpha_s = img[:, :, 2] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background_img[y1:y2, x1:x2, c] = (alpha_s * img[:, :, c] + alpha_l * background_img[y1:y2, x1:x2, c])

    return background_img