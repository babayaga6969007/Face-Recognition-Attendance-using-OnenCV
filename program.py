
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import os

# initializing video capture
video_capture = cv2.VideoCapture(0)

# loaingd known face images and encodings
known_faces = {
    "KP Baa Don": face_recognition.face_encodings(face_recognition.load_image_file("photos/kp_baa.jpg"))[0],
    "Balen Dai": face_recognition.face_encodings(face_recognition.load_image_file("photos/balen.jpg"))[0],
    "Kaju Wala": face_recognition.face_encodings(face_recognition.load_image_file("photos/rishi.jpg"))[0],
    "Devashish": face_recognition.face_encodings(face_recognition.load_image_file("photos/devashish.jpg"))[0],
    
}

# Initialize lists and variables
known_faces_names = list(known_faces.keys())
students = known_faces_names.copy()
face_locations = []
face_encodings = []
face_names = []

# create CSV file with headers if it doesn't exist
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_file = f"{current_date}.csv"
if not os.path.isfile(csv_file):
    with open(csv_file, "w", newline="") as f:
        lnwriter = csv.writer(f)
        lnwriter.writerow(["Student's Name", "Date", "Time"])

# open CSV file for appending
with open(csv_file, "a", newline="") as f:
    lnwriter = csv.writer(f)

    def has_faces(frame):
        face_locations = face_recognition.face_locations(frame)
        return len(face_locations) > 0

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if has_faces(rgb_small_frame):
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(list(known_faces.values()), face_encoding)
                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]

                face_names.append(name)

                if name in known_faces_names:
                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 0, 255), 2)  # Adjusted for resizing
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    font_color = (0, 0, 255)  # Red
                    thickness = 2

                    # Display the name inside the rectangle
                    cv2.putText(frame, name, (left * 4, top * 4 - 10), font, font_scale, font_color, thickness)

                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = datetime.now().strftime("%I-%M-%S %p")
                        lnwriter.writerow([name, current_date, current_time])

        cv2.imshow("attendance system", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release video capture and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()



#Face Recognition algo runs all the time.
'''import face_recognition
import cv2
import numpy as np
import csv  #to create and edit .csv files  
from datetime import datetime
import os 

# initialize video capture
video_capture = cv2.VideoCapture(0)  #[0] here means video capture via webcam, if any other camera is available, then increase array size.

 

# Load known face images and encodings
known_faces = {
    "Hikaru": face_recognition.face_encodings(face_recognition.load_image_file("photos/hikaru.jpg"))[0],
    "Sandesh": face_recognition.face_encodings(face_recognition.load_image_file("photos/sandesh.jpg"))[0],
    "Magnus": face_recognition.face_encodings(face_recognition.load_image_file("photos/magnus.jpg"))[0],
    "Devashish": face_recognition.face_encodings(face_recognition.load_image_file("photos/devashish.jpg"))[0],
    "Abhishek": face_recognition.face_encodings(face_recognition.load_image_file("photos/abhishek.jpg"))[0],
    "Sumit": face_recognition.face_encodings(face_recognition.load_image_file("photos/sumit.jpg"))[0],
}

# Initialize lists and variables
known_faces_names = list(known_faces.keys())
students = known_faces_names.copy()
face_locations = []
face_encodings = []
face_names = []

# Create CSV file with headers if it doesn't exist
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_file = f"{current_date}.csv"
if not os.path.isfile(csv_file):
    with open(csv_file, "w", newline="") as f:
        lnwriter = csv.writer(f)
        lnwriter.writerow(["Student's Name", "Date", "Time"])  # Add headers to the CSV file

# Open CSV file for appending
with open(csv_file, "a", newline="") as f:
    lnwriter = csv.writer(f)

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if True:  # Replace 's' with a descriptive condition if needed
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(list(known_faces.values()), face_encoding)
                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]

                face_names.append(name)

                if name in known_faces_names:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    
                    bottomLeftCornerOfText = (10, 100)
                    fontScale = 1.5
                    fontColor = (0, 0, 139)
                    thickness = 4
                    lineType = 2

                    cv2.putText(
                        frame,
                        f"{name} Present",
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        thickness,
                        lineType,
                    )

                    if name in students:
                        students.remove(name)
                        print(students)
                        current_time = datetime.now().strftime("%I-%M-%S %p")  # Update the time for each entry
                        lnwriter.writerow([name, current_date, current_time])  # Append data to CSV

        cv2.imshow("attendance system", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): #quit the program if user enters q
            break
# Release video capture and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()'''