from json import detect_encoding
#from tkinter import ROUND
from detecto import core, utils
from detecto.visualize import show_labeled_image
import matplotlib as plt
import cv2
import numpy as np      

"""
*Constants
*
*
*
"""
#Items list
DOOR = "door"
WINDOW = "window"
BASIN = "basin"
ROUNDTABLE = "roundTable"
BED = "bed"

#Thresholds
THRESHOLD_DOOR = 11

IMG_URL = 'data7/file_2.jpg' #for testing only

"""
*Required Functions
*
*
"""
def find_orient(img, coord, offset):
        coord = coord.numpy()
        coord = coord.astype(int)
        coord = coord.tolist()
        #coord = [587, 335, 690, 441]
        p1 = [coord[0], coord[0]+offset, coord[1], coord[1]+offset]
        p2 = [coord[0], coord[0]+offset, coord[3]-offset, coord[3]]
        p3 = [coord[2]-offset, coord[2], coord[1], coord[1]+offset]
        p4 = [coord[2]-offset, coord[2], coord[3]-offset, coord[3]]
        s=[]
        s.append(sum(map(sum,img[p1[2]:p1[3],p1[0]:p1[1]])))
        s.append(sum(map(sum,img[p2[2]:p2[3],p2[0]:p2[1]])))
        s.append(sum(map(sum,img[p3[2]:p3[3],p3[0]:p3[1]])))
        s.append(sum(map(sum,img[p4[2]:p4[3],p4[0]:p4[1]])))
        min_pts = sorted(s)[:2]
        positions = {s.index(min_pts[0]), s.index(min_pts[1])}
        if positions == {0,1}:
                return 'right'
        elif positions == {1,2}:
                return 'bottom'
        elif positions == {2,3}:
                return 'left'
        else:
                return 'top'
def distanceBetweenPoint(pt1,pt2):
        (x1,y1) = pt1
        (x2,y2) = pt2

        return (abs(x2-x1)+abs(y2-y1))

def lengthWidthFinder(tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])
        
        if(abs(b-d) > abs(a-c)):
                length = round(abs(b-d))
                width = round(abs(a-c))
        else:
                length = round(abs(a-c))
                width = round(abs(b-d))

        return (length, width) #length will always be largest

