import tkinter as tk
import tkinter.messagebox as msg
import sqlite3

conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit()

def prediksi_fakultas(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    elif ing > bio and ing > fis:
        return "Bahasa"
    else:
        return "Nilai Sama / Tidak Dapat Ditentukan"

def proses_hasil():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except:
        msg.showerror("Error", "Semua nilai harus angka!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))
    conn.commit()

    luaran.config(text=f"Hasil Prediksi: {hasil}", bg="yellow")
    msg.showinfo("Berhasil", "Data berhasil disimpan ke database!")

top = tk.Tk()
top.title("Aplikasi Prediksi Prodi Pilihan")
top.geometry("400x500")
top.configure(bg="#2716A4")

judul_label = tk.Label(top, text="Input Nilai Siswa", bg="#2716A4", font=("Times New Roman", 12, "bold"))
judul_label.pack(pady=10)

frame_nama = tk.Frame(top, bg="#2716A4")
frame_nama.pack(pady=5)

tk.Label(frame_nama, text="Nama Siswa:", bg="white", width=12).pack(side=tk.LEFT)
entry_nama = tk.Entry(frame_nama, bd=6)
entry_nama.pack(side=tk.LEFT, expand=True)

frame_bio = tk.Frame(top, bg="#2716A4")
frame_bio.pack(pady=5)

tk.Label(frame_bio, text="Biologi:", bg="white", width=12).pack(side=tk.LEFT)
entry_bio = tk.Entry(frame_bio, bd=6)
entry_bio.pack(side=tk.LEFT, expand=True)

frame_fis = tk.Frame(top, bg="#2716A4")
frame_fis.pack(pady=5)

tk.Label(frame_fis, text="Fisika:", bg="white", width=12).pack(side=tk.LEFT)
entry_fis = tk.Entry(frame_fis, bd=6)
entry_fis.pack(side=tk.LEFT, expand=True)

frame_ing = tk.Frame(top, bg="#2716A4")
frame_ing.pack(pady=5)

tk.Label(frame_ing, text="Inggris:", bg="white", width=12).pack(side=tk.LEFT)
entry_ing = tk.Entry(frame_ing, bd=6)
entry_ing.pack(side=tk.LEFT, expand=True)

tombolHasil = tk.Button(top, text="Submit & Prediksi", bg="#1198C5", command=proses_hasil)
tombolHasil.pack(pady=20)

luaran = tk.Label(top, text="Luaran hasil prediksi", bg="#ffffff")
luaran.pack(side=tk.BOTTOM, pady=20)

top.mainloop()
