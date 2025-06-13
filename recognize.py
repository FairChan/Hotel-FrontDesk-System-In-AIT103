import cv2
import pickle
import numpy as np
import uuid
import pandas as pd
from deepface import DeepFace
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Model Configuration
MODEL_NAME = "ArcFace"
DETECTOR_BACKEND = "mtcnn"
MAX_DIM = 800
PREDICT_THRESHOLD = 0.7#tolerance level

# Model File Path
PCA_PATH = "/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/pca.pkl"#❗️Absolute path modification
LABEL_ENCODER_PATH = "/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/label_encoder.pkl"#❗️Absolute path modification
CLASSIFIER_PATH = "/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/face_classifier.pkl"#❗️Absolute path modification
GUEST_INFO_PATH = "/Users/fairchan/Downloads/FaceRecognitionProgram-main/SecondModel/guest_info.csv"#❗️Absolute path modification

#Loading Resident Information

def load_guest_info():
    try:
        df = pd.read_csv(GUEST_INFO_PATH)
        info_dict = {
            row['name'].strip().lower(): {
                'room': row['room'],
                'check_in': row['check_in'],
                'check_out': row['check_out']
            } for _, row in df.iterrows()
        }
        return info_dict
    except Exception as e:
        print(f"❌  Failed to load resident information: {e}")
        return {}

GUEST_DATA = load_guest_info()

# identifying function
def recognize_face(frame):
    try:
        objs = DeepFace.represent(
            img_path=frame,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=False
        )
        if len(objs) == 0 or "embedding" not in objs[0]:
            return "🙅No face detected", None
        embedding = objs[0]["embedding"]

        with open(PCA_PATH, "rb") as f:
            pca = pickle.load(f)
        with open(LABEL_ENCODER_PATH, "rb") as f:
            le = pickle.load(f)
        with open(CLASSIFIER_PATH, "rb") as f:
            clf = pickle.load(f)

        embedding_2d = pca.transform([embedding])
        pred_proba = clf.predict_proba(embedding_2d)[0]
        pred_idx = np.argmax(pred_proba)
        label = le.inverse_transform([pred_idx])[0]
        confidence = pred_proba[pred_idx]

        if confidence < PREDICT_THRESHOLD:
            return "🟡 Unregistrated Face", confidence
        return f"✅ {label}", confidence
    except Exception as e:
        return "❌ recognition failure", None

# GUI Recognition Window
class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("😃Facial Recognition System")
        self.label_img = tk.Label(self.root)
        self.label_img.pack()
        self.info_text = tk.Label(self.root, text="", font=("Helvetica", 14), justify=tk.LEFT)
        self.info_text.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.root.after(10, self.update_frame)
            return

        resized_frame = cv2.resize(frame, (640, 480))

        try:
            result = DeepFace.extract_faces(
                img_path=resized_frame,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=False,
                align=False
            )
        except:
            result = []

        info_display = "unidentified user"

        for face_obj in result:
            region = face_obj["facial_area"]
            x, y, w, h = region["x"], region["y"], region["w"], region["h"]
            x, y = max(0, x), max(0, y)
            face_crop = resized_frame[y:y+h, x:x+w]

            label, conf = recognize_face(face_crop)
            cv2.rectangle(resized_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            clean_name = label.replace("✅ ", "").strip().lower()
            info_display = label
            if clean_name in GUEST_DATA:
                info = GUEST_DATA[clean_name]
                info_display += f"\n🏨Room Number: {info['room']}"
                info_display += f"\n⭕️Your check-in time: {info['check_in']}"
                info_display += f"\n❌Your check-out deadline: {info['check_out']}"

        # Update GUI Text
        self.info_text.config(text=info_display)

        # Show image
        img_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.label_img.imgtk = img_tk
        self.label_img.config(image=img_tk)

        self.root.after(30, self.update_frame)

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
