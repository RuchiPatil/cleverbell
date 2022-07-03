import urllib.request
import face_recognition
import json
import cv2

'''
AI Module : Functions that perform detection and recognition; are
called by the scheduler
'''

# ----------------------------------------------------- GET ENCODINGS
def get_encodings():
    known_face_encodings = []
    known_face_names = []

    # someones_face = face_recognition.load_image_file()

    with open('USERS/users.json', 'r') as file:
        data = json.load(file)
    face

    for x in range(0, len(data)):
        print(x)
        reco_image = face_recognition.load_image_file(data[x]['image'])
        print(data[x]['image'])
        face_encoding = face_recognition.face_encodings(reco_image)[0]
        print(33)

        known_face_encodings.append(face_encoding)
        known_face_names.append(data[x]['first_name'])

    print('list of known face encodings:' + str(known_face_encodings))
    print('list of known face names:' + str(known_face_names))

    return known_face_encodings, known_face_names

# ------------------------------------------------------- COMPARE DETECTECTED
def compare(site_cap_image):

    face_enc, name_enc = get_encodings()

    #site_cap_image = 'site_photo.jpg'
    cv_site_cap_image = cv2.imread(site_cap_image)
    image_to_reco = face_recognition.load_image_file(site_cap_image)
    all_face_locations = face_recognition.face_locations(image_to_reco, model="hog")
    all_face_encodings = face_recognition.face_encodings(image_to_reco, all_face_locations)

    print("{} faces found in total.".format(len(all_face_locations)))
    for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encodings):
        # split the tuple
        t_p, r_p, b_p, l_p = current_face_location

        # compare for face matches (based on known faces)
        # current_face_encodings refers to test image, known_face_enc refers to training images
        all_matches = face_recognition.compare_faces(face_enc, current_face_encoding)

        # init an unknown name string
        person_name = "Unknown"

        # if match found, use first kind of name
        if True in all_matches:
            first_match_index = all_matches.index(True)
            person_name = name_enc[first_match_index]

            # visual label
        cv2.rectangle(cv_site_cap_image, (l_p, t_p), (r_p, b_p), (255, 0, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(cv_site_cap_image, person_name, (l_p, b_p), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Identified', cv_site_cap_image)

        return person_name
