import cv2


def compress(path,image, jpg_quality=None , png_compression = None):
    if jpg_quality:
        cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
    elif png_compression:
        cv2.imwrite(path, image,[int(cv2.IMWRITE_PNG_COMPRESSION), png_compression])
    else:
        cv2.imwrite(path, image)


def read_img(path):
    return cv2.imread(path)

def write_img(path,image):
    cv2.imwrite(path,image)