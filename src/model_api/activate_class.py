import pickle as pkl
import math
import datetime
#import pygame


def model_start():
    with open('./src/model_api/model_se.pkl','rb') as f:
        pickle = pkl.load(f)
    models = {'xgb' : pickle[0], 'rf' : pickle[1]}
    #return scalar, model
    return models


class moves_:
    def init():
        global m_start,r_start, list_x, list_y, list_z,movement_record
        # m_start = pygame.time.get_ticks()
        m_start = datetime.datetime.now()
        list_x, list_y, list_z,movement_record = [],[],[],[0]
        for k in range (33):
            list_x.append(0)
            list_y.append(0)
            list_z.append(0)


    def detect(results):
        global m_start,r_start, list_x, list_y, list_z,movement_record
        # m_passed = pygame.time.get_ticks() - m_start
        distance_t = datetime.datetime.now() - m_start
        m_passed = int(distance_t.total_seconds() * (10**6))
        if m_passed > 100: 
            movement = 0
            delta = 0
            num_landmark = 0
            i=0
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if lm.visibility > 0.7:
                    num_landmark +=1
                    delta_x = lm.x - list_x[id]
                    delta_y = lm.y - list_y[id]
                    delta_z = lm.z - list_z[id]
                    delta = round(math.sqrt((delta_x * delta_x) + (delta_y * delta_y)+ (delta_z * delta_z)),5) * 100
                    movement += delta
                else: 
                    delta = 0
                del list_x[id],list_y[id],list_z[id]
                list_x.insert(id,round(lm.x,5))
                list_y.insert(id,round(lm.y,5))
                list_z.insert(id,round(lm.z,5))
            movement = round(movement/ num_landmark,5)
            m_passed = 0
            # m_start = pygame.time.get_ticks()
            m_start = datetime.datetime.now()
            movement_record.append(movement)
        if len(movement_record) == 2: # 영상별로 첫 번째 움직임 데이터는 불필요하여 삭제
            del movement_record[0]
            movement_record.append(0)
        
        if len(movement_record) == 0:
            moving = 0
        else :
            moving = round(sum(movement_record)/len(movement_record),5)
        return moving

class face_angle_: 
    def init():
        global angle_records
        angle_records = [0]


    def detect(results):
        global angle_records
        Head_L = [round(results.pose_landmarks.landmark[7].x,5) , round(results.pose_landmarks.landmark[7].y,5)]
        Head_R = [round(results.pose_landmarks.landmark[8].x,5) , round(results.pose_landmarks.landmark[8].y,5)]

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
        x_coord = round(results.pose_landmarks.landmark[0].x * shape[1],5)
        y_coord = round(results.pose_landmarks.landmark[0].y * shape[0],5)
     
        
        off_x = abs(x_coord-shape[1]/2)
        off_y = abs(y_coord-shape[0]/2)
        off_distance = round(math.sqrt((off_x * off_x) + (off_y * off_y)),5)
        off_records.append(off_distance)
        if len(off_records) == 0:
            come_off = 0
        else :
            come_off =round(sum(off_records)/len(off_records),5)

        
        return come_off

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