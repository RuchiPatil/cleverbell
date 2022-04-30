import cv2 as cv2
import face_recognition

webcam_stream = cv2.VideoCapture(0)

# initializing empty array that holds the locations for faces detected
all_face_loc = []

while True:
    # get current frame
    ret, curr_frame = webcam_stream.read()
    # ret is a bool, that will be true when soemthing is returned from the read of the stream

    # make the frame smaller so that the computer can process it faster
    curr_frame_sm = cv2.resize(curr_frame, (0, 0), fx=0.25, fy=0.25)

    # now find all the locations bish
    # we want to use hog, since its faster
    # upsample is 1 for now
    all_face_loc = face_recognition.face_locations(curr_frame_sm, model='hog')

    for index, current_fac_loc in enumerate(all_face_loc):
        #print("inside for")
        # split tuple
        t_pos, r_pos, b_pos, l_pos = current_fac_loc
        t_pos = t_pos * 4
        r_pos = r_pos * 4
        b_pos = b_pos * 4
        l_pos = l_pos * 4

        # print('face @ {} at top:{}, right:{}, bottom:{}, left:{}'.format(index + 1, t_pos, r_pos, b_pos, l_pos))

        cv2.rectangle(curr_frame, (l_pos, t_pos), (r_pos, b_pos), (0, 0, 255), 2)
        cv2.imshow("webcam video", curr_frame)
        # print("after ")

    # press 'q' on keyboard to break true while
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the webcome from our clutches HAHAHAHAHAHA
webcam_stream.release()
cv2.destroyAllWindows()
