import cv2

create_image_data_functions = []

def register(func):
    create_image_data_functions.append(func)

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