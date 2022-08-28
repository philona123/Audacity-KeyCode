import cv2
import numpy as np
from a import wall_extraction
from main import detectItems

def fill(img, origin, corners, coord):
    # origin = [origin[0]+coord[0], origin[1]+coord[1]]
    corners = sorted(corners, key = lambda K: (origin[0]-K[0])**2 + (origin[1]-K[1])**2)
    a = round(min(list(map(lambda x: x[0], corners[:4]))))
    b = round(min(list(map(lambda x: x[1], corners[:4]))))
    c = round(max(list(map(lambda x: x[0], corners[:4]))))
    d = round(max(list(map(lambda x: x[1], corners[:4]))))
    img[b:d, a:c] = 255
    return img

def process_image(filename):

    objects = detectItems(filename)    
    img = cv2.imread(filename)
    # cv2.imwrite('modified_img.jpg',img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    # img = cv2.imread('modified_img.jpg')
    img = wall_extraction(img)
    cv2.imwrite('output/extracted.png',img)

    new_img = cv2.imread('output/extracted.png', cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    dst = cv2.cornerHarris(gray,5,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    for i in objects:
        if i['item'] == 'window':
            new_img = fill(new_img, i['origin'], corners, i['coordinates'])

    element1 = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    eroded = cv2.erode(new_img,element1)
    thinned = cv2.ximgproc.thinning(cv2.cvtColor(eroded, cv2.COLOR_RGB2GRAY))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))
    thickened = cv2.dilate(thinned, element2)
    skelton = cv2.erode(thickened,element1)
    cv2.imwrite('output/filled.png',skelton)
