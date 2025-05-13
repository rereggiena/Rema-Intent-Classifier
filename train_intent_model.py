# Import library yang diperlukan
import json                     # Untuk memuat file JSON (intents)
import pickle                   # Untuk menyimpan model yang sudah dilatih ke dalam file
from sklearn.model_selection import train_test_split  # Untuk membagi data ke data latih dan uji
from sklearn.pipeline import make_pipeline            # Untuk membuat pipeline antara TF-IDF dan model
from sklearn.feature_extraction.text import TfidfVectorizer  # Untuk mengubah teks menjadi vektor numerik (TF-IDF)
from sklearn.linear_model import LogisticRegression   # Model klasifikasi yang digunakan (Logistic Regression)
from sklearn.metrics import classification_report     # Untuk mengevaluasi performa model dengan metrik klasifikasi

# Membuka dan membaca file intents.json yang berisi pola dan tag intent
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)  # Memuat data intents ke dalam variabel intents

# Inisialisasi list kosong untuk menyimpan pola (teks) dan labelnya
texts = []   # Menyimpan teks dari pola input
labels = []  # Menyimpan label/tag dari setiap pola

# Looping melalui setiap intent dalam data intents
for intent in intents["intents"]:
    for pattern in intent["patterns"]:      # Loop setiap pattern dalam intent
        texts.append(pattern.lower())       # Menambahkan teks pattern ke list (diubah ke huruf kecil)
        labels.append(intent["tag"])        # Menambahkan tag intent ke list label

# Membagi data menjadi data latih dan data uji (80:20), dengan stratifikasi berdasarkan label
x_train, x_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, stratify=labels, random_state=42
)

# Membuat pipeline yang terdiri dari TF-IDF vectorizer dan Logistic Regression
model = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))

# Melatih model menggunakan data latih
model.fit(x_train, y_train)

# Memprediksi hasil dari data uji
y_pred = model.predict(x_test)

# Menampilkan laporan evaluasi model (akurasi, presisi, recall, f1-score)
print("\n📊 Evaluation Report:")
print(classification_report(y_test, y_pred))

# Menyimpan model yang sudah dilatih ke dalam file .pkl
with open("intent_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

# Menampilkan pesan bahwa model telah berhasil disimpan
print("\n Model training complete and saved to 'intent_classifier.pkl'")