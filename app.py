# Penjelasan: Import library yang dibutuhkan
import tkinter as tk # Untuk membuat GUI aplikasi desktop
from tkinter import Canvas, Frame, Entry, Scrollbar, PhotoImage # Komponen GUI tambahan
import time          # Untuk fungsi terkait waktu
import threading     # Untuk menjalankan proses secara paralel (threading)
from model_response import respond

# Membuat window utama aplikasi dengan judul dan ukuran tertentu
root = tk.Tk()
root.title("Chatbot Nilai Siswa")
root.geometry("450x700")
root.configure(bg="#f0f2f5")

# Membuat frame area chat
chat_frame = Frame(root, bg="#f0f2f5")
chat_frame.pack(padx=20, pady=20, fill="both", expand=True)

canvas = Canvas(chat_frame, bg="#f0f2f5", highlightthickness=0)
scrollbar = Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#f0f2f5")

# Mengatur agar scroll otomatis saat frame bertambah
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Membuat frame untuk input user di bawah area chat
input_frame = Frame(root, bg="#ffffff")
input_frame.pack(padx=20, pady=10, fill="x")

# Membuat entry (kolom input) untuk mengetik pesan
entry = Entry(input_frame, font=("Helvetica", 12), bg="#ffffff", fg="#333333", bd=0)
entry.pack(side="left", fill="both", expand=True, ipady=10, padx=(10, 5))
entry.bind("<Return>", lambda event: send_message(entry.get()))

# Fungsi untuk menggambar warna gradient pada canvas
def draw_gradient(canvas, x, y, w, h, color1, color2):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / h
    g_ratio = (g2 - g1) / h
    b_ratio = (b2 - b1) / h

    for i in range(h):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(x, y+i, x+w, y+i, fill=color)

# Fungsi untuk membuat rectangle dengan sudut membulat pada canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Fungsi untuk membuat pop-up
import tkinter as tk
from tkinter import Canvas, Frame

