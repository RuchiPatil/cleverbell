import urllib.request
import face_recognition
import json
import cv2


def get_encodings():
    known_face_encodings = []
    known_face_names = []

    # someones_face = face_recognition.load_image_file()

    with open('USERS/users.json', 'r') as file:
        data = json.load(file)

    for x in data:
        print(type(x['first_name']))
        print(x['image'])

        reco_image = face_recognition.load_image_file(x['image'])
        face_encoding = face_recognition.face_encodings(reco_image)[0]

        known_face_encodings.append(face_encoding)
        known_face_names.append(x['first_name'])

    print('list of known face encodings:' + str(known_face_encodings))
    print('list of known face names:' + str(known_face_names))

    return known_face_encodings, known_face_names


def get_image():

    webserver_path = 'http://192.168.2.120/saved-photo'
    captured_image = 'site_photo.jpg'
    # This line grabs the image from the webserver and saves in CWD as 'site_photo.jpg'
    urllib.request.urlretrieve(webserver_path, captured_image)


def compare(face_enc, name_enc):
    site_cap_image = 'site_photo.jpg'
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

    cv2.waitKey(0)
    cv2.destroyAllWindows()


f_enc = []
n_enc = []
f_enc, n_enc = get_encodings()
compare(f_enc, n_enc)


# loop through the json, for each name in users, create a face enconding

