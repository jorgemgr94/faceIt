import cv2, sys, numpy, os,fnmatch

size = 4
fn_haar = 'haarcascade_frontalface_alt.xml'
fn_dir = 'subject_faces'

# Part 1: Create fisherRecognizer
print('Hold on loading necessary files...')
(images, lables, names, id) = ([], [], {}, 0)
# looking into folders till reaching the requested
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        #for filename in os.listdir(subjectpath):
        for filename in fnmatch.filter(os.listdir(subjectpath), '*.png'):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(im_width, im_height) = (224, 184)
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

model = cv2.face.FisherFaceRecognizer_create()
model.train(images, lables)

haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)

#Part 2: Use fisherRecognizer on camera stream
while True:
    (rval, frame) = webcam.read()
    frame=cv2.flip(frame,1,0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))
    faces = haar_cascade.detectMultiScale(mini)
    for i in range(len(faces)):
        face_i = faces[i]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        prediction = model.predict(face_resize)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
        cv2.putText(frame,
            'You are: %s - %.0f' % (names[prediction[0]],prediction[1]),
            (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 0))
    cv2.imshow('FaceIT | Face Recognition & Subject Identification', frame)
    key = cv2.waitKey(10)
    if key == 27:
        break