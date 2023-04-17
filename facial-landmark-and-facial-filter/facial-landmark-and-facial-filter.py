import cv2
import numpy as np
import dlib
import os
# then create a variable pwd 
pwd = os.path.dirname(__file__)

webcam = True

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = detector(imgGray)
predictor = dlib.shape_predictor(pwd + "/shape_predictor_68_face_landmarks.dat")


    
        
def empty(a):
    pass
cv2.namedWindow("BGR")
cv2.resizeWindow("BGR", 640, 240)
cv2.createTrackbar("Blue", "BGR", 0, 255, empty)
cv2.createTrackbar("Green", "BGR", 0, 255, empty)
cv2.createTrackbar("Red", "BGR", 0, 255, empty)


def create_box(img, points, scale = 5, masked = False, cropped = True): # by default, scale = 5, masked = False, cropped = True
    if(masked):
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        img = cv2.bitwise_and(img, mask)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)
    if(cropped):
        bounding_box = cv2.boundingRect(points)
        x, y, w, h = bounding_box
        img_crop = img[y: y+h, x: x+w]
        img_crop = cv2.resize(img_crop, (0,0), None, scale, scale)
        return img_crop
    else:
        return mask


while True:

    if webcam: success_, img = cap.read()
    else: img = cv2.imread(pwd + "/2.PNG")
    # img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    img = cv2.resize(img, (0,0), None, 1, 1)
    imgOriginal = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(imgGray)
    # cv2.imshow("Original", imgOriginal)
    # cv2.waitKey(0)


    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        imgOriginal = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        landmarks = predictor(imgGray, face)
        myPoints = []
        for n in range(68): # among 68 face landmarks
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            myPoints.append([x, y])
            # cv2.circle(imgOriginal,  (x,y), 5, (50, 50, 255), cv2.FILLED)
            # cv2.putText(imgOriginal, str(n), (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1 ) # y-10 for little bit higher in y, # 0.8 is scale, # thickness is 1
        
        myPoints = np.array(myPoints)
        # for left eyes
        # img_left_eye = create_box(img, myPoints[36: 42]) # as in our predictor 36-41 belongs to left eye
        # cv2.imshow("left_eye", img_left_eye)
        # cv2.waitKey(0)

        # for lips
        img_lips = create_box(img, myPoints[48: 61], 3, masked = True) # black bg and untouched lips(pink original color)
        # img_lips = create_box(img, myPoints[48: 61], 3, masked = True, cropped = False) # black bg and white lips only
        cv2.imshow("lips", img_lips)
        # cv2.waitKey(0)
        # to color lips 
        img_color_lips = np.zeros_like(img_lips)
        
        b = cv2.getTrackbarPos('Blue', 'BGR')
        g = cv2.getTrackbarPos('Green', 'BGR')
        r = cv2.getTrackbarPos('Red', 'BGR')
        
        img_color_lips[:] = b, g, r
        img_color_lips = cv2.bitwise_and(img_lips, img_color_lips)
        # adding blurr to lips to make it more natural like
        img_color_lips = cv2.GaussianBlur(img_color_lips, (7, 7), 10)
        img_original_gray = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
        img_original_gray = cv2.cvtColor(img_original_gray, cv2.COLOR_GRAY2BGR)
        # img_color_lips = cv2.addWeighted(img_original_gray, 1, img_color_lips, 0.4, 0) 
        # img_color_lips = cv2.addWeighted(imgOriginal, 1, img_color_lips, 0.4, 0) 
        cv2.imshow("BGR", img_color_lips)

        cv2.imshow("Original", imgOriginal)
        cv2.waitKey(1)
        print(myPoints)


