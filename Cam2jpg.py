import cv2
import os
from deepface import DeepFace
import time

SAVE_FOLDER = "input/clear_named_faces"
SAMPLES_PER_PERSON = 30
DETECTOR_BACKEND = "mtcnn"

def capture_face_samples():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌Can't turn on the camera.")
        return

    print(f"📸 Start collecting faces (target:{SAMPLES_PER_PERSON} ），Press ‘q’ to exit early")

    collected = 0
    name = input("Please enter the person's name (in English, for filenames only):").strip().lower()
    save_path = SAVE_FOLDER
    os.makedirs(save_path, exist_ok=True)

    while collected < SAMPLES_PER_PERSON:
        ret, frame = cap.read()
        if not ret:
            break

        filename = f"{name}{collected+1}.jpg"

        cv2.imwrite(os.path.join(save_path, filename), frame)
        cv2.imshow("Acquisition...", frame)
        print(f"✅ Acquired {collected+1} ")
        collected += 1
        time.sleep(0.5)  # 保留你之前想要的间隔

        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✌️ Complete the acquisition and save a total of 3 {collected} images to {save_path}")

if __name__ == "__main__":
    capture_face_samples()