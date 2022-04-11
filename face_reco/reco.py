# ruchi reco

import cv2
import face_recognition

test_file_loc = "images/test/grace_frankie_cast.jpg"
#load image to detect
og_image = cv2.imread(test_file_loc)
#load sample pic and extract face encodings
#return a list of 128-dimensional face encodings
#(one for each face in the image)
#we are getting the first face (assuming that there is only the one face)

#Image setup
jane_image = face_recognition.load_image_file("images/train/jane_fonda_1.jpg")
jane_face_encoding = face_recognition.face_encodings(jane_image)[0]

lily_image = face_recognition.load_image_file("images/train/lily_tomlin_1.jpg")
lily_face_encoding = face_recognition.face_encodings(lily_image)[0]

#Arrays to save encodings and to hold according labels
known_face_encodings = [jane_face_encoding, lily_face_encoding]
known_face_names = ["Jane Fonda", "Lily Tomlin"]

#load unkown image to idenitfy faces
image_to_reco = face_recognition.load_image_file(test_file_loc)

#find all the faces in UNKOWN IMAGE
all_face_locations = face_recognition.face_locations(image_to_reco, model="hog")
all_face_encodings = face_recognition.face_encodings(image_to_reco, all_face_locations)

print("{} faces found in total.".format(len(all_face_locations)))
#loop thru each location of found face and the face encodings found in unknown image
for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encodings):
    #split the tuple
    t_p, r_p, b_p, l_p = current_face_location
    
    #compare for face matches (based on known faces)
    #current_face_encodings refers to test image, known_face_enc refers to training images
    all_matches = face_recognition.compare_faces(known_face_encodings, current_face_encoding)
    
    #init an unkown name string
    person_name= "Unknown"
    
    #if match found, use first kind of name
    if True in all_matches:
        first_match_index = all_matches.index(True)
        person_name = known_face_names[first_match_index]
        
        #visual label
    cv2.rectangle(og_image, (l_p, t_p), (r_p, b_p), (255, 0, 0), 2)
    
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(og_image, person_name, (l_p, b_p), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Identified', og_image)


cv2.waitKey(0)
cv2.destroyAllWindows()
