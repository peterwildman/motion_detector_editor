import cv2, time




class video_motion_detector():

    def __init__(self):
        self.path = "C:\\test\\tesla_motion_detector\\"
        self.fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.out = cv2.VideoWriter((self.path + "out_test.avi"), self.fourcc, 24,(1280,960))

    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    def _capture_motion(self, video_file):
        self.video=cv2.VideoCapture(video_file)
        self._check = True
        self._first_frame = None
        while self._check:
            self._check, frame = self.video.read()
            
        
            self._status=0
            if self._check:
            
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                gray=cv2.GaussianBlur(gray,(21,21),0)
                if self._first_frame is None:
                    self._first_frame = gray
                    continue

                delta_frame=cv2.absdiff(self._first_frame,gray)
                thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
                thresh_frame= cv2.dilate(thresh_frame, None, iterations=2)

                (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in cnts:
                    if cv2.contourArea(contour) < 1000:
                        continue
                    self._status = 1
                    # (x,y,w,h)=cv2.boundingRect(contour)
                    # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

                cv2.imshow("Capturing", gray)
                cv2.imshow("Delta Frame",delta_frame)
                cv2.imshow("Threshold Frame",thresh_frame)
                cv2.imshow("Color Frame",frame)
                if self._status == 1:
                    self.out.write(frame)
                
                

            key = cv2.waitKey(1)
            if key ==ord('q'):
                break

    def _trim_videos(self, video_list):
        for video_file in video_list:
            print("video_file")
            self._capture_motion(video_file)  

    def _close_video_tools(self):     
        self.out.release()
        self.video.release()
        cv2.destroyAllWindows

    def main(self,video_file_list):
        self._trim_videos(video_file_list)
        self._close_video_tools()

vdm = video_motion_detector()
video_file_list=["front.mp4", "front2.mp4"]
vdm.main(video_file_list)
