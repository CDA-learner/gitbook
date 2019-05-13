# # coding:utf-8
#
# import cv2
#
#
# img_path = gb.glob("numbers\\*")
#
# k = 0
# labels = []
# samples =  []
#
# for path in img_path:
#     img  = cv2.imread(path)
#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray,(5,5),0)
#     thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
#     image, contours, hierarchy =cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#
# height,width = img.shape[:2]
#     w = width/5
#     rect_list = []
#     list1 = []
#     list2 = []
#     for cnt in contours:
#         #if cv2.contourArea(cnt)>100:
#         [x,y,w,h] = cv2.boundingRect(cnt)
#
#         if w>30 and h > (height/4):
#             if y < (height/2):
#                 list1.append([x,y,w,h])
#             else:
#                 list2.append([x,y,w,h])
#     list1_sorted = sorted(list1,key = lambda t : t[0])
#     list2_sorted = sorted(list2,key = lambda t : t[0])
#
#  for i in range(5):
#         [x1,y1,w1,h1] = list1_sorted[i]
#         [x2,y2,w2,h2] = list2_sorted[i]
#         number_roi1 = gray[y1:y1+h1, x1:x1+w1] #Cut the frame to size
#         number_roi2 = gray[y2:y2+h2, x2:x2+w2] #Cut the frame to size
#         resized_roi1=cv2.resize(number_roi1,(20,40))
#         thresh1 = cv2.adaptiveThreshold(resized_roi1,255,1,1,11,2)
#
#         resized_roi2=cv2.resize(number_roi2,(20,40))
#         thresh2 = cv2.adaptiveThreshold(resized_roi2,255,1,1,11,2)
# import one_hot_encoding as ohe


name = '7 7 3 0 _1555498788.png'
x='3 7 2 4 '
label = x[0]+x[2]+x[4]+x[6]
print(label)