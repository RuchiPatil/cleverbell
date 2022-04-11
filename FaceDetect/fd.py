# ruchi

import cv2
import face_recognition

image_to_detect = cv2.imread('tgp.jpg')
cv2.imshow("test", image_to_detect)

all_face_loc = face_recognition.face_locations(image_to_detect, model="hog")



#looping through face locs
for index, current_fac_loc in enumerate(all_face_loc):
    #split tuple
    t_pos, r_pos, b_pos, l_pos = current_fac_loc
    print('face @ {} at top:{}, right:{}, bottom:{}, left:{}'.format(index+1, t_pos, r_pos, b_pos, l_pos))
    cv2.rectangle(image_to_detect, (l_pos, t_pos), (r_pos, b_pos), (0,0,255), 2)
    cv2.imshow("count", image_to_detect)

cv2.waitKey(0)
cv2.destroyAllWindows()
print("{} face(s) in da pic".format(len(all_face_loc)))

