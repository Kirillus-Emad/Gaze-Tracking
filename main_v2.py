import numpy as np
import cv2
import dlib
import pyglet
from math import hypot
import Keyboard_v2 as kb
from text_box import TextDisplayGUI
from threading import Thread


def gaze_tracking(blinking_rate,right_rate,center_rate):
    
    # Capture Video
    cap=cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor= dlib.shape_predictor(r"F:\New folder\AI Track\NAID\Project\project v2\shape_predictor_68_face_landmarks.dat")

    # get letters
    en_letters_1, en_letters_2, ar_letters_1, ar_letters_2, symbols_1, symbols_2, numbers=kb.get_letters()

    # sounds
    click_sound=pyglet.media.load(r'F:\New folder\AI Track\NAID\Project\project v2\click.m4a',streaming=False)
    left_sound=pyglet.media.load(r'F:\New folder\AI Track\NAID\Project\project v2\left.m4a',streaming=False)
    right_sound=pyglet.media.load(r'F:\New folder\AI Track\NAID\Project\project v2\right.m4a',streaming=False)

    def madpoint(p1,p2):
        return int((p1.x+p2.x)/2), int((p1.y+ p2.y)/2)


    def get_blinking_retio(eye_points, facial_landmarks):
        left_point= (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point= (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top= madpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom= madpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))

        hor_line_lenght=hypot((left_point[0]-right_point[0]),(left_point[1]-right_point[1]))
        ver_line_lenght =hypot((center_top[0]-center_bottom[0]),(center_top[1]-center_bottom[1]))
        ratio= hor_line_lenght/(ver_line_lenght+0.000001)
        
        return ratio



    def eyes_contour_points(facial_landmarks):
        left_eye = []
        right_eye = []
        for n in range(36, 42):
            x = facial_landmarks.part(n).x
            y = facial_landmarks.part(n).y
            left_eye.append([x, y])
        for n in range(42, 48):
            x = facial_landmarks.part(n).x
            y = facial_landmarks.part(n).y
            right_eye.append([x, y])
        left_eye = np.array(left_eye, np.int32)
        right_eye = np.array(right_eye, np.int32)
        return left_eye, right_eye

    def get_gaze_ratio(eye_points,gray,facial_landmarks):
        
        eye_region= np.array([ (facial_landmarks.part(eye_points[0]).x,facial_landmarks.part(eye_points[0]).y),
                                        (facial_landmarks.part(eye_points[1]).x,facial_landmarks.part(eye_points[1]).y),
                                        (facial_landmarks.part(eye_points[2]).x,facial_landmarks.part(eye_points[2]).y),
                                        (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y),
                                        (facial_landmarks.part(eye_points[4]).x,facial_landmarks.part(eye_points[4]).y),
                                        (facial_landmarks.part(eye_points[5]).x,facial_landmarks.part(eye_points[5]).y)], np.int32)
        
        height,width,_=frame.shape
        mask=np.zeros((height,width),np.uint8)
        
        cv2.polylines(mask, [eye_region], True,255,2)
        cv2.fillPoly(mask, [eye_region],255 )
        
        eye=cv2.bitwise_and(gray, gray,mask=mask)
        
        min_x = np.min(eye_region[:,0])
        max_x = np.max(eye_region[:,0])
        min_y = np.min(eye_region[:,1])
        max_y = np.max(eye_region[:,1])

        gray_eye=eye[min_y:max_y, min_x:max_x]
        
        # resize the eye as i want to capture good white and blackk numbers to enhance performance
        gray_eye=cv2.resize(gray_eye,None,fx=3,fy=3)
        
        _,threshold_eye= cv2.threshold(gray_eye,72,255,cv2.THRESH_BINARY)

        height,width=threshold_eye.shape
        left_side_threshold=threshold_eye[0:height, 0: int(width/2)]
        left_side_white=cv2.countNonZero(left_side_threshold)

        right_side_threshold=threshold_eye[0:height, int(width/2):width]
        right_side_white=cv2.countNonZero(right_side_threshold)
        
        gaze_ratio = left_side_white / (right_side_white + 0.0001) # if right_side_white != 0 else 0
            
        return gaze_ratio
    
    letter_index=0 # what is the current choosen letter
    blinking_frames=0  # how many frames i continusly blinked
    frames_to_blink=12 #  if we blink 12 frames --> choose this letter

    text=''

    keys_set=en_letters_1
    keyboard_selection_frames=0 # how many frames i stay to access left or right
    CAPS_button=False

    keyboard=kb.draw_keyboard()

    while True:
        _, frame = cap.read()
        rows,cols,_ = frame.shape
        # frames+=1
        keyboard[:] = (26,26,26)
        
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        # Draw a white space for loading bar
        frame[rows - 50: rows, 0: cols] = (255, 255, 255) 
           
        
        faces = detector(gray)
        
        for face in faces :

            landmarks = predictor(gray,face)

            left_eye,right_eye = eyes_contour_points(landmarks)
            
            #Detect Blinking
            left_eye_ratio=get_blinking_retio([36,37,38,39,40,41], landmarks)
            right_eye_ratio=get_blinking_retio([42,43,44,45,46,47], landmarks)
            blinking_ratio= (left_eye_ratio+right_eye_ratio)/2
            blinking_ratio=round(blinking_ratio,3)
            
            # # Eyes color
            # cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
            # cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)
            
            # detect Blinking
            if blinking_ratio>blinking_rate:

                blinking_frames+=1
                # frames-=1
                
                #Show green eyes when closed
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)
                
                if blinking_frames == frames_to_blink:
                    
                    if active_letter =='CAPS':
                        
                        if CAPS_button is True:
                            
                            CAPS_button=False
                            
                        else:
                            CAPS_button=True
                            
                    elif active_letter == 'ARB':
                        keys_set=ar_letters_1
                        letter_index=0
                        
                    elif active_letter =='ENG':
                        keys_set=en_letters_1
                        letter_index=0
                        
                    elif active_letter =='SYB':
                        keys_set=symbols_1
                        letter_index=0
                        
                    elif active_letter =='NUM':
                        keys_set=numbers
                        letter_index=0
                        
                    elif active_letter =='<--':
                        text=text[:-1]
                        
                    elif active_letter =='>>':  # go to second part of keyboard
                        
                        if keys_set == ar_letters_1:
                            keys_set=ar_letters_2
                            letter_index=0
                            
                        elif keys_set == en_letters_1:
                            keys_set=en_letters_2
                            letter_index=0
                            
                        elif keys_set == symbols_1:
                            keys_set=symbols_2
                            letter_index=0
                            
                    elif active_letter =='<<':  # go to second part of keyboard
                        
                        if keys_set == ar_letters_2:
                            keys_set=ar_letters_1
                            letter_index=0
                            
                        elif keys_set == en_letters_2:
                            keys_set=en_letters_1
                            letter_index=0
                            
                        elif keys_set == symbols_2:
                            keys_set=symbols_1
                            letter_index=0
                            
                    elif active_letter=='__':
                        text+=' '
                        
                    else:
                        if CAPS_button == True and (keys_set ==en_letters_1 or keys_set ==en_letters_2):
                            
                            text+=active_letter.upper()
                        else:
                            text+=active_letter
                            
                    click_sound.play()
                    
            else:
                blinking_frames = 0
                
            #Gaze Detection
            gaze_ratio_left_eye=get_gaze_ratio([36,37,38,39,40,41],gray ,landmarks)
            gaze_ratio_right_eye=get_gaze_ratio([42,43,44,45,46,47],gray ,landmarks)
            
            gaze_ratio=(gaze_ratio_right_eye+gaze_ratio_left_eye)/2

            if gaze_ratio<=right_rate:
                
                keyboard_selection_frames += 1
                
                # If Kept gaze on one side more than 10 frames, move to keyboard
                if keyboard_selection_frames == 10:
                    if letter_index == len(keys_set)-1 :
                        letter_index=0
                    else:
                        letter_index+=1
                        
                    right_sound.play()
                    #set frames count to zero when keyboard is selected.
                    
                    keyboard_selection_frames = 0
                    
            elif center_rate[0]<gaze_ratio<center_rate[1]:

                continue
            
            else:
                
                keyboard_selection_frames += 1
                
                # If Kept gaze on one side more than 15 frames, move to keyboard
                if keyboard_selection_frames == 10:

                    if letter_index == 0:
                        letter_index=len(keys_set)-1
                    else:
                        letter_index-=1
                        
                    left_sound.play()
                    
                    #set frames count to zero when keyboard is selected. 
                    keyboard_selection_frames = 0
                    
        
        active_letter=keys_set[letter_index]
                
        kb.draw_letters(keys_set,keyboard,letter_index)


        
        # Show the text we're writing on external GUI
        text_gui.update_text(text)
            
        # Blinking loading bar
        percentage_blinking = blinking_frames / frames_to_blink
        loading_x = int(cols * percentage_blinking)
        cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)
        
        cv2.imshow("Frame", frame)
        cv2.imshow("Virtual keyboard", keyboard)   
        
        key=cv2.waitKey(1)
        if key==27:
            break

    cap.release()
    cv2.destroyAllWindows()

# parameters of gaze_tracking
# you can edit them to be fit to your camera and your case in your favor way

blinking_ratio=6.29  # increase --> must close your eyes more

right_ratio_down_from=0.5 # ratio of how ratio you want to detect looking right, increase --> more bias to right
left_ratio_start_from=1.1 # ratio of how ratio you want to detect looking right, decrease --> more bias to left
center_ratio=[right_ratio_down_from,left_ratio_start_from] # ratio of how you make your program knows you look at center


# # Run gaze tracker in separate thread to make both GUI and main program run parallel
t = Thread(target=gaze_tracking,args=(blinking_ratio, right_ratio_down_from, center_ratio), daemon=True)
t.start()

text_gui = TextDisplayGUI()
text_gui.run()