# -*- coding: utf-8 -*-
import cv2
import time
#from matplotlib.pyplot import contour
import uuid
import threading
import random

'''
Modulation the code by 2 classes
'''
class radom_str:
    def __init__(self,randomLength = 8):
        self.randomLength = randomLength

    """
    生成一个指定长度的随机字符串
    """
    def generate_random_str(self, randomlength):
        # 1. Define a empty string
        random_str = ''
        # 2. Define the possible value
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        # 3. Generate a random string according to the length given
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

class train_image :
    def __init__(self,videoTime):
        self.videoTime = videoTime
        self.pre_frame = None  # 总是取前一帧做为背景（不用考虑环境影响）
        self.fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.size = (0,0)
        self.frame_list = []
        self.lastTime = time.time()
        self.dectTime = time.time()
        self.firstTime = time.time()
    '''
    def thread_job(self, imgList):
           filename = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
           #filename = generate_random_str(randomlength=16)
           filepath = '/home/pi/move/'
           fileadresse = '.avi'
           path = filepath + filename + fileadresse
           fourcc = cv2.cv.CV_FOURCC(*'XVID')
           out = cv2.VideoWriter(path,fourcc, 20.0, (640,480))
           print (len(imgList))
           for i in range (len(imgList)) :
               video.write (imgList[i])
           cv2.imwrite(filepath+filename+fileadresse, img)

    def initialization (self):
             # 1. Take the defaut video device as the source
            camera = cv2.VideoCapture(0)
            #camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,480)
            #camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,320)
            self.size = (int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
            print (self.size)
            # if the device can't be open, noticy the client
            if camera is None:
                print('check the connection to the camera')
                exit()
            return camera
    '''
    def analyFrame (self, camera):

            res, cur_frame = camera.read()
            if res != True:
                exit()
            # Turn the original picture to gray picture
            gray_img = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
            #gray_img = cv2.resize(gray_img, (500, 500))
            # Use Gaussian filtre to improve the accuracy
            gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)

            #
            rotated = self.rotImg(cur_frame)

            if self.pre_frame is None:
                #First time,program will take the first pickture as the reference
                pre_frame = gray_img
            else:
                #absdiff 差分，用于比较与背景的差别(pre_frame是背景) ，gray_img是当前帧
                img_delta = cv2.absdiff(self.pre_frame, gray_img)
                #图像二值化
                thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contourMax = 0
                for i in range(len(contours)):
                    if cv2.contourArea(contours[i]) > 500 and cv2.contourArea(contours[i])>=contourMax: # 设置敏感度
                        contourMax = contourArea(contours[i])
                        # cv2.drawContours(cur_frame,contours[i],-1,(0,255,0),2)
                        print("somethings moving here!!")
                        self.dectTime = time.time()
                        if (self.dectTime - self.lastTime)>1:
                            self.firstTime = self.dectTime
                        self.lastTime = self.dectTime
                    else:
                        continue
                if time.time()-self.firstTime < self.videoTime :
                    self.frame_list.append (rotated)
                else :
                    self.makeVideo(self.frame_list)
                    self.frame_list = []
            self.pre_frame = gray_img
            return rotated

    # 把图片向左转90度，室外摄像机角度不为正才做此操作
    def rotImg(self,cur_frame):
        (h, w) = cur_frame.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(cur_frame, M, (w, h))
        return rotated
    # Make the video by the n second frame_list
    def makeVideo(self, frame_list):
        print(len(frame_list))
        if (len(frame_list) > 0):
            filename = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
            out = cv2.VideoWriter(filename + '.avi', self.fourcc, 10.0, self.size)
            for frame in frame_list:
                out.write(frame)

    def showImg(self,rotated):
            cv2.imshow('img', rotated)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                return 0
            else :
                return 1

    def run (self) :
        camera = self.initialization()
        while 1 :
            img = self.analyFrame(camera)
            if self.showImg()==0 :
                break
        camera.release()
        cv2.destroyAllWindows()