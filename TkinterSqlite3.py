import tkinter as tk
import tkinter.messagebox as msg
import sqlite3

# ======================== DATABASE ============================
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

# ======================== LOGIC PREDIKSI =======================
def prediksi_fakultas(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    elif ing > bio and ing > fis:
        return "Bahasa"
    else:
        return "Nilai Sama / Tidak Dapat Ditentukan"

# ======================== FUNGSI CRUD ===========================
def load_data():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
    for row in cursor.fetchall():
        tampil = f"{row[0]} | {row[1]} | Bio:{row[2]} | Fis:{row[3]} | Ing:{row[4]} | {row[5]}"
        listbox.insert(tk.END, tampil)

def tambah_data():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except:
        msg.showerror("Error", "Nilai harus berupa angka!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))
    conn.commit()

    msg.showinfo("Berhasil", "Data berhasil disimpan!")
    load_data()

def pilih_data(event):
    try:
        index = listbox.curselection()[0]
        data = listbox.get(index).split(" | ")

        global selected_id
        selected_id = data[0]

        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, data[1])

        entry_bio.delete(0, tk.END)
        entry_bio.insert(0, data[2].split(":")[1])

        entry_fis.delete(0, tk.END)
        entry_fis.insert(0, data[3].split(":")[1])

        entry_ing.delete(0, tk.END)
        entry_ing.insert(0, data[4].split(":")[1])
    except:
        pass

def update_data():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except:
        msg.showerror("Error", "Nilai harus angka!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    cursor.execute("""
        UPDATE nilai_siswa 
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, bio, fis, ing, hasil, selected_id))
    conn.commit()

    msg.showinfo("Sukses", "Data berhasil diperbarui!")
    load_data()

def delete_data():
    if msg.askyesno("Konfirmasi", "Yakin ingin menghapus data?"):
        cursor.execute("DELETE FROM nilai_siswa WHERE id=?", (selected_id,))
        conn.commit()
        load_data()
        msg.showinfo("Sukses", "Data berhasil dihapus!")

# ======================== GUI =========================
top = tk.Tk()
top.title("Aplikasi Prediksi Prodi Siswa")
top.geometry("520x600")
top.config(bg="#e8e8ff")

judul = tk.Label(top, text="Input Nilai Siswa", font=("Arial", 16, "bold"), bg="#e8e8ff")
judul.pack(pady=10)

# Frame Input
frame_input = tk.Frame(top, bg="#dcdcff", padx=10, pady=10)
frame_input.pack(pady=10, fill="x")

def buat_entry(frame, teks):
    lbl = tk.Label(frame, text=teks, bg="#dcdcff", width=12, anchor="w")
    lbl.pack()
    ent = tk.Entry(frame)
    ent.pack(ipady=3, pady=3, fill="x")
    return ent

entry_nama = buat_entry(frame_input, "Nama Siswa")
entry_bio = buat_entry(frame_input, "Biologi")
entry_fis = buat_entry(frame_input, "Fisika")
entry_ing = buat_entry(frame_input, "Inggris")

# Tombol
frame_tombol = tk.Frame(top, bg="#e8e8ff")
frame_tombol.pack(pady=10)

tk.Button(frame_tombol, text="Tambah Data", width=15, bg="#4CAF50", fg="white", command=tambah_data).grid(row=0, column=0, padx=5)
tk.Button(frame_tombol, text="Update Data", width=15, bg="#2196F3", fg="white", command=update_data).grid(row=0, column=1, padx=5)
tk.Button(frame_tombol, text="Delete Data", width=15, bg="#f44336", fg="white", command=delete_data).grid(row=0, column=2, padx=5)

# Listbox
listbox = tk.Listbox(top, height=12, font=("Courier New", 10))
listbox.pack(pady=15, fill="both", padx=15)
listbox.bind("<<ListboxSelect>>", pilih_data)

load_data()

top.mainloop()
