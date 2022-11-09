import pickle as pkl
from sklearn.model_selection import GridSearchCV
import catboost
import math
import pygame


def model_start():
    with open('./src/model_api/model_11_07_CB4.pkl','rb') as f:
        model = pkl.load(f)
    return model

class moves_:
    def init():
        global m_start,r_start, list_x, list_y, list_z,movement_record, movings
        m_start = pygame.time.get_ticks()
        list_x, list_y, list_z,movement_record = [],[],[],[0]
        for k in range (478):
            list_x.append(0)
            list_y.append(0)
            list_z.append(0)


    def detect(results):
        global m_start,r_start, list_x, list_y, list_z,movement_record, movings
        m_passed = pygame.time.get_ticks() - m_start
        if m_passed > 100: 
            movement = 0
            delta = 0

            for id, lm in enumerate(results.multi_face_landmarks[0].landmark):
                delta_x = lm.x - list_x[id]
                #print("1")
                delta_y = lm.y - list_y[id]
                delta_z = lm.z - list_z[id]
                delta = round(math.sqrt((delta_x * delta_x) + (delta_y * delta_y)+ (delta_z * delta_z)),5) * 100
                movement += delta
                del list_x[id],list_y[id],list_z[id]
                list_x.insert(id,round(lm.x,5))
                list_y.insert(id,round(lm.y,5))
                list_z.insert(id,round(lm.z,5))
            movement = round(movement,5)
            m_passed = 0
            m_start = pygame.time.get_ticks()
            movement_record.append(movement)
        if len(movement_record) == 2: # 영상별로 첫 번째 움직임 데이터는 불필요하여 삭제
            del movement_record[1]
            movement_record.append(0)
        
        if len(movement_record) == 0:
            movings = 0
        else :
            movings = round(sum(movement_record)/len(movement_record),5)

        return movings


class face_angle_: 
    def init():
        global angle_records
        angle_records = [0]


    def detect(results):
        global angle_records
        Head_L = [round(results.multi_face_landmarks[0].landmark[127].x,5) , round(results.multi_face_landmarks[0].landmark[127].y,5)]
        Head_R = [round(results.multi_face_landmarks[0].landmark[356].x,5) , round(results.multi_face_landmarks[0].landmark[356].y,5)]

        x_cord = abs(Head_L[0]-Head_R[0])
        z_cord = abs(Head_L[1]-Head_R[1])
        angle = round(math.atan2(x_cord/z_cord,2),5)

        angle_records.append(angle)
        if len(angle_records) == 0:
            face_angle = 0
        else :
            face_angle = round(sum(angle_records)/len(angle_records),5)

        
        return face_angle


class face_off_: 
    def init():
        global off_records
        off_records = [0]


    def detect(image, results):
        global off_records
        shape = image.shape
        x_coord = round(results.multi_face_landmarks[0].landmark[1].x * shape[1],5)
        y_coord = round(results.multi_face_landmarks[0].landmark[1].y * shape[0],5)
     
        
        off_x = abs(x_coord-shape[1]/2)
        off_y = abs(y_coord-shape[0]/2)
        off_distance = round(math.sqrt((off_x * off_x) + (off_y * off_y)),5)
        off_records.append(off_distance)
        if len(off_records) == 0:
            come_off = 0
        else :
            come_off =round(sum(off_records)/len(off_records),5)

        
        return come_off
                           
                 #movement = rou

class emot_:
    def init():
        global emotion_list
        emotion_list = [[0] for k in range(7)]
        
    def detect(emotions):
        try:
            if emotion_list[6] != 0:
                for idx, data in enumerate(emotions[0]['emotions']):
                    emotion=round(emotions[0]['emotions'][data],5)
                    emotion_list[idx].append(emotion)

        except IndexError:
            pass
        if sum(emotion_list[6]) == 0: # 중립감정이 0만 뽑혔다면
            fer_result = [0,0,0,0,0,0,0]
        else :
            fer_result = [round((sum(i)/len(i)),5) for i in emotion_list]
        return fer_result