def originFinder(tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        x_cord = round(abs((a-c)//2)) #p
        y_cord = round(abs((b-d)//2))#q
        x_cord_orgin_added = x_cord + a
        y_cord_origin_added = y_cord + b
        cord = (x_cord_orgin_added, y_cord_origin_added)

        return cord
#Function to find sum of values of a pixel's neighbouring pixels
def sumFilter(img,x,y):
        sum_of_filter = 0
        for i in range(x-THRESHOLD_DOOR,x+THRESHOLD_DOOR):
                for j in range(y-THRESHOLD_DOOR, y+THRESHOLD_DOOR):
                        sum_of_filter += img[i,j]
        return sum_of_filter

def orientationDoor(img, tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        A_sum_filter = sumFilter(img,a,b)
        B_sum_filter = sumFilter(img,c,b)
        C_sum_filter = sumFilter(img,c,d)
        D_sum_filter = sumFilter(img,a,d)

        if(A_sum_filter>B_sum_filter and B_sum_filter>D_sum_filter):
                return "top"
        elif(C_sum_filter>D_sum_filter and D_sum_filter>A_sum_filter):
                return "bottom"
        elif(B_sum_filter>C_sum_filter and C_sum_filter>A_sum_filter):
                return "right"
        else:
                return "left"
def orientationDoorv2(img, tensor):
        #imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgGrey = img
        #thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        temp_list=[]
        for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
                x = approx.ravel()[0]
                y = approx.ravel()[1] - 5
                if len(approx) == 4:
                        x1 ,y1, w, h = cv2.boundingRect(approx)
                        # aspectRatio = float(w)/h
                        # print(aspectRatio)
                        # if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                        #         cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                        # else:
                        #         cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))        
                        temp_list.append((x1,y1))
        
def orientationDoorv3(img, tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])


def orientationDoorv3(img, tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        new_img = img[b:d, a:c]
        # cv2.imshow('new_img',new_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        gray=new_img
        dst = cv2.cornerHarris(gray,5,3,0.04)
        dst = cv2.dilate(dst,None)
        ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

        A_point = (a,b)
        B_point = (c,b)
        C_point = (c,d)
        D_point = (a,d)

        A_distance = 0
        B_distance = 0
        C_distance = 0
        D_distance = 0

        for point in corners:
                A_distance += distanceBetweenPoint((point[0]+a,point[1]+c), A_point)
                B_distance += distanceBetweenPoint((point[0]+a,point[1]+c), B_point)
                C_distance += distanceBetweenPoint((point[0]+a,point[1]+c), C_point)
                D_distance += distanceBetweenPoint((point[0]+a,point[1]+c), D_point)

        
        if(A_distance >B_distance and B_distance>D_distance):
                return "top"
        elif(D_distance >C_distance and C_distance>A_distance):
                return "bottom"
        elif(A_distance >D_distance and D_distance>B_distance):
                return "left"
        else:
                return "right"
        
        # res = np.hstack((centroids,corners))
        # res = np.int0(res)
        # new_img[res[:,1],res[:,0]]=[0,0,255]
        # new_img[res[:,3],res[:,2]] = [0,255,0]
        # cv2.imshow("image",new_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def orientationWindow(tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        if(abs(b-d)>abs(a-c)):
                return "vertical"
        else:
                return "horizontal"

def orientationBed(img, tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        if(abs(b-d)>abs(a-c)):
                #vertical
                sum_top = 0
                sum_bottom = 0
                for i in range (b, (d-b)//2):
                        for j in range (a, c):
                                sum_top += img[j,i]
                for i in range ((d-b)//2, d):
                        for j in range (a, c):
                                sum_bottom += img[j,i]
                if (sum_top < sum_bottom):
                        return "top"
                else:
                        return "bottom"

        else:
                #horizontal
                sum_left = 0
                sum_right = 0
                for i in range (a, (a-c)//2):
                        for j in range (b, d):
                                sum_left += img[i,j]
                for i in range ( (a-c)//2, c):
                        for j in range (b, d):
                                sum_right += img[i,j]
                if (sum_left < sum_right):
                        return "left"
                else:
                        return "right"


def orientationBasin(img, tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        A_sum_filter = sumFilter(img,a,b)
        B_sum_filter = sumFilter(img,c,b)
        C_sum_filter = sumFilter(img,c,d)
        D_sum_filter = sumFilter(img,a,d)

        if((A_sum_filter<C_sum_filter)and(A_sum_filter<D_sum_filter)and(B_sum_filter<C_sum_filter)and(B_sum_filter<D_sum_filter)):
                return "top"
        elif((B_sum_filter<A_sum_filter)and(B_sum_filter<D_sum_filter)and(C_sum_filter<A_sum_filter)and(C_sum_filter<D_sum_filter)):
                return "right"
        elif((D_sum_filter<A_sum_filter)and(D_sum_filter<B_sum_filter)and(C_sum_filter<A_sum_filter)and(C_sum_filter<B_sum_filter)):
                return "bottom"
        else:
                return "left"
def orientationFinder(item, tensor, img):
        if(item == DOOR):
                # return orientationDoorv3(img, tensor)
                return find_orient(img, tensor, THRESHOLD_DOOR)
        elif(item == WINDOW):
                return orientationWindow(tensor)
        elif(item == BED):
                return orientationBed(img, tensor)
        elif(item==BASIN):
                return orientationBasin(img, tensor)
        else:
                return "none"

def coordinatePointsFetch(tensor):
        tensor_ar = tensor.numpy()
        tensor_ar =tensor_ar.astype(int)
        a = int(tensor_ar[0])
        b = int(tensor_ar[1])
        c = int(tensor_ar[2])
        d = int(tensor_ar[3])

        return [a,b,c,d]

def detectItems(file_name):
        #LOADING MODEL
        model = core.Model.load('model_weights4.pth', [DOOR, WINDOW, ROUNDTABLE, BED,BASIN])
        model_2 = core.Model.load('model_weights2.pth', [DOOR, WINDOW, ROUNDTABLE, BED,BASIN])
        #req_img = cv2.imread(IMG_URL) #FOR VISUALISATION ONLY
        image = utils.read_image(file_name) 	
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_size = np.shape(image)[0:2] #extracting after removing nuumber of channels

        #PREDICTING
        predictions = model.predict(image)
        predictions_2 = model_2.predict(image)
        labels, boxes, scores = predictions
        labels_2, boxes_2, scores_2 = predictions_2


        #initialising list to empty list
        item_list = []
        number_of_items = len(labels)
        number_of_items_2 = len(labels_2)
        
        for i in range(number_of_items):
                #initialising dict to store an item detail
                if(labels[i] != 'door' and scores[i].item()>=0.9): 
                        #print(labels[i]," ",scores[i]," ",boxes[i])
                        item_info = {}
                        length, width = lengthWidthFinder(boxes[i])
                        origin = originFinder(boxes[i])
                        item = labels[i]

                        item_info["imageSize"] = img_size
                        item_info["item"] = item
                        item_info["length"] = length
                        item_info["width"] = width
                        item_info["origin"] = origin
                        item_info["orientation"] = orientationFinder(item, boxes[i], image_grey)
                        item_info["coordinates"] = coordinatePointsFetch(boxes[i])

                        item_list.append(item_info)
        for i in range(number_of_items_2):
                if(labels_2[i] == 'door'):
                        item_info = {}
                        length, width = lengthWidthFinder(boxes_2[i])
                        origin = originFinder(boxes_2[i])
                        item = labels_2[i]

                        item_info["imageSize"] = img_size
                        item_info["item"] = item
                        item_info["length"] = length
                        item_info["width"] = width
                        item_info["origin"] = origin
                        item_info["orientation"] = orientationFinder(item, boxes_2[i], image_grey)
                        item_info["coordinates"] = coordinatePointsFetch(boxes_2[i])

                        item_list.append(item_info)


        return item_list

if (__name__ == '__main__'):
        item_list = detectItems(IMG_URL)
        for item in item_list:
                print(item)