# Fungsi untuk menampilkan pop-up daftar fitur/pertanyaan yang bisa dipilih
def show_popup():
    # Membuat pop-up window
    popup = tk.Toplevel(root)
    popup.title("List Of Features")
    popup.geometry("300x300")
    popup.configure(bg="#f0f2f5")

    # Frame utama dengan canvas dan scrollbar
    canvas = Canvas(popup, bg="#f0f2f5", highlightthickness=0)
    scrollbar = Scrollbar(popup, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f0f2f5")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    def _on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            pass

    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows / MacOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Daftar pertanyaan
    questions = [
        "Halo", "Goodbye", "Thank you",
        "Nilai Total Tertinggi", "Nilai Total Terendah", "Nilai Total Rata-Rata",
        "Jumlah Siswa", "Jumlah Perempuan", "Jumlah Laki",
        "Usia Tertua", "Usia Termuda", "Usia Rata",
        "Kuis Tertinggi", "Kuis Terendah", "Kuis Rata Rata",
        "Tugas Terendah", "Tugas Tertinggi", "Tugas Rata Rata",
        "Partisipasi Tertinggi", "Partisipasi Terendah", "Partisipasi Rata Rata",
        "Jumlah Siswa dengan Nilai A", "Jumlah Siswa dengan Nilai B", "Jumlah Siswa dengan Nilai C",
        "Jumlah Siswa dengan Nilai D","Jumlah Siswa dengan Nilai F",
        "Distribusi Nilai", "Kehadiran Terendah", "Kehadiran Tertinggi", "Kehadiran Rata Rata",
        "Persentase Lulus", "Nilai Midterm Tertinggi", "Nilai Midterm Terendah", "Nilai Midterm Rata-Rata",
        "Nilai Final Terendah", "Nilai Final Tertinggi", "Nilai Final Rata-Rata",
        "Statistik Dataset"
    ]
    
    def send_question(question):
        send_message(question)

    # Tambahkan tombol-tombol pertanyaan ke dalam scrollable_frame
    for question in questions:
        question_button = tk.Button(
            scrollable_frame,
            text=question,
            command=lambda q=question: send_question(q),
            font=("Helvetica", 12),
            bg="#7f5af0",
            fg="white",
            relief="flat"
        )
        question_button.pack(pady=5, fill="x", padx=10)

    # Tombol untuk menutup pop-up secara manual
    close_button = tk.Button(
        scrollable_frame,
        text="Tutup",
        command=popup.destroy,
        font=("Helvetica", 10),
        bg="#7f5af0",
        fg="white"
    )
    close_button.pack(pady=10)

# Membuat tombol "+" di samping tombol kirim, untuk menampilkan fitur pop-up
plus_button_canvas = Canvas(input_frame, width=40, height=40, highlightthickness=0, bg="#7f5af0")
draw_gradient(plus_button_canvas, 0, 0, 50, 50, "#7f5af0", "#4ea5f7")
plus_button_canvas.create_text(20, 20, text="+", font=("Helvetica", 20), fill="white")
plus_button_canvas.pack(side="right", padx=(5, 10), pady=5)
plus_button_canvas.bind("<Button-1>", lambda event: show_popup())  

# Membuat tombol send (ikon ➤)
send_button_canvas = Canvas(input_frame, width=40, height=40, highlightthickness=0, bg="#7f5af0")
draw_gradient(send_button_canvas, 0, 0, 50, 50, "#7f5af0", "#4ea5f7")
send_button_canvas.create_text(20, 20, text="➤", font=("Helvetica", 20), fill="white")
send_button_canvas.pack(side="right", padx=(5, 10), pady=5)
send_button_canvas.bind("<Button-1>", lambda event: send_message(entry.get()))

# Fungsi untuk membuat bubble chat di area chat
def create_bubble(text, is_user=True):
    bubble_frame = Frame(scrollable_frame, bg="#f0f2f5")
    bubble_frame.pack(fill="x", pady=5, padx=10, anchor="e" if is_user else "w")

    inner_frame = Frame(bubble_frame, bg="#f0f2f5")
    inner_frame.pack(anchor="e" if is_user else "w")

    MAX_WIDTH = 250
    text_width = len(text) * 9
    lines = text.split('\n')
    text_height = len(lines) * 18
    bubble_canvas_width = min(text_width + 40, MAX_WIDTH)
    bubble_canvas = Canvas(inner_frame, width=bubble_canvas_width, height=text_height + 30, highlightthickness=0, bg="#f0f2f5")

    if is_user:
        user_image = PhotoImage(file="image/user.png").subsample(16, 16)
        user_label = tk.Label(inner_frame, image=user_image, bg="#f0f2f5")
        user_label.image = user_image
        user_label.pack(side="right", padx=(10, 0), anchor="n")

        radius = 10
        bubble_canvas.config(bg="#f0f2f5")

        r1, g1, b1 = bubble_canvas.winfo_rgb("#7f5af0")
        r2, g2, b2 = bubble_canvas.winfo_rgb("#4ea5f7")
        h = text_height + 30
        w = bubble_canvas_width

        r_ratio = (r2 - r1) / h
        g_ratio = (g2 - g1) / h
        b_ratio = (b2 - b1) / h

        for i in range(h):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'

            if i < radius:
                x_offset = radius - ((radius**2 - (radius - i)**2) ** 0.5)
            elif i > h - radius:
                x_offset = radius - ((radius**2 - (i - (h - radius))**2) ** 0.5)
            else:
                x_offset = 0

            bubble_canvas.create_line(x_offset, i, w - x_offset, i, fill=color)

        create_rounded_rectangle(bubble_canvas, 0, 0, bubble_canvas_width, text_height + 30, radius=radius, fill="", outline="")

        bubble_canvas.create_text(20, 10, text=text, font=("Helvetica", 11), fill="white", anchor="nw", width=bubble_canvas_width - 40)
        bubble_canvas.pack(side="right", padx=(20, 0), anchor="n")

    else:
        bot_image = PhotoImage(file="image/bot.png").subsample(12, 12)
        bot_label = tk.Label(inner_frame, image=bot_image, bg="#f0f2f5")
        bot_label.image = bot_image
        bot_label.pack(side="left", padx=(30, 5), anchor="n")

        radius = 20
        bubble_canvas.config(bg="#f0f2f5")

        # Buat teks sementara untuk mengukur ukuran yang tepat
        temp_text_id = bubble_canvas.create_text(
            0, 0,
            text=text,
            font=("Helvetica", 11),
            anchor="nw",
            width=MAX_WIDTH - 40
        )
        bbox = bubble_canvas.bbox(temp_text_id)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        bubble_canvas_width = text_width + 40
        bubble_canvas.config(width=bubble_canvas_width, height=text_height + 30)
        bubble_canvas.delete(temp_text_id)

        create_rounded_rectangle(
            bubble_canvas,
            0,
            0,
            bubble_canvas_width,
            text_height + 30,
            radius=radius,
            fill="#ffffff",
            outline="#ffffff"
        )

        bubble_canvas.create_text(
            20,
            10,
            text=text,
            font=("Helvetica", 11),
            fill="black",
            anchor="nw",
            width=bubble_canvas_width - 40
        )
        bubble_canvas.pack(side="left", anchor="n")


    bubble_canvas.pack()
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# Fungsi animasi loading
def show_loading():
    loading_bubble = Frame(scrollable_frame, bg="#f0f2f5")
    loading_canvas = Canvas(loading_bubble, width=300, height=40, bg="#f0f2f5", highlightthickness=0)
    loading_text = "Analyzing data, please wait"
    text_item = loading_canvas.create_text(150, 20, text=loading_text, font=("Helvetica", 11), fill="#7f5af0", width=260)
    loading_canvas.pack(anchor="w", pady=5, padx=(0, 50))
    loading_bubble.pack(anchor="w", fill="x")
    root.update_idletasks()
    canvas.yview_moveto(1.0)

    dots = ""
    for _ in range(6):
        dots += "."
        loading_canvas.itemconfig(text_item, text=loading_text + dots)
        time.sleep(0.1)
        root.update_idletasks()
    loading_bubble.destroy()

# Fungsi kirim pesan
def send_message(user_input):
    if not user_input.strip():
        return

    entry.delete(0, tk.END)
    create_bubble(user_input, is_user=True)

    def bot_response():
        show_loading()
        response = respond(user_input)
        create_bubble(response, is_user=False)

    threading.Thread(target=bot_response).start()
    
# Jalankan aplikasi
root.mainloop()
