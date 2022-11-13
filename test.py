# # import os

# # dir_path = os.getcwd()


# # video_path = []
# # dir_path = os.getcwd()
# # for (root, directories, files) in os.walk(dir_path):
# #     for file in files:
# #         if '.mp4' in file:
# #             file_path = os.path.join(root, file)
# #             file_path = file_path.replace(dir_path, '')
# #             video_path.append(file_path)

# # print(video_path)

# # print(type(True))
# # print(type(True)==bool)
# # print(bool(1))
# # print(bool(0))
# # print(bool(-1))
# # print(int(bool(None)))
# # print('playing' in 'playing')
# # print('abc' in 'abc')

# list =[0,1]
# t_list = [1,2,3,4,5,6]

# list[1] = 3

# print(list)

# list.append(i for i in t_list)

# print(list)

# import re

# list = 'asdasdfas 10'

# re_list = re.sub(r'[^0-9]', '', list)
# print(list)


convert_trigeredid_to_num = {}
for i in range(30):
    convert_trigeredid_to_num['stateSectionBtn {0}'.format(i)] = 'btn {0}'.format(i)

print(convert_trigeredid_to_num)

dic = {
    '1key' : { 'a' : 1, 'b' : 2},
    '2key' : {'a' : 3, 'b' : 4}
}

print(dic['1key']['a'])


list_1 = [1,2,3,4,5]
list_2 = [6,7,8,9,10]

list_3 = list_1 + list_2

print(list_3)
