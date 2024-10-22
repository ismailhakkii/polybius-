import tkinter as tk
from tkinter import filedialog, messagebox
import random

# Global değişkenler
polybius_square = None
dark_mode = False  # Karanlık mod başlangıçta kapalı

# Karakter tekrarlarını önleyen fonksiyon
def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

# Key'e dayalı Polybius tablosu oluşturma
def create_polybius_square(key):
    # Türkçe ve İngilizce harfler ve ek karakterler
    characters = (
        "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        "abcçdefgğhıijklmnoöprsştuüvyz"
        "0123456789"
        " .,;:!?()[]{}-_'\"/\\|@#~`"
        "$%^&*+=<>€£₺¥§©®™"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Büyük İngilizce harfler
        "abcdefghijklmnopqrstuvwxyz"  # Küçük İngilizce harfler
        "ÄÖÜäöüß"  # Almanca karakterler
    )

    characters = remove_duplicates(characters)
    total_chars = len(characters)

    # Toplam karakter sayısını 100'e sınırlayalım
    if total_chars > 100:
        characters = characters[:100]
    elif total_chars < 100:
        # Eksik karakterleri doldurmak için boşluk ekleyelim
        characters += ' ' * (100 - total_chars)
        characters = characters[:100]

    # Şimdi toplam karakter sayısı 100 olmalı
    total_chars = len(characters)
    grid_size = 10  # 10x10 matris

    # Key'e göre aynı sonucu almak için random.seed kullanıyoruz
    random.seed(key)
    characters = list(characters)
    random.shuffle(characters)  # Karakterleri key'e göre karıştırıyoruz

    polybius_square = {}
    index = 0
    for row in range(1, grid_size + 1):
        for col in range(1, grid_size + 1):
            if index < total_chars:
                polybius_square[characters[index]] = (row, col)
                index += 1
    return polybius_square, grid_size

# Polybius şifreleme fonksiyonu
def polybius_encrypt(message, polybius_square):
    if not polybius_square:
        messagebox.showerror("Hata", "Lütfen önce bir anahtar girin ve tabloyu oluşturun.")
        return ""
    encrypted_message = []
    for letter in message:
        if letter in polybius_square:
            row, col = polybius_square[letter]
            encrypted_message.append(f"{row:02}{col:02}")
        else:
            encrypted_message.append("????")  # Geçersiz karakterler için ????
    return "".join(encrypted_message)

# Polybius çözme fonksiyonu
def polybius_decrypt(encrypted_message, polybius_square):
    if not polybius_square:
        messagebox.showerror("Hata", "Lütfen önce bir anahtar girin ve tabloyu oluşturun.")
        return ""
    decrypted_message = ""
    inverse_polybius_square = {v: k for k, v in polybius_square.items()}

    # Hatalı giriş kontrolü
    encrypted_message = encrypted_message.replace(" ", "")
    if not encrypted_message.isdigit() or len(encrypted_message) % 4 != 0:
        return "[Geçersiz şifreleme formatı]"

    for i in range(0, len(encrypted_message), 4):
        row = int(encrypted_message[i:i+2])
        col = int(encrypted_message[i+2:i+4])
        pair = (row, col)
        if pair in inverse_polybius_square:
            decrypted_message += inverse_polybius_square[pair]
        else:
            decrypted_message += "?"
    return decrypted_message

# Tabloyu göstermek için fonksiyon
def show_table():
    if not polybius_square:
        messagebox.showerror("Hata", "Lütfen önce bir anahtar girin ve tabloyu oluşturun.")
        return
    table_window = tk.Toplevel(root)
    table_window.title("Polybius Tablosu")
    apply_theme(table_window)

    # Grid yapısı ile tabloyu oluşturma
    for letter, (row, col) in polybius_square.items():
        tk.Label(table_window, text=f"{letter}", borderwidth=2, relief="solid", width=3, height=1,
                 bg=bg_color, fg=fg_color).grid(row=row, column=col, padx=2, pady=2)

# Dosyadan şifreleme yapmak için
def load_file_encrypt():
    if not polybius_square:
        messagebox.showerror("Hata", "Lütfen önce bir anahtar girin ve tabloyu oluşturun.")
        return
    file_path = filedialog.askopenfilename(filetypes=[("Metin Dosyaları", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            encrypted = polybius_encrypt(content, polybius_square)
            result_var.set(f"Şifrelenmiş Mesaj: {encrypted}")

# Dosyadan çözme yapmak için
def load_file_decrypt():
    if not polybius_square:
        messagebox.showerror("Hata", "Lütfen önce bir anahtar girin ve tabloyu oluşturun.")
        return
    file_path = filedialog.askopenfilename(filetypes=[("Metin Dosyaları", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            decrypted = polybius_decrypt(content, polybius_square)
            result_var.set(f"Çözülmüş Mesaj: {decrypted}")

# Key giriş alanı
def get_key():
    key = key_entry.get()
    if key.isdigit():
        return int(key)  # Anahtarı tamsayıya çeviriyoruz
    elif key == "":  # Eğer key girilmezse rastgele bir key üretelim
        random_key = random.randint(1, 1000000)  # Rastgele bir key oluştur
        key_entry.insert(0, str(random_key))  # Rastgele key'i giriş kutusuna yaz
        return random_key
    else:
        messagebox.showerror("Hata", "Geçerli bir anahtar girin")
        return None

# Şifreleme ve çözme işlemlerini başlatmak için anahtarı kullan
def start_with_key():
    global polybius_square, grid_size
    key = get_key()
    if key is not None:
        result = create_polybius_square(key)
        if result:
            polybius_square, grid_size = result
            messagebox.showinfo("Başarılı", f"Polybius tablosu başarıyla oluşturuldu. Tablonun boyutu: {grid_size}x{grid_size}")

# Karanlık modu uygula
def apply_theme(widget):
    for child in widget.winfo_children():
        if isinstance(child, tk.Frame):
            child.configure(bg=bg_color)
            apply_theme(child)
        elif isinstance(child, tk.Label):
            child.configure(bg=bg_color, fg=fg_color)
        elif isinstance(child, tk.Button):
            child.configure(bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
        elif isinstance(child, tk.Entry):
            child.configure(bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        elif isinstance(child, tk.Checkbutton):
            child.configure(bg=bg_color, fg=fg_color, activebackground=bg_color, selectcolor=bg_color)

# Karanlık modu değiştir
def toggle_dark_mode():
    global dark_mode, bg_color, fg_color, button_bg_color, button_fg_color, entry_bg_color, active_bg_color
    dark_mode = not dark_mode
    if dark_mode:
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_bg_color = "#4d4d4d"
        button_fg_color = "#ffffff"
        entry_bg_color = "#3c3c3c"
        active_bg_color = "#5e5e5e"
    else:
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        button_bg_color = "#e0e0e0"
        button_fg_color = "#000000"
        entry_bg_color = "#ffffff"
        active_bg_color = "#d5d5d5"

    root.configure(bg=bg_color)
    apply_theme(root)

# **Sonucu panoya kopyalama fonksiyonu**
def copy_result():
    result_text = result_var.get()
    if result_text:
        root.clipboard_clear()
        root.clipboard_append(result_text)
        messagebox.showinfo("Bilgi", "Sonuç panoya kopyalandı.")
    else:
        messagebox.showwarning("Uyarı", "Kopyalanacak bir sonuç yok.")

# Başlangıç renkleri
bg_color = "#f0f0f0"
fg_color = "#000000"
button_bg_color = "#e0e0e0"
button_fg_color = "#000000"
entry_bg_color = "#ffffff"
active_bg_color = "#d5d5d5"

# Arayüzü iyileştiriyoruz
root = tk.Tk()
root.title("Key'e Dayalı Polybius Şifreleme")
root.geometry("600x850")
root.configure(bg=bg_color)

# Ana Frame
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(pady=20)

# Karanlık Mod Seçeneği
dark_mode_var = tk.BooleanVar()
dark_mode_var.set(False)
dark_mode_check = tk.Checkbutton(root, text="Karanlık Mod", variable=dark_mode_var, command=toggle_dark_mode,
                                 bg=bg_color, fg=fg_color, activebackground=bg_color, selectcolor=bg_color)
dark_mode_check.pack()

# Key giriş alanı
key_frame = tk.Frame(main_frame, bg=bg_color)
key_frame.pack(pady=10)

tk.Label(key_frame, text="Key (Anahtar) girin:", font=("Arial", 12), bg=bg_color, fg=fg_color).pack(side=tk.LEFT)
key_entry = tk.Entry(key_frame, width=20, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
key_entry.pack(side=tk.LEFT, padx=5)
key_button = tk.Button(key_frame, text="Tabloyu Anahtarla Oluştur", command=start_with_key,
                       bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
key_button.pack(side=tk.LEFT, padx=5)

# Mesaj giriş alanı
message_frame = tk.Frame(main_frame, bg=bg_color)
message_frame.pack(pady=10)

tk.Label(message_frame, text="Mesajı girin:", font=("Arial", 12), bg=bg_color, fg=fg_color).pack(anchor='w')
message_entry = tk.Entry(message_frame, width=70, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
message_entry.pack(pady=5)

# Şifrele ve çöz düğmeleri
button_frame = tk.Frame(main_frame, bg=bg_color)
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Şifrele", width=20, command=lambda: result_var.set(
    f"Şifrelenmiş Mesaj: {polybius_encrypt(message_entry.get(), polybius_square)}"),
    bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
encrypt_button.grid(row=0, column=0, padx=5, pady=5)

decrypt_button = tk.Button(button_frame, text="Çöz", width=20, command=lambda: result_var.set(
    f"Çözülmüş Mesaj: {polybius_decrypt(message_entry.get(), polybius_square)}"),
    bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
decrypt_button.grid(row=0, column=1, padx=5, pady=5)

# Dosyadan şifreleme ve çözme düğmeleri
file_button_frame = tk.Frame(main_frame, bg=bg_color)
file_button_frame.pack(pady=10)

file_encrypt_button = tk.Button(file_button_frame, text="Dosyadan Şifrele", width=20, command=load_file_encrypt,
                                bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
file_encrypt_button.grid(row=0, column=0, padx=5, pady=5)

file_decrypt_button = tk.Button(file_button_frame, text="Dosyadan Çöz", width=20, command=load_file_decrypt,
                                bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
file_decrypt_button.grid(row=0, column=1, padx=5, pady=5)

# Tabloyu gösteren buton
show_table_button = tk.Button(main_frame, text="Tabloyu Göster", command=show_table,
                              bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
show_table_button.pack(pady=10)

# Sonuç alanı
result_frame = tk.Frame(main_frame, bg=bg_color)
result_frame.pack(pady=20)

result_var = tk.StringVar()
result_label = tk.Label(result_frame, textvariable=result_var, wraplength=550, font=("Arial", 10), justify="left",
                        bg=bg_color, fg=fg_color)
result_label.pack()

# **Sonucu panoya kopyalama butonu**
copy_button = tk.Button(main_frame, text="Sonucu Panoya Kopyala", command=copy_result,
                        bg=button_bg_color, fg=button_fg_color, activebackground=active_bg_color)
copy_button.pack(pady=5)

# Ana döngüyü başlat
root.mainloop()