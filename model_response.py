import json          # Untuk membaca file JSON
import random        # Untuk memilih respons secara acak
import pickle        # Untuk memuat model machine learning
import pandas as pd  # Untuk manipulasi data tabular
import re            # Untuk regex (pencocokan pola teks)

# Membuka file model intent classifier yang sudah dilatih, lalu dimuat ke variabel intent_model
with open("intent_classifier.pkl", "rb") as f:
    intent_model = pickle.load(f)

# Membaca file CSV berisi data siswa ke dalam DataFrame pandas
df = pd.read_csv("Dataset_siswa.csv")

# Membaca file intents.json yang berisi daftar intent dan respons chatbot
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# Dictionary untuk menghubungkan pola pertanyaan dengan nama kolom pada DataFrame
patternDict = {
    r"(nilai\s*)?final|uas": "Final_Score",
    r"(nilai\s*)?midterm|uts": "Midterm_Score",
    r"(nilai\s*)?total": "Total_Score",
    r"(absen|kehadiran|hadir)": "Attendance (%)",
    r"(tugas|assignment)": "Assignments_Avg",
    r"(kuis|quiz)": "Quizzes_Avg",
    r"(partisipasi)": "Participation_Score",
    r"(lulus)":"Lulus",
    r"(usia|umur)": "Age",
    r"(grade)": "Grade",
    r"(jumlah)": "JumSis",
    r"(distribusi)": "Distribusi",
    r"(statistik)": "Statistik"
}

# Fungsi untuk mengekstrak slot dari intent dan input user
def extract_slots(intent_tag, user_input):
    slots = {}
    # Mengecek apakah intent mengandung pola tertentu, lalu memasukkan nama kolom ke slots
    for pat, col in patternDict.items():
        if re.search(pat, intent_tag, re.IGNORECASE):
            slots["column"] = col
            break

    # Mengecek apakah intent meminta rata-rata
    if re.search(r"(rata|average|avg)", intent_tag, re.IGNORECASE):
        m = re.search(r"(rata|average|avg)", intent_tag, re.IGNORECASE)
        slots["average"] = True

    # Mengecek apakah intent meminta nilai/usia tertinggi
    elif re.search(r"(paling tinggi|tertinggi|tertua)", intent_tag, re.IGNORECASE):
        slots["extreme"] = "max"

    # Mengecek apakah intent meminta nilai/usia terendah
    elif re.search(r"(paling rendah|terendah|termuda)", intent_tag, re.IGNORECASE):
        slots["extreme"] = "min"

    # Jika intent berhubungan dengan grade, cek grade spesifik dari input user
    if re.search(r"(grade)", intent_tag, re.IGNORECASE):
        m = re.search(r"(nilai|grade)\s+(A|B|C|D|F)", user_input, re.IGNORECASE)
        slots["grade"] = m.group(2)


    # Mengecek apakah intent menyebut gender
    if "perempuan" in intent_tag.lower():
        slots["Gender"] = "Female"
        
    elif "laki" in intent_tag.lower():
        slots["Gender"] = "Male"

    return slots

# Fungsi untuk menjalankan query dinamis ke DataFrame berdasarkan slot yang diekstrak
def run_query(slots):
    q = df.copy() # Membuat salinan DataFrame agar data asli tidak berubah

    if ("column" in slots):
        # Jika yang diminta adalah persentase lulus
        if (slots["column"] == "Lulus"):
            lulus = q[q["Grade"].isin(["A", "B", "C"])]
            
            return [{
                "value":round((len(lulus) / len(df)) * 100, 2)
            }]
            
        # Jika yang diminta adalah jumlah siswa dengan grade tertentu
        if (slots["column"] == "Grade"):
            grade = len(q[q["Grade"] == slots["grade"]])
            print(grade)
            return [{
                "value":grade,
                "grade":slots["grade"]
            }]
        
        # Jika yang diminta adalah statistik deskriptif seluruh data
        if (slots["column"] == "Statistik"):
            stat = q.describe().round(2).to_dict()
            stat_lines = []
            
            for kolom, nilai in stat.items():
                stat_lines.append(f"\n📊 {kolom}:")
                for metrik, angka in nilai.items():
                    stat_lines.append(f"  - {metrik}: {angka}")

            return [{
                "value": "\n".join(stat_lines)
            }]
        
        print(slots)

        # Jika yang diminta adalah distribusi jumlah siswa per grade
        if (slots["column"] == "Distribusi"):
            print("yay")
            val = q["Grade"].value_counts(sort=False, ascending=True).to_dict()
            val_keys = list(val.keys())
            val_keys.sort()

            sorted_val = {i: val[i] for i in val_keys}
            val_lines = []

            for key, value in sorted_val.items():
                val_lines.append(f"\n {key}: {value}")

            return [{
                "value" : "\n".join(val_lines)
            }]

        # Jika user menyebut gender, filter berdasarkan gender
        if ("Gender" in slots):
            q = q[q["Gender"] == slots["Gender"]]

        if (slots["column"] == "JumSis"):
            val = int(len(q))
            return [{
                "value": val
            }]
            
        # Jika user menyebut operator dan threshold (misal: nilai > 80)
        if ("operator" in slots) and ("threshold" in slots):
            q = q.query(f"`{slots['column']}` {slots['op']} {slots['threshold']}")
            return [{"email": row["Email"]} for _, row in q.iterrows()]

        # Jika user meminta nilai tertinggi/terendah
        if ("extreme" in slots):
            val = q[slots["column"]].max() if slots["extreme"] == "max" else q[slots["column"]].min()
            
            q = q[q[slots["column"]] == val]
            return [{
                "email": row["Email"],
                "value": row[slots["column"]]
            } for _, row in q.iterrows()]
        
        # Jika user meminta rata-rata nilai kolom tertentu
        if ("average" in slots):
            val = round(q[slots["column"]].mean(), 2)

            return [{
                "value": val
            } for _, row in q.iterrows()]

    return []

# Fungsi untuk menghasilkan respons chatbot berdasarkan input user
def respond(user_input):
    # Prediksi intent dari input user menggunakan model
    intent_tag = intent_model.predict([user_input])[0]
    # Ekstrak slot dari intent dan input user
    slots = extract_slots(intent_tag, user_input)

    # Cari template respons yang sesuai dari intents.json
    response_template = None
    for intent in intents["intents"]:
        if intent["tag"] == intent_tag:
            response_template = random.choice(intent["responses"])
            break
    
    # Jika tidak ditemukan template, balas default
    if not response_template:
        return "Maaf, saya tidak mengerti maksud Anda."
    
    # Jika respons mengandung placeholder, isi dengan hasil query
    if "{" in response_template:
        print("slots",slots)
        result = run_query(slots)

        if not result:
            return "Tidak ada data yang cocok dengan kriteria tersebut."

        return response_template.format(**result[0])

    # Jika tidak ada placeholder, kembalikan respons apa adanya
    return response_template
