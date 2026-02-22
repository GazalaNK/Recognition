import cv2 
import mediapipe as mp
 
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

face_mesh=mp_face.FaceMesh()
cap=cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results =face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_draw.draw_landmarks(
                img,
                face_landmarks,
                mp_face.FACEMESH_TESSELATION
                )
    
    cv2.imshow("Face Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()