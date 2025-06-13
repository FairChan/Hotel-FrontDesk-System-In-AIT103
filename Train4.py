import os
import re
import pickle
import cv2
import numpy as np
import uuid
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from deepface import DeepFace

# 配置
MODEL_NAME = "ArcFace"
DETECTOR_BACKEND = "mtcnn"
INPUT_FOLDER = "input"
NAMED_FOLDERS = ["clear_named_faces", "blurred_named_faces"]
MAX_DIM = 800
PCA_PATH = "pca.pkl"
CLASSIFIER_PATH = "face_classifier.pkl"
LABEL_ENCODER_PATH = "label_encoder.pkl"
N_COMPONENTS = 50  # PCA降维目标维度

def load_and_resize_image(img_path, max_dim=MAX_DIM):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("无法加载图像: " + img_path)
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img

def collect_named_faces():
    embeddings, names = [], []

    for folder_name in NAMED_FOLDERS:
        folder_path = os.path.join(INPUT_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            print(f"📂 文件夹不存在：{folder_path}，跳过")
            continue

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            try:
                img_bgr = load_and_resize_image(img_path)
                temp_path = f"temp_{uuid.uuid4().hex}.jpg"
                cv2.imwrite(temp_path, img_bgr)

                objs = DeepFace.represent(
                    img_path=temp_path,
                    model_name=MODEL_NAME,
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=True
                )
                os.remove(temp_path)

                if len(objs) == 0:
                    continue

                embedding = objs[0]["embedding"]

                # 解析人名
                m = re.match(r"([a-zA-Z]+)", img_name)
                label = m.group(1).lower() if m else None
                if not label:
                    continue  # 跳过无法解析名字的图像

                embeddings.append(embedding)
                names.append(label)

            except Exception as e:
                print(f"⚠️ 处理失败: {img_path}，原因: {e}")
                continue

    return np.array(embeddings), names

def visualize_embeddings(embeddings, labels):
    tsne = TSNE(n_components=2, perplexity=5, random_state=42)
    X_embedded = tsne.fit_transform(embeddings)

    le = LabelEncoder()
    y = le.fit_transform(labels)

    plt.figure(figsize=(10, 6))
    for i, label in enumerate(le.classes_):
        idxs = y == i
        plt.scatter(X_embedded[idxs, 0], X_embedded[idxs, 1], label=label)
    plt.title("💡 已命名人脸可视化 (t-SNE)")
    plt.legend()
    plt.show()

def train_named_classifier():
    embeddings, names = collect_named_faces()

    if len(embeddings) == 0:
        print("❌ 没有任何有效命名人脸数据")
        return

    print(f"✅ 收集命名人脸完成，共 {len(embeddings)} 条样本，开始训练...")

    # PCA降维
    pca = PCA(n_components=N_COMPONENTS)
    X_reduced = pca.fit_transform(embeddings)

    # 标签编码
    le = LabelEncoder()
    y = le.fit_transform(names)

    # SVM 训练
    clf = SVC(kernel='linear', probability=True)
    clf.fit(X_reduced, y)

    # 模型保存
    with open(PCA_PATH, "wb") as f:
        pickle.dump(pca, f)
    with open(CLASSIFIER_PATH, "wb") as f:
        pickle.dump(clf, f)
    with open(LABEL_ENCODER_PATH, "wb") as f:
        pickle.dump(le, f)

    print("🎉 训练完成！模型已保存：")
    print("📂", PCA_PATH)
    print("📂", CLASSIFIER_PATH)
    print("📂", LABEL_ENCODER_PATH)
    print("🧠 类别映射：", dict(zip(le.classes_, le.transform(le.classes_))))

    # 可视化
    visualize_embeddings(X_reduced, names)

if __name__ == "__main__":
    train_named_classifier()