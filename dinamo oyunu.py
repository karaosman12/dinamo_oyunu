import tkinter as tk
import random
import winsound  # Windows için ses efektleri
from tkinter import messagebox

class DinamoOyunu:
    def __init__(self, master):
        self.master = master
        master.title("Dinamo Oyunu")
        master.geometry("800x600")  # Ekran çözünürlüğü ayarı
        master.resizable(False, False)  # Pencere boyutunu değiştirmeyi engelle
        master.config(bg="#e0f7fa")

        self.zorluk_seviyesi = tk.StringVar(value="orta")
        self.hedef_sayi = None
        self.deneme_sayisi = 0
        self.basari_sayisi = 0
        self.toplam_deneme = 0
        self.tahmin_gecmisi = []
        self.sure = 30  # 30 saniye zaman sınırı
        self.zaman_guncelleme_id = None

        # Başlık
        self.baslik_frame = tk.Frame(master, bg="#e0f7fa")
        self.baslik_frame.pack(pady=10)

        self.baslik_label = tk.Label(self.baslik_frame, text="Dinamo Oyunu", bg="#e0f7fa", font=("Arial", 16, "bold"))
        self.baslik_label.pack(side=tk.LEFT)

        # Yardım Butonu
        self.yardim_buton = tk.Button(self.baslik_frame, text="?", command=self.yardim, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), width=2)
        self.yardim_buton.pack(side=tk.LEFT, padx=5)

        # Zorluk Seçimi
        self.label = tk.Label(master, text="Zorluk Seviyesi Seçin:", bg="#e0f7fa", font=("Arial", 12))
        self.label.pack(pady=10)

        self.zorluk_frame = tk.Frame(master, bg="#e0f7fa")
        self.zorluk_frame.pack(pady=5)

        self.kolay_radio = tk.Radiobutton(self.zorluk_frame, text="Kolay (1-50)", variable=self.zorluk_seviyesi, value="kolay", bg="#e0f7fa")
        self.kolay_radio.pack(side=tk.LEFT)

        self.orta_radio = tk.Radiobutton(self.zorluk_frame, text="Orta (1-100)", variable=self.zorluk_seviyesi, value="orta", bg="#e0f7fa")
        self.orta_radio.pack(side=tk.LEFT)

        self.zor_radio = tk.Radiobutton(self.zorluk_frame, text="Zor (1-200)", variable=self.zorluk_seviyesi, value="zor", bg="#e0f7fa")
        self.zor_radio.pack(side=tk.LEFT)

        # Başlat/Yeniden Başla Butonu
        self.baslat_yeniden_buton = tk.Button(master, text="Başlat", command=self.baslat_yeniden_basla, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.baslat_yeniden_buton.pack(pady=10)

        # Tahmin Girişi
        self.tahmin_frame = tk.Frame(master, bg="#e0f7fa")
        self.tahmin_frame.pack(pady=5)

        self.tahmin_girdisi = tk.Entry(self.tahmin_frame, font=("Arial", 12))
        self.tahmin_girdisi.pack(side=tk.LEFT, padx=5)

        self.tahmin_buton = tk.Button(self.tahmin_frame, text="Tahmin Et", command=self.tahmin_et, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.tahmin_buton.pack(side=tk.LEFT)

        # Sonuç ve İstatistikler
        self.sonuc_label = tk.Label(master, text="", bg="#e0f7fa", font=("Arial", 12))
        self.sonuc_label.pack(pady=10)

        self.istatistikler_label = tk.Label(master, text="", bg="#e0f7fa", font=("Arial", 12))
        self.istatistikler_label.pack(pady=10)

        self.gecmis_label = tk.Label(master, text="Tahmin Geçmişi: ", bg="#e0f7fa", font=("Arial", 12))
        self.gecmis_label.pack(pady=10)

        self.gecmis_text = tk.Text(master, height=5, width=40, bg="#e0f7fa", state=tk.DISABLED, font=("Arial", 12))
        self.gecmis_text.pack(pady=5)

        self.zaman_label = tk.Label(master, text="", bg="#e0f7fa", font=("Arial", 12))
        self.zaman_label.pack(pady=10)

    def baslat_yeniden_basla(self):
        if self.hedef_sayi is None:  # Oyun başlamamışsa başlat
            self.oyuna_basla()
            self.baslat_yeniden_buton.config(text="Yeniden Başla")  # Buton metnini değiştir
        else:  # Oyun devam ediyorsa yeniden başlat
            self.yeniden_basla()

    def oyuna_basla(self):
        if self.zorluk_seviyesi.get() == "kolay":
            self.hedef_sayi = random.randint(1, 50)
        elif self.zorluk_seviyesi.get() == "orta":
            self.hedef_sayi = random.randint(1, 100)
        else:
            self.hedef_sayi = random.randint(1, 200)

        self.deneme_sayisi = 0
        self.sonuc_label.config(text="")
        self.tahmin_girdisi.delete(0, tk.END)
        self.tahmin_buton.config(state=tk.NORMAL)
        self.baslat_yeniden_buton.config(state=tk.NORMAL)
        self.tahmin_gecmisi.clear()
        self.gecmis_text.config(state=tk.NORMAL)
        self.gecmis_text.delete(1.0, tk.END)
        self.gecmis_text.config(state=tk.DISABLED)

        self.sure = 30  # Zamanı sıfırla
        self.zaman_label.config(text=f"Kalan Süre: {self.sure} saniye")
        self.zaman_guncelleme_id = self.master.after(1000, self.zaman_guncelle)

    def zaman_guncelle(self):
        if self.sure > 0:
            self.sure -= 1
            self.zaman_label.config(text=f"Kalan Süre: {self.sure} saniye")
            self.zaman_guncelleme_id = self.master.after(1000, self.zaman_guncelle)
        else:
            self.sonuc_label.config(text="Zaman doldu! Oyun sona erdi.")
            self.tahmin_buton.config(state=tk.DISABLED)

    def tahmin_et(self):
        try:
            tahmin = int(self.tahmin_girdisi.get())
            if (self.zorluk_seviyesi.get() == "kolay" and not (1 <= tahmin <= 50)) or \
               (self.zorluk_seviyesi.get() == "orta" and not (1 <= tahmin <= 100)) or \
               (self.zorluk_seviyesi.get() == "zor" and not (1 <= tahmin <= 200)):
                self.sonuc_label.config(text="Lütfen geçerli bir sayı girin.")
                return

            self.deneme_sayisi += 1
            self.toplam_deneme += 1
            self.tahmin_gecmisi.append(tahmin)

            if tahmin < self.hedef_sayi:
                self.sonuc_label.config(text="Daha yüksek bir sayı tahmin edin.")
            elif tahmin > self.hedef_sayi:
                self.sonuc_label.config(text="Daha düşük bir sayı tahmin edin.")
            else:
                self.basari_sayisi += 1
                self.sonuc_label.config(text=f"Tebrikler! {self.deneme_sayisi} denemede doğru tahmin ettiniz.")
                self.baslat_yeniden_buton.config(state=tk.NORMAL)
                self.tahmin_buton.config(state=tk.DISABLED)
                self.guncelle_istatistikler()
                winsound.Beep(1000, 500)  # Doğru tahmin sesi
                self.master.after_cancel(self.zaman_guncelleme_id)  # Zamanlayıcıyı durdur

            self.guncelle_gecmis()
        except ValueError:
            self.sonuc_label.config(text="Lütfen geçerli bir sayı girin.")

    def guncelle_gecmis(self):
        self.gecmis_text.config(state=tk.NORMAL)
        self.gecmis_text.delete(1.0, tk.END)
        self.gecmis_text.insert(tk.END, " ".join(map(str, self.tahmin_gecmisi)))
        self.gecmis_text.config(state=tk.DISABLED)

    def guncelle_istatistikler(self):
        if self.toplam_deneme > 0:
            basari_orani = (self.basari_sayisi / self.toplam_deneme) * 100
            self.istatistikler_label.config(text=f"Başarı Oranı: {basari_orani:.2f}% | Toplam Deneme: {self.toplam_deneme}")

    def yeniden_basla(self):
        self.hedef_sayi = None
        self.deneme_sayisi = 0
        self.sonuc_label.config(text="")
        self.tahmin_girdisi.delete(0, tk.END)
        self.tahmin_buton.config(state=tk.NORMAL)
        self.baslat_yeniden_buton.config(text="Başlat")  # Buton metnini değiştir
        self.baslat_yeniden_buton.config(state=tk.NORMAL)
        self.sure = 0  # Geri sayımı sıfırla
        self.zaman_label.config(text=f"Kalan Süre: {self.sure} saniye")  # Geri sayım etiketini sıfırla

    def yardim(self):
        yardim_mesaji = (
            "Dinamo Oyunu Nasıl Oynanır:\n"
            "1. Zorluk seviyesini seçin (Kolay, Orta, Zor).\n"
            "2. 1 ile belirlenen aralıkta bir sayı tahmin edin.\n"
            "3. Doğru tahmin ettiğinizde tebrik edileceksiniz.\n"
            "4. Zaman dolmadan doğru tahmin yapmaya çalışın.\n"
            "5. Tahmin geçmişinizi görebilirsiniz."
        )
        messagebox.showinfo("Yardım", yardim_mesaji)

if __name__ == "__main__":
    root = tk.Tk()
    dinamo_oyunu = DinamoOyunu(root)
    root.mainloop()
