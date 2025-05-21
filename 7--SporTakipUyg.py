import tkinter as tk
from tkinter import ttk, messagebox

class Antrenman:
    def __init__(self, ad, puan):
        self.ad = ad
        self.puan = puan

class Sporcu:
    def __init__(self, ad, spor_dali):
        self.ad = ad
        self.spor_dali = spor_dali
        self.antrenmanlar = []

    def antrenman_ekle(self, antrenman):
        self.antrenmanlar.append(antrenman)

    def rapor_satirlari(self):
        # Liste için: her satır => "SporcuAd | SporDalı | AntrenmanAd | Puan"
        satirlar = []
        for i, a in enumerate(self.antrenmanlar):
            satirlar.append((f"{self.ad} | {self.spor_dali} | {a.ad} | Puan: {a.puan}", i))
        return satirlar

    def antrenman_guncelle(self, index, yeni_ad, yeni_puan):
        self.antrenmanlar[index].ad = yeni_ad
        self.antrenmanlar[index].puan = yeni_puan

    def antrenman_sil(self, index):
        del self.antrenmanlar[index]

class AntrenmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antrenman Takip Sistemi")
        self.root.geometry("600x600")
        self.root.configure(bg="#e6f2ff")

        self.sporcular = []

        # Başlık
        ttk.Label(root, text="🏋️ Antrenman Takip Sistemi", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Form: Sporcu ve Antrenman Ekleme
        form_frame = ttk.Frame(root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Sporcu Adı:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sporcu_ad_entry = ttk.Entry(form_frame, width=30)
        self.sporcu_ad_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Spor Dalı:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.spor_dal_entry = ttk.Entry(form_frame, width=30)
        self.spor_dal_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Antrenman Adı:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.antrenman_ad_entry = ttk.Entry(form_frame, width=30)
        self.antrenman_ad_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Puan (0-100):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.puan_entry = ttk.Entry(form_frame, width=30)
        self.puan_entry.grid(row=3, column=1, pady=5)

        ttk.Button(form_frame, text="Sporcu ve Antrenman Ekle", command=self.sporcu_antrenman_ekle).grid(row=4, column=0, columnspan=2, pady=10)

        # Raporlar Listbox
        ttk.Label(root, text="Raporlar (Antrenmanlar):", font=("Segoe UI", 12, "bold")).pack(pady=(20, 5))
        self.rapor_listbox = tk.Listbox(root, width=80, height=15)
        self.rapor_listbox.pack()

        ttk.Button(root, text="Raporları Göster", command=self.rapor_goster).pack(pady=5)

        # Güncelleme ve Silme alanı
        update_frame = ttk.Frame(root)
        update_frame.pack(pady=10)

        ttk.Label(update_frame, text="Yeni Antrenman Adı:").grid(row=0, column=0, padx=5, pady=5)
        self.guncel_ad_entry = ttk.Entry(update_frame, width=30)
        self.guncel_ad_entry.grid(row=0, column=1, pady=5)

        ttk.Label(update_frame, text="Yeni Puan:").grid(row=0, column=2, padx=5, pady=5)
        self.guncel_puan_entry = ttk.Entry(update_frame, width=10)
        self.guncel_puan_entry.grid(row=0, column=3, pady=5)

        ttk.Button(update_frame, text="Güncelle", command=self.antrenman_guncelle).grid(row=0, column=4, padx=10)
        ttk.Button(update_frame, text="Sil", command=self.antrenman_sil).grid(row=0, column=5, padx=10)

        # Antrenman listesi indeks eşleme
        self.rapor_index_map = []

        # Liste seçildiğinde kutuları doldur
        self.rapor_listbox.bind('<<ListboxSelect>>', self.liste_secildi)

    def sporcu_antrenman_ekle(self):
        ad = self.sporcu_ad_entry.get().strip()
        dal = self.spor_dal_entry.get().strip()
        antrenman_ad = self.antrenman_ad_entry.get().strip()
        puan_str = self.puan_entry.get().strip()

        if not ad or not dal or not antrenman_ad or not puan_str:
            messagebox.showwarning("Hata", "Tüm alanları doldurun!")
            return

        try:
            puan = int(puan_str)
            if not (0 <= puan <= 100):
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Puan 0 ile 100 arasında tam sayı olmalı!")
            return

        sporcu = None
        for s in self.sporcular:
            if s.ad.lower() == ad.lower():
                sporcu = s
                break

        if not sporcu:
            sporcu = Sporcu(ad, dal)
            self.sporcular.append(sporcu)

        sporcu.antrenman_ekle(Antrenman(antrenman_ad, puan))
        messagebox.showinfo("Başarılı", f"{ad} için '{antrenman_ad}' antrenmanı eklendi.")

        # Alanları temizle (sadece antrenman adı ve puan)
        self.antrenman_ad_entry.delete(0, tk.END)
        self.puan_entry.delete(0, tk.END)

    def rapor_goster(self):
        self.rapor_listbox.delete(0, tk.END)
        self.rapor_index_map.clear()

        for sporcu in self.sporcular:
            for satir, index in sporcu.rapor_satirlari():
                self.rapor_listbox.insert(tk.END, satir)
                self.rapor_index_map.append((sporcu, index))

    def liste_secildi(self, event):
        secilen = self.rapor_listbox.curselection()
        if not secilen:
            return
        i = secilen[0]
        sporcu, index = self.rapor_index_map[i]
        antrenman = sporcu.antrenmanlar[index]
        # Güncelleme alanlarını doldur
        self.guncel_ad_entry.delete(0, tk.END)
        self.guncel_ad_entry.insert(0, antrenman.ad)
        self.guncel_puan_entry.delete(0, tk.END)
        self.guncel_puan_entry.insert(0, str(antrenman.puan))

    def antrenman_guncelle(self):
        secilen = self.rapor_listbox.curselection()
        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen güncellenecek antrenmanı seçin.")
            return

        yeni_ad = self.guncel_ad_entry.get().strip()
        yeni_puan_str = self.guncel_puan_entry.get().strip()

        if not yeni_ad or not yeni_puan_str:
            messagebox.showwarning("Hata", "Yeni antrenman adı ve puan girilmeli!")
            return

        try:
            yeni_puan = int(yeni_puan_str)
            if not (0 <= yeni_puan <= 100):
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Puan 0-100 aralığında olmalı!")
            return

        i = secilen[0]
        sporcu, index = self.rapor_index_map[i]

        eski_antrenman = sporcu.antrenmanlar[index]
        eski_ad = eski_antrenman.ad
        eski_puan = eski_antrenman.puan

        sporcu.antrenman_guncelle(index, yeni_ad, yeni_puan)
        messagebox.showinfo("Güncellendi", f"{sporcu.ad} için '{eski_ad}' antrenmanı '{yeni_ad}' olarak güncellendi.\nPuan: {eski_puan} -> {yeni_puan}")

        self.rapor_goster()

    def antrenman_sil(self):
        secilen = self.rapor_listbox.curselection()
        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen silinecek antrenmanı seçin.")
            return

        i = secilen[0]
        sporcu, index = self.rapor_index_map[i]
        silinen = sporcu.antrenmanlar[index].ad
        sporcu.antrenman_sil(index)
        messagebox.showinfo("Silindi", f"{sporcu.ad} için '{silinen}' antrenmanı silindi.")

        self.rapor_goster()
        # Güncelleme alanlarını temizle
        self.guncel_ad_entry.delete(0, tk.END)
        self.guncel_puan_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AntrenmanApp(root)
    root.mainloop()
