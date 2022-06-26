import image_processing
from arduino_comm import arduino_comm
from kivy.logger import Logger
import time
class Main_logic():
    def __init__(self):
        self.state_dict = dict()
        self.run_flag = True
        self.current_state = 0 # if -1 the find color , if 0 then start program

        self.FORWARD = b'F'
        self.BACKWARD = b'B'
        self.RIGHT = b'R'
        self.LEFT = b'L'
        self.STOP = b'S'
        self.PICK = b'K'
        self.PLACE = b'E'
        self.SOFT_RIGHT1 = b'G'
        self.SOFT_LEFT1 = b'T'
        self.SOFT_RIGHT2 = b'Q'
        self.SOFT_LEFT3 = b'W'
        self.SOFT_RIGHT3 = b'Y'
        self.SOFT_LEFT3 = b'U'


        self.low_color = [31 , 64 , 100]
        self.high_color = [37 , 255,255]

        self.low_color_pink = [170,120,110]
        self.high_color_pink = [177,205,255]

        self.time_to_pick = None

        self.state_dict[-1] = image_processing.find_color
        self.state_dict[0] = self.start
        self.state_dict[1] = self.detect_ball
        self.state_dict[2] = self.go_to_ball
        self.state_dict[3] = self.pick_ball
        self.state_dict[4] = self.detect_drop_location
        self.state_dict[5] = self.go_to_drop_location
        self.state_dict[6] = self.place_ball
        self.state_dict[7] = self.end

        self.count = 0

    def main_logic(self,image):
        Logger.info(f"Image Processing: im main_logic " + str(self.current_state))

        image_processing.state = str(self.current_state)
        # if self.count==3:
        #     self.count+=1
        #     image = self.state_dict[self.current_state](image)
        #     self.count = 0
        image = self.state_dict[self.current_state](image)
        return image

    def start(self,image):
        #do nothing
        # send command to make all things rest 
        # if run_flag is True start the process else do nothing
        image , coordinates = image_processing.detect_ball(image , self.low_color , self.high_color )
        
        if self.run_flag == True:
            # send stop and make arm at rest
            arduino_comm.send_date(self.STOP)
            arduino_comm.send_date(self.PLACE)
            self.current_state+=1
        else:
            # send stop and make arm at rest
            arduino_comm.send_date(self.STOP)
            arduino_comm.send_date(self.PLACE)
        return image

    def detect_ball(self , image):
        # move round to detect ball, when found stop,change state
        # move right till you detect the color contour
        # if found stop and change state
        image , coordinates = image_processing.detect_ball(image , self.low_color , self.high_color)
        if coordinates == (-1,-1,-1,-1):
            arduino_comm.send_date(self.RIGHT)
        else:
            arduino_comm.send_date(self.STOP)
            self.current_state +=1
        return image

    def go_to_ball(self , image):
        image , coordinates = image_processing.detect_ball(image , self.low_color , self.high_color )
        if coordinates == (-1,-1,-1,-1):
            self.current_state = 1 # go to detect ball
        else:
            x,y,w,h = coordinates
            motion_in_x = True
            motion_in_y = True

            ## motion in y direction
            if x<185:
                arduino_comm.send_date(self.SOFT_LEFT1)
            elif x>215:
                arduino_comm.send_date(self.SOFT_RIGHT1)
            else:
                motion_in_y = False
            
                ## motion in x direction
                if w < 150 or y < 490: 
                    arduino_comm.send_date(self.FORWARD)
                else:
                    motion_in_x = False

            if not motion_in_x and not motion_in_y:
                arduino_comm.send_date(self.STOP)
                self.current_state +=1
                self.time_to_pick = time.time()
        return image

    def pick_ball(self,image):
        # pick ball, WAIT IN THIS STATE FOR SOME TIME - 1 sec
        image , coordinates = image_processing.detect_ball(image , self.low_color , self.high_color )

        if time.time() - self.time_to_pick>2:
            self.current_state +=1
        else:
            arduino_comm.send_date(self.PICK)
        return image

    def detect_drop_location(self,image):
        #move in circle and detect the drop location
        number_of_countors = 1 # no of objects to detect
        Logger.info(f"in Detect Drop Location " + str(self.current_state))
        image , coordinates = image_processing.detect_ball(image , self.low_color_pink , self.high_color_pink )
        Logger.info(f"cordinates " + str(coordinates))
        if coordinates == (-1,-1,-1,-1): ##if no object rotate right
            arduino_comm.send_date(self.RIGHT)
            Logger.info(f"right turn to find drop location " + str(self.current_state))
        else:
            arduino_comm.send_date(self.STOP)
            self.current_state +=1
            Logger.info(f"Drop location- stop " + str(self.current_state))
        return image

    def go_to_drop_location(self, image):
        #move towards drop location
        number_of_countors = 1 # no of objects to detect
        Logger.info(f"in Go to drop location " + str(self.current_state))
        image , coordinates = image_processing.detect_ball(image , self.low_color_pink , self.high_color_pink)
        if coordinates == (-1,-1,-1,-1):
            self.current_state = 4 # go to detect ball
        else:
            x,y,w,h = coordinates
            Logger.info(f"cordinates " + str(coordinates))
            motion_in_x = True
            motion_in_y = True

            ## motion in y direction
            if x<170:
                arduino_comm.send_date(self.SOFT_LEFT1)
                Logger.info(f"In motion in y diretion: x<170 " + str(self.current_state))
            elif x>200:
                arduino_comm.send_date(self.SOFT_RIGHT1)
                Logger.info(f"In motion in y diretion: x>200 " + str(self.current_state))
            else:
                motion_in_y = False
            
                ## motion in x direction
                if w < 100: # test and change the logic
                    arduino_comm.send_date(self.FORWARD)
                else:
                    motion_in_x = False

            if not motion_in_x and not motion_in_y:
                arduino_comm.send_date(self.STOP)
                self.current_state +=1
                self.time_to_drop = time.time()
        return image

    def place_ball(self,image):
        #place ball by CHECKING DISTANCE , IF MORE THAN A VALUE THAN PLACED.
        number_of_countors = 1 # no of objects to detect
        image , coordinates = image_processing.detect_ball(image , self.low_color_pink , self.high_color_pink )
        if time.time() - self.time_to_drop>2:
            self.current_state +=1
            
        else:
            arduino_comm.send_date(self.PLACE)

            self.time_to_reverse = time.time()
            # x1,y1,w1,h1 = coordinates[0]
            # x2,y2,w2,h2 = coordinates[1]

            # image_processing.debug = "DIST = "+ str(abs(x1 - x2))
            # if abs(x1 - x2)>= 2500:
            #     self.current_state+=1
            # else:
            #     arduino_comm.send_date(self.PLACE)
        return image
    def end(self , image):
        # do nothing ,send no data

        image , coordinates = image_processing.detect_ball(image , self.low_color_pink , self.high_color_pink )

        if time.time() - self.time_to_reverse>2:
            arduino_comm.send_date(self.STOP)
        else:
            arduino_comm.send_date(self.BACKWARD)
        return image

main_logic = Main_logic()