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

    def rapor_al(self):
        if not self.antrenmanlar:
            return "Kayıtlı antrenman bulunamadı."
        rapor = f"📋 {self.ad} ({self.spor_dali}) Antrenman Raporu:\n\n"
        for a in self.antrenmanlar:
            rapor += f"- {a.ad} | Puan: {a.puan}\n"
        return rapor

class AntrenmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antrenman Takip Sistemi")
        self.root.geometry("600x600")
        self.root.configure(bg="#e6f2ff")

        self.sporcular = []
        self.secili_sporcu = None
        self.secili_antrenman_index = None

        ttk.Label(root, text="🏋️ Antrenman Takip Sistemi", font=("Segoe UI", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=5)

        ttk.Label(frame, text="Sporcu Adı:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.sporcu_ad_entry = ttk.Entry(frame, width=30)
        self.sporcu_ad_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Spor Dalı:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.spor_dal_entry = ttk.Entry(frame, width=30)
        self.spor_dal_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Antrenman Adı:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.antrenman_ad_entry = ttk.Entry(frame, width=30)
        self.antrenman_ad_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Puan (0-100):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.puan_entry = ttk.Entry(frame, width=30)
        self.puan_entry.grid(row=3, column=1)

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Sporcu ve Antrenman Ekle", command=self.sporcu_antrenman_ekle).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Güncelle", command=self.antrenman_guncelle).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Sil", command=self.antrenman_sil).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Rapor Al", command=self.rapor_goster).grid(row=0, column=3, padx=5)

        # Antrenman Listbox
        self.antrenman_listbox = tk.Listbox(root, height=6, width=50)
        self.antrenman_listbox.pack(pady=5)
        self.antrenman_listbox.bind('<<ListboxSelect>>', self.antrenman_secildi)

        # Rapor Alanı
        self.rapor_alan = tk.Text(root, height=15, width=70)
        self.rapor_alan.pack(pady=10)
        self.rapor_alan.configure(state="disabled", font=("Courier New", 10))

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
            messagebox.showwarning("Hata", "Puan 0 ile 100 arasında olmalı!")
            return

        sporcu = None
        for s in self.sporcular:
            if s.ad.lower() == ad.lower():
                sporcu = s
                break

        if not sporcu:
            sporcu = Sporcu(ad, dal)
            self.sporcular.append(sporcu)

        self.secili_sporcu = sporcu
        sporcu.antrenman_ekle(Antrenman(antrenman_ad, puan))

        messagebox.showinfo("Başarılı", f"{ad} için '{antrenman_ad}' eklendi.")
        self.antrenman_ad_entry.delete(0, tk.END)
        self.puan_entry.delete(0, tk.END)

        self.antrenmanlari_guncelle_listbox()

    def antrenmanlari_guncelle_listbox(self):
        self.antrenman_listbox.delete(0, tk.END)
        if self.secili_sporcu:
            for idx, ant in enumerate(self.secili_sporcu.antrenmanlar):
                self.antrenman_listbox.insert(tk.END, f"{idx+1}. {ant.ad} | Puan: {ant.puan}")

    def antrenman_secildi(self, event):
        secim = self.antrenman_listbox.curselection()
        if not secim or not self.secili_sporcu:
            return
        index = secim[0]
        self.secili_antrenman_index = index
        secili_ant = self.secili_sporcu.antrenmanlar[index]
        self.antrenman_ad_entry.delete(0, tk.END)
        self.antrenman_ad_entry.insert(0, secili_ant.ad)
        self.puan_entry.delete(0, tk.END)
        self.puan_entry.insert(0, str(secili_ant.puan))

    def antrenman_guncelle(self):
        if self.secili_sporcu is None or self.secili_antrenman_index is None:
            messagebox.showwarning("Hata", "Güncellemek için bir antrenman seçin.")
            return
        try:
            yeni_ad = self.antrenman_ad_entry.get().strip()
            yeni_puan = int(self.puan_entry.get().strip())
            if not (0 <= yeni_puan <= 100):
                raise ValueError
        except:
            messagebox.showwarning("Hata", "Geçerli bir puan girin (0-100).")
            return

        ant = self.secili_sporcu.antrenmanlar[self.secili_antrenman_index]
        ant.ad = yeni_ad
        ant.puan = yeni_puan

        messagebox.showinfo("Güncellendi", "Antrenman başarıyla güncellendi.")
        self.antrenmanlari_guncelle_listbox()

    def antrenman_sil(self):
        if self.secili_sporcu is None or self.secili_antrenman_index is None:
            messagebox.showwarning("Hata", "Silmek için bir antrenman seçin.")
            return
        del self.secili_sporcu.antrenmanlar[self.secili_antrenman_index]
        messagebox.showinfo("Silindi", "Antrenman silindi.")
        self.secili_antrenman_index = None
        self.antrenman_ad_entry.delete(0, tk.END)
        self.puan_entry.delete(0, tk.END)
        self.antrenmanlari_guncelle_listbox()

    def rapor_goster(self):
        self.rapor_alan.configure(state="normal")
        self.rapor_alan.delete(1.0, tk.END)
        if not self.sporcular:
            self.rapor_alan.insert(tk.END, "Henüz sporcu veya antrenman eklenmedi.")
        else:
            for s in self.sporcular:
                self.rapor_alan.insert(tk.END, s.rapor_al() + "\n")
        self.rapor_alan.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AntrenmanApp(root)
    root.mainloop()
