import pickle as pkl
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import math
import pygame


def model_start():
    with open('./src/model_api/model.pkl','rb') as f:
        pickle = pkl.load(f)
        scalar = pickle[1]
        model = pickle[0]
    return scalar, model

class off_angle: 
    def init():
        global off_records, angle_records
        off_records = [0]
        angle_records = []

    def detect(image, face_mesh_results):
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            for id, lm in enumerate(face_landmarks.landmark):
                shape = image.shape
                landmark_x = int(lm.x * shape[1])
                landmark_y = int(lm.y * shape[0])
                if id == 1 :
                    Nose=[landmark_x,landmark_y]
                if id == 127 :
                    Head_L=[lm.x,lm.y]
                if id == 356 :
                    Head_R=[lm.x,lm.y]
        off_distance = abs(Nose[0]-shape[1]/2)
        off_records.append(off_distance)
        come_off = max(off_records)-min(off_records)
        
        
        x_cord = abs(Head_L[0]-Head_R[0])
        z_cord = abs(Head_L[1]-Head_R[1])
        angle = round(math.atan2(x_cord/z_cord,2),2)*90-50
        if angle >90:
            angle = 90
        if angle < 0 :
            angle = 0
        angle_records.append(angle)
        face_angle = round(sum(angle_records)/len(angle_records))

        
        return come_off, face_angle

class moves_ZX:
    def init():
        global mX_start,rX_start, list_xX, list_yX, movement_recordX
        mX_start = pygame.time.get_ticks()
        rX_start = pygame.time.get_ticks()
        list_xX, list_yX, movement_recordX = [],[],[0]
        for k in range (33):
            list_xX.append(0)
            list_yX.append(0)


    def detect(results):
        global mX_start
        mX_passed = pygame.time.get_ticks() - mX_start
        if mX_passed > 50: 
            movement = 0
            delta = 0
            num_landmark = 0
            i=0
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if lm.visibility > 0.7:
                    num_landmark +=1
                    delta_x = lm.x - list_xX[id]
                    delta_y = lm.y - list_yX[id]
                    delta = math.sqrt((delta_x * delta_x) + (delta_y * delta_y)) * 100
                    movement += delta
                else:
                    delta = 0
                del list_xX[id],list_yX[id]
                list_xX.insert(id,lm.x)
                list_yX.insert(id,lm.y)
            movement = movement/ num_landmark
            mX_passed = 0
            mX_start = pygame.time.get_ticks()
            movement_recordX.append(movement)
        if len(movement_recordX) == 2: # 영상별로 첫 번째 움직임 데이터는 불필요하여 삭제
            del movement_recordX[0]
            movement_recordX.append(0)
        movingX = round(sum(movement_recordX)/len(movement_recordX),3)
        return movingX
                            #movement = rou

class fer:
    def init():
        global angry_list, disgust_list, fear_list, happy_list, sad_list, surprise_list, neutral_list,emotion_list
        angry_list = [0]
        disgust_list = [0]
        fear_list = [0]
        happy_list = [0]
        sad_list = [0]
        surprise_list = [0]
        neutral_list = [0]
        emotion_list = [0,0,0,0,0,0,0]
        
    def detect(frame,emotions):
        try:
            for idx, data in enumerate(emotions[0]['emotions']):
                emotion=emotions[0]['emotions'][data]
                del emotion_list[idx]
                emotion_list.insert(idx,emotion)
            if emotion_list[6] != 0:
                angry_list.append(emotion_list[0])
                disgust_list.append(emotion_list[1])
                fear_list.append(emotion_list[2])
                happy_list.append(emotion_list[3])
                sad_list.append(emotion_list[4])
                surprise_list.append(emotion_list[5])
                neutral_list.append(emotion_list[6])
        except IndexError:
            pass
        if sum(neutral_list) == 0:
            fer_result = [0,0,0,0,0,0,0]
        else :
            fer_result = [sum(angry_list)/len(angry_list),sum(disgust_list)/len(disgust_list),sum(fear_list)/len(fear_list),sum(happy_list)/len(happy_list),sum(sad_list)/len(sad_list),sum(surprise_list)/len(surprise_list),sum(neutral_list)/len(neutral_list)]
        return fer_result

