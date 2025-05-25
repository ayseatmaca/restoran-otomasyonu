import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
from Kullanıcı_girişiUI import*
from datetime import datetime
from AnamenüUİ import Ui_MainWindow as Ui_AnaMenu

"""uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()"""


import sqlite3
global curs
global conn
import sqlite3
import os

# Var olan veritabanını sil ve tekrar oluştur
"""if os.path.exists('veritabani.db'):
    os.remove('veritabani.db')"""

conn = sqlite3.connect('Veritabani_Yemek.db')
curs = conn.cursor()

curs.execute('''
CREATE TABLE IF NOT EXISTS Menü (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_adi TEXT NOT NULL,
    fiyat REAL NOT NULL
)
''')
"""try:
    curs.execute("ALTER TABLE Menü ADD COLUMN miktar INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    print("Zaten miktar sütunu var")"""

# Şiparişler tablosu, müşteri ve ürün bilgisi içerir
curs.execute('''
CREATE TABLE IF NOT EXISTS siparisler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    musteri_adi TEXT NOT NULL,
    urun_id INTEGER NOT NULL,
    miktar INTEGER NOT NULL,
    tarih TEXT NOT NULL,
    toplam_tutar REAL,
    FOREIGN KEY (urun_id) REFERENCES menu(id) -- Bağlantı (Foreign Key)
)

''')

curs.execute('''
CREATE TABLE IF NOT EXISTS calisanlar (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL,
    soyisim TEXT NOT NULL,
    tel_no TEXT,
    departman TEXT NOT NULL,
    kullanici_adi TEXT NOT NULL UNIQUE,  
    sifre TEXT NOT NULL
)
''')


"""# Çalışan ekle
isim = "Ayşe"
soyisim = "Atmaca"
tel_no = "05551234567"
departman = "Yönetim"
kullanici_adi = "ayseatmaca"
sifre = "1234"

try:
    curs.execute("INSERT INTO calisanlar (isim, soyisim, tel_no, departman, kullanici_adi, sifre) VALUES (?, ?, ?, ?, ?, ?)",
                 (isim, soyisim, tel_no, departman, kullanici_adi, sifre))
    conn.commit()
    print("Çalışan başarıyla eklendi.")
except sqlite3.IntegrityError:
    print("Bu kullanıcı adı zaten var!")"""
conn.commit()
conn.close()




# --- Giriş Ekranı Sınıfı ---
class LoginEkrani(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        self.ui.giris.clicked.connect(self.Giris)

    def Giris(self):
        kullanici_adi = self.ui.giri_kullancad.text()
        sifre = self.ui.giri_sifre.text()

        conn = sqlite3.connect('Veritabani_Yemek.db')
        curs = conn.cursor()

        curs.execute("SELECT * FROM calisanlar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        sonuc = curs.fetchone()

        if sonuc:
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.menu_penceresi = QMainWindow()
            self.ui_menu = Ui_AnaMenu()
            self.ui_menu.setupUi(self.menu_penceresi)                       
            self.menu_penceresi.show()
            self.close()
            
            self.ui_menu.pB_Ekle.clicked.connect(self.urun_ekle)
            self.tabloyu_doldur()
            
            
            """Ana Menu tusları buarda atnacak"""
            self.ui_menu.tableWidget_menu.itemSelectionChanged.connect(self.tablo_satir_secildi)
            self.ui_menu.pB_Guncelle.clicked.connect(self.urun_guncelle)
            self.ui_menu.pB_Sil.clicked.connect(self.urun_sil)
            """MENU YÖNETİMŞ BUTONLARI"""
            self.combobox_doldur()
            self.ui_menu.pB_ekle.clicked.connect(self.siparis_ekle)
            self.siparisleri_goster()
            self.ui_menu.tableWidget_menu_2.cellClicked.connect(self.siparis_satiri_secildi)
            self.ui_menu.pB_guncelle.clicked.connect(self.siparis_guncelle)
            self.ui_menu.pB_Sil_2.clicked.connect(self.silSiparis)
            self.ui_menu.tabWidget_menogeleri.currentChanged.connect(self.sayfaDegisti)
            self.ui_menu.pB_Raporugrntle.clicked.connect(self.raporu_excele_aktar)
            """ÇALIŞSANYÖNETİMİ"""
            self.ui_menu.pB_ekle_2.clicked.connect(self.calisan_ekle)
            self.ui_menu.tabWidget_menogeleri.currentChanged.connect(self.sayfaDegistir)
            self.ui_menu.pB_Dzenle.clicked.connect(self.calisan_guncelle)
            self.ui_menu.tableWidget_Calisanlar.cellClicked.connect(self.calisan_verilerini_getir)
            self.ui_menu.pB_sil.clicked.connect(self.calisan_sil)
            self.ui_menu.bt_cks.clicked.connect(self.uygulamayi_kapat)


  
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

        conn.close()
    """ÜRÜNEKLE"""
    def urun_ekle(self):
        urun_adi = self.ui_menu.le_urunadi.text()
        fiyat = self.ui_menu.dSB_fiyat.value()
        miktar = self.ui_menu.SB_adet.value()
        
        if not urun_adi:
            QMessageBox.warning(self, "Hata", "Ürün adı boş bırakılamaz!")
            return
        if fiyat <= 0:
            QMessageBox.warning(self, "Hata", "Fiyat 0'dan büyük olmalıdır!")
            return
        if miktar <= 0:
            QMessageBox.warning(self, "Hata", "Miktar 0'dan büyük olmalıdır!")
            return

        conn = sqlite3.connect('Veritabani_Yemek.db')
        curs = conn.cursor()
        
        # Aynı ürün var mı kontrol et
        curs.execute("SELECT miktar FROM Menü WHERE urun_adi=?", (urun_adi,))
        sonuc = curs.fetchone()
    
        if sonuc:
           # Ürün zaten varsa, sadece miktarı artır
           mevcut_miktar = sonuc[0]
           yeni_miktar = mevcut_miktar + miktar
           curs.execute("UPDATE Menü SET miktar=?, fiyat=? WHERE urun_adi=?", (yeni_miktar, fiyat, urun_adi))
        else:
           # Yoksa yeni ürün olarak ekle
           curs.execute("INSERT INTO Menü (urun_adi, fiyat, miktar) VALUES (?, ?, ?)", (urun_adi, fiyat, miktar))

        
        
        
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Ürün başarıyla eklendi!")
        self.ui_menu.le_urunadi.clear()
        self.ui_menu.dSB_fiyat.setValue(0.0)
        self.ui_menu.SB_adet.setValue(0)     
        self.tabloyu_doldur()
    """TABLO DOLDURMA"""    
    def tabloyu_doldur(self):
        conn = sqlite3.connect('Veritabani_Yemek.db')
        curs = conn.cursor()
        curs.execute("SELECT id, urun_adi, fiyat, miktar FROM Menü")
        veriler = curs.fetchall()
        conn.close()
    
        self.ui_menu.tableWidget_menu.setRowCount(len(veriler))
        self.ui_menu.tableWidget_menu.setColumnCount(4)
        self.ui_menu.tableWidget_menu.setHorizontalHeaderLabels(["ID", "Ürün Adı", "Fiyat", "Miktar"])
    
        for row, veri in enumerate(veriler):
            for col, val in enumerate(veri):
                self.ui_menu.tableWidget_menu.setItem(row, col, QTableWidgetItem(str(val)))
    
        self.ui_menu.tableWidget_menu.resizeColumnsToContents()

    """TABLO SEÇİMİ"""
    """Burada methodlar atanacak """
    def tablo_satir_secildi(self):
        secilen_satir = self.ui_menu.tableWidget_menu.currentRow()
        if secilen_satir != -1:
            urun_adi = self.ui_menu.tableWidget_menu.item(secilen_satir, 1).text()
            fiyat = float(self.ui_menu.tableWidget_menu.item(secilen_satir, 2).text())
            miktar = int(self.ui_menu.tableWidget_menu.item(secilen_satir, 3).text())
    
            self.ui_menu.le_urunadi.setText(urun_adi)
            self.ui_menu.dSB_fiyat.setValue(fiyat)
            self.ui_menu.SB_adet.setValue(miktar)

    """ÜRÜN GÜNCELLEME"""
    def urun_guncelle(self):
        secilen_satir = self.ui_menu.tableWidget_menu.currentRow()
        if secilen_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellemek için tablodan bir satır seçin.")
            return
    
        urun_id = int(self.ui_menu.tableWidget_menu.item(secilen_satir, 0).text())
        urun_adi = self.ui_menu.le_urunadi.text().strip()
        fiyat = self.ui_menu.dSB_fiyat.value()
        miktar = self.ui_menu.SB_adet.value()
    
        if not urun_adi:
            QMessageBox.warning(self, "Uyarı", "Ürün adı boş olamaz!")
            return
    
        conn = sqlite3.connect('Veritabani_Yemek.db')
        curs = conn.cursor()
        curs.execute("UPDATE Menü SET urun_adi=?, fiyat=?, miktar=? WHERE id=?",
                     (urun_adi, fiyat, miktar, urun_id))
        conn.commit()
        conn.close()
    
        QMessageBox.information(self, "Başarılı", "Ürün başarıyla güncellendi!")
        self.tabloyu_doldur()
        
        self.ui_menu.le_urunadi.clear()
        self.ui_menu.dSB_fiyat.setValue(0.0)
        self.ui_menu.SB_adet.setValue(0)
        
        
    """ÜRÜN SİL"""
    def urun_sil(self):
        secilen_satir = self.ui_menu.tableWidget_menu.currentRow()
        if secilen_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek bir ürün seçin!")
            return
    
        urun_id = int(self.ui_menu.tableWidget_menu.item(secilen_satir, 0).text())
    
        cevap = QMessageBox.question(
            self,
            "Silme Onayı",
            "Seçilen ürünü silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if cevap == QMessageBox.Yes:
            conn = sqlite3.connect('Veritabani_Yemek.db')
            curs = conn.cursor()
            curs.execute("DELETE FROM Menü WHERE id=?", (urun_id,))
            conn.commit()
            conn.close()
    
            QMessageBox.information(self, "Başarılı", "Ürün başarıyla silindi!")
            self.tabloyu_doldur()
            self.ui_menu.le_urunadi.clear()
            self.ui_menu.dSB_fiyat.setValue(0.0)
            self.ui_menu.SB_adet.setValue(0)
            
            
            
    """SİPARİŞ YÖNETİMİ EKRANI"""
    """ÜRÜNLERİ COMBOBOXA YÜKLE"""
    def combobox_doldur(self):
        self.ui_menu.CB_urunsecimi.clear()
        
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        curs.execute("SELECT urun_adi, miktar FROM Menü")
        urunler = curs.fetchall()
    
        for urun_adi, miktar in urunler:
            if miktar > 0:
                self.ui_menu.CB_urunsecimi.addItem(urun_adi)
            else:
                self.ui_menu.CB_urunsecimi.addItem(f"{urun_adi} (Stokta yok)")
    
        conn.close()

    """SİPARİŞEKLE"""    
    def siparis_ekle(self):
        musteri_adi = self.ui_menu.Mteriad.text().strip()
        urun_adi = self.ui_menu.CB_urunsecimi.currentText()
        miktar = self.ui_menu.SB_adet_2.value()
    
        if not musteri_adi:
            QMessageBox.warning(self, "Hata", "Müşteri adı boş bırakılamaz.")
            return
        if miktar <= 0:
            QMessageBox.warning(self, "Hata", "Miktar 0'dan büyük olmalıdır.")
            return
    
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        curs.execute("SELECT id, fiyat, miktar FROM Menü WHERE urun_adi=?", (urun_adi,))
        urun = curs.fetchone()
    
        if not urun:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı.")
            conn.close()
            return
    
        urun_id, fiyat, stok_miktar = urun
    
        if miktar > stok_miktar:
            QMessageBox.warning(self, "Stok Hatası", f"Stokta yalnızca {stok_miktar} adet var.")
            conn.close()
            return
    
        toplam_tutar = fiyat * miktar
        from datetime import datetime
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        curs.execute("""
            INSERT INTO siparisler (musteri_adi, urun_id, miktar, tarih, toplam_tutar)
            VALUES (?, ?, ?, ?, ?)
        """, (musteri_adi, urun_id, miktar, tarih, toplam_tutar))
    
        yeni_stok = stok_miktar - miktar
        curs.execute("UPDATE Menü SET miktar=? WHERE id=?", (yeni_stok, urun_id))
    
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Sipariş başarıyla eklendi.")
        self.ui_menu.Mteriad.clear()
        self.ui_menu.SB_adet_2.setValue(0)
        self.combobox_doldur()
        self.tabloyu_doldur()
        self.siparisleri_goster()

    
    """ŞİPARİŞ LİSTELE"""
    def siparisleri_goster(self):
        
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        # JOIN ile urun_adi da gelsin
        curs.execute('''
            SELECT s.id, s.musteri_adi, m.urun_adi, s.miktar, s.tarih, s.toplam_tutar
            FROM siparisler s
            JOIN Menü m ON s.urun_id = m.id
            ORDER BY s.tarih DESC
        ''')
        veriler = curs.fetchall()
        conn.close()
    
        self.ui_menu.tableWidget_menu_2.setRowCount(len(veriler))
        self.ui_menu.tableWidget_menu_2.setColumnCount(6)
        self.ui_menu.tableWidget_menu_2.setHorizontalHeaderLabels([
            "ID", "Müşteri Adı", "Ürün Adı", "Miktar", "Tarih", "Toplam Tutar"
        ])
    
        for row_idx, satir in enumerate(veriler):
            for col_idx, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                self.ui_menu.tableWidget_menu_2.setItem(row_idx, col_idx, item)
    
        self.ui_menu.tableWidget_menu_2.resizeColumnsToContents()

        
    
    
    """Satır SEÇİMİ"""
    def siparis_satiri_secildi(self, row, column):
        
        secilen_id = int(self.ui_menu.tableWidget_menu_2.item(row, 0).text())
        musteri_adi = self.ui_menu.tableWidget_menu_2.item(row, 1).text()
        urun_adi = self.ui_menu.tableWidget_menu_2.item(row, 2).text()
        miktar = int(self.ui_menu.tableWidget_menu_2.item(row, 3).text())
    
        self.ui_menu.Mteriad.setText(musteri_adi)
        self.ui_menu.CB_urunsecimi.setCurrentText(urun_adi)
        self.ui_menu.SB_adet_2.setValue(miktar)

        try:
            
            siparis_id = int(self.ui_menu.tableWidget_menu_2.item(row, 0).text())
    
            conn = sqlite3.connect("Veritabani_Yemek.db")
            curs = conn.cursor()
    
            # Sipariş bilgilerini getir
            curs.execute("""
                SELECT s.musteri_adi, m.urun_adi, s.miktar
                FROM siparisler s
                JOIN Menü m ON s.urun_id = m.id
                WHERE s.id = ?
            """, (siparis_id,))
            veri = curs.fetchone()
            conn.close()
    
            if veri:
                musteri_adi, urun_adi, miktar = veri
                self.ui_menu.Mteriad.setText(musteri_adi)
                self.ui_menu.CB_urunsecimi.setCurrentText(urun_adi)
                self.ui_menu.SB_adet_2.setValue(miktar)
        except Exception as e:
            print("Hata:", e)
            QMessageBox.warning(self, "Hata", "Sipariş bilgileri alınırken bir hata oluştu.")

    
    
    
    
    
    """SİPARİŞ GUNCELLE"""
    def siparis_guncelle(self):
        secilen_satir = self.ui_menu.tableWidget_menu_2.currentRow()
        if secilen_satir == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellemek için bir sipariş seçin.")
            return
    
        siparis_id = int(self.ui_menu.tableWidget_menu_2.item(secilen_satir, 0).text())
        musteri_adi = self.ui_menu.Mteriad.text().strip()
        yeni_urun_adi = self.ui_menu.CB_urunsecimi.currentText()
        yeni_miktar = self.ui_menu.SB_adet_2.value()
    
        if not musteri_adi:
            QMessageBox.warning(self, "Hata", "Müşteri adı boş olamaz!")
            return
        if yeni_miktar <= 0:
            QMessageBox.warning(self, "Hata", "Miktar sıfırdan büyük olmalıdır!")
            return
    
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        # Eski siparişi bul
        curs.execute("SELECT urun_id, miktar FROM siparisler WHERE id=?", (siparis_id,))
        eski_siparis = curs.fetchone()
        if not eski_siparis:
            QMessageBox.warning(self, "Hata", "Sipariş bulunamadı!")
            conn.close()
            return
    
        eski_urun_id, eski_miktar = eski_siparis
    
        # Eski ürün stoğunu geri ekle
        curs.execute("UPDATE Menü SET miktar = miktar + ? WHERE id=?", (eski_miktar, eski_urun_id))
    
        # Yeni ürün bilgilerini al
        curs.execute("SELECT id, fiyat, miktar FROM Menü WHERE urun_adi=?", (yeni_urun_adi,))
        yeni_urun = curs.fetchone()
        if not yeni_urun:
            QMessageBox.warning(self, "Hata", "Seçilen ürün veritabanında bulunamadı!")
            conn.close()
            return
    
        yeni_urun_id, fiyat, mevcut_stok = yeni_urun
        if yeni_miktar > mevcut_stok:
            QMessageBox.warning(self, "Stok Yetersiz", f"Stokta sadece {mevcut_stok} adet var.")
            conn.close()
            return
    
        yeni_tutar = fiyat * yeni_miktar
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        # Siparişi güncelle
        curs.execute('''
            UPDATE siparisler SET musteri_adi=?, urun_id=?, miktar=?, tarih=?, toplam_tutar=?
            WHERE id=?
        ''', (musteri_adi, yeni_urun_id, yeni_miktar, tarih, yeni_tutar, siparis_id))
    
        # Yeni ürün stoktan düş
        curs.execute("UPDATE Menü SET miktar = miktar - ? WHERE id=?", (yeni_miktar, yeni_urun_id))
    
        conn.commit()
        conn.close()
    
        QMessageBox.information(self, "Başarılı", "Sipariş başarıyla güncellendi.")
        self.ui_menu.Mteriad.clear()
        self.ui_menu.SB_adet_2.setValue(0)
        self.combobox_doldur()
        self.tabloyu_doldur()
        self.siparisleri_goster()

        
    """SİPARİŞ SİL BUTONU """
    def silSiparis(self):
        secili_satir = self.ui_menu.tableWidget_menu_2.currentRow()
    
        if secili_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir sipariş seçin.")
            return
    
        siparis_id = int(self.ui_menu.tableWidget_menu_2.item(secili_satir, 0).text())
    
        cevap = QMessageBox.question(
            self,
            "Sipariş Silme",
            "Bu siparişi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if cevap == QMessageBox.Yes:
            try:
                conn = sqlite3.connect("Veritabani_Yemek.db")
                curs = conn.cursor()
    
                # 1. Sipariş bilgilerini al (stok geri eklenecek)
                curs.execute("""
                    SELECT urun_id, miktar FROM siparisler WHERE id = ?
                """, (siparis_id,))
                siparis = curs.fetchone()
    
                if siparis:
                    urun_id, miktar = siparis
    
                    # 2. Stoku geri yükle
                    curs.execute("""
                        UPDATE Menü SET miktar = miktar + ? WHERE id = ?
                    """, (miktar, urun_id))
    
                    # 3. Siparişi sil
                    curs.execute("DELETE FROM siparisler WHERE id = ?", (siparis_id,))
    
                    conn.commit()
                    conn.close()
    
                    # Tabloyu güncelle
                    self.ui_menu.tableWidget_menu_2.removeRow(secili_satir)
    
                    QMessageBox.information(self, "Başarılı", "Sipariş başarıyla silindi.")
                    self.combobox_doldur()
                    self.tabloyu_doldur()
                    self.siparisleri_goster()
                else:
                    QMessageBox.warning(self, "Hata", "Sipariş bulunamadı!")
    
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")
                
                
                
    """RAPORLAR SAYFASI """
    def rapor_tablosunu_doldur(self):
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        curs.execute('''
            SELECT m.urun_adi, 
                   SUM(s.miktar) AS toplam_miktar,
                   SUM(s.toplam_tutar) AS toplam_tutar
            FROM siparisler s
            JOIN Menü m ON s.urun_id = m.id
            GROUP BY s.urun_id
            ORDER BY toplam_tutar DESC
        ''')
    
        veriler = curs.fetchall()
        conn.close()
    
        self.ui_menu.tableWidget_Raporlar.setRowCount(0)
        self.ui_menu.tableWidget_Raporlar.setColumnCount(3)
        self.ui_menu.tableWidget_Raporlar.setHorizontalHeaderLabels(["Ürün Adı", "Toplam Miktar", "Toplam Tutar"])
    
        for satir_num, satir in enumerate(veriler):
            self.ui_menu.tableWidget_Raporlar.insertRow(satir_num)
            for sutun_num, veri in enumerate(satir):
                self.ui_menu.tableWidget_Raporlar.setItem(satir_num, sutun_num, QTableWidgetItem(str(veri)))
    """SAYFA DEĞİŞTİĞİNDE OTOMATİK RAPORLAR TABLOSUNU DOLDURMA"""            
    def sayfaDegisti(self, index):
        if index == 2:  # 4. sekme (sıfırdan başladığı için)
            self.rapor_tablosunu_doldur()
    """RAPORU GÖRÜNTÜLE BUTONU İÇİN EXCELDE DOSYA AÇMA """        
    
    
    def raporu_excele_aktar(self):
        from openpyxl import Workbook # type: ignore
        from PyQt5.QtWidgets import QFileDialog
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        curs.execute('''
            SELECT m.urun_adi, 
                   SUM(s.miktar) AS toplam_miktar,
                   SUM(s.toplam_tutar) AS toplam_tutar
            FROM siparisler s
            JOIN Menü m ON s.urun_id = m.id
            GROUP BY s.urun_id
            ORDER BY toplam_tutar DESC
        ''')
        veriler = curs.fetchall()
        conn.close()
    
        # Excel dosyası oluştur
        wb = Workbook()
        ws = wb.active
        ws.title = "Rapor"
    
        # Başlıklar
        ws.append(["Ürün Adı", "Toplam Miktar", "Toplam Tutar"])
    
        # Veriler
        for veri in veriler:
            ws.append(veri)
    
        # Dosya konumunu seçtir
        dosya_yolu, _ = QFileDialog.getSaveFileName(None, "Excel Olarak Kaydet", "", "Excel Files (*.xlsx)")
        if dosya_yolu:
            if not dosya_yolu.endswith(".xlsx"):
                dosya_yolu += ".xlsx"
            wb.save(dosya_yolu)
            print("Rapor başarıyla kaydedildi:", dosya_yolu)
            
            
    """ÇALIŞAN YÖNETİMİ SAYFASI METHODLARI"""
    
    """ÇALIŞAN EKLEME BUTONU """
    def calisan_ekle(self):
        isim = self.ui_menu.LE_Calisanadi.text()
        soyisim = self.ui_menu.LE_Soyadi.text()
        tel_no = self.ui_menu.LE_Tel.text()
        departman = self.ui_menu.LE_Departman.text()
        kullanici_adi = self.ui_menu.LE_Kullaniciadi.text()
        sifre = self.ui_menu.LE_Sifre.text()
    
        if not (isim and soyisim and departman and kullanici_adi and sifre):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm zorunlu alanları doldurun.")
            return
    
        try:
            conn = sqlite3.connect("Veritabani_Yemek.db")
            curs = conn.cursor()
            curs.execute('''
                INSERT INTO calisanlar (isim, soyisim, tel_no, departman, kullanici_adi, sifre)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (isim, soyisim, tel_no, departman, kullanici_adi, sifre))
            conn.commit()
            conn.close()
    
            QMessageBox.information(self, "Başarılı", "Çalışan başarıyla eklendi.")
            self.calisan_tablosunu_doldur()
    
            # Girişleri temizle
            self.ui_menu.LE_Calisanadi.clear()
            self.ui_menu.LE_Soyadi.clear()
            self.ui_menu.LE_Tel.clear()
            self.ui_menu.LE_Departman.clear()
            self.ui_menu.LE_Kullaniciadi.clear()
            self.ui_menu.LE_Sifre.clear()
    
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kayıtlı!")

    
    
    
    
    
    """ÇALIŞAN TABLOSU DOLDURMA """
    
    """ÇALLISAN VERİSİ ÇEKME """            
    def calisan_tablosunu_doldur(self):
        import sqlite3
        from PyQt5.QtWidgets import QTableWidgetItem
    
        # Veritabanı bağlantısı
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
    
        # Tablodan çalışan verilerini çek
        curs.execute("SELECT id, isim, soyisim, tel_no, departman, kullanici_adi FROM calisanlar")
        calisanlar = curs.fetchall()
    
        conn.close()
    
        # Tabloyu sıfırla
        self.ui_menu.tableWidget_Calisanlar.setRowCount(0)
        self.ui_menu.tableWidget_Calisanlar.setColumnCount(6)
        self.ui_menu.tableWidget_Calisanlar.setHorizontalHeaderLabels([
            "ID", "İsim", "Soyisim", "Telefon", "Departman", "Kullanıcı Adı"
        ])
    
        # Verileri tabloya yaz
        for satir_num, satir in enumerate(calisanlar):
            self.ui_menu.tableWidget_Calisanlar.insertRow(satir_num)
            for sutun_num, veri in enumerate(satir):
                item = QTableWidgetItem(str(veri))
                self.ui_menu.tableWidget_Calisanlar.setItem(satir_num, sutun_num, item)
                
    """SAYFA DEĞİŞTİĞİNDE TABLO GETİR"""            
    def sayfaDegistir(self, index):
        if index == 3:  # "Çalışanlar" sekmesinin index'ine göre ayarla
            self.calisan_tablosunu_doldur()
            
            
    """GÜNCELLEME BUTONU METHODU"""
    def calisan_verilerini_getir(self):
        try:
            secili_satir = self.ui_menu.tableWidget_Calisanlar.currentRow()
            if secili_satir != -1:
                self.secilen_calisan_id = self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 0).text()
                print(f"ID alındı: {self.secilen_calisan_id}")
                self.ui_menu.LE_Calisanadi.setText(self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 1).text())
                self.ui_menu.LE_Soyadi.setText(self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 2).text())
                self.ui_menu.LE_Tel.setText(self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 3).text())
                self.ui_menu.LE_Departman.setText(self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 4).text())
                self.ui_menu.LE_Kullaniciadi.setText(self.ui_menu.tableWidget_Calisanlar.item(secili_satir, 5).text())
        except Exception as e:
            print("Hata:", e)

    """Çlaışan guncelle"""        
    def calisan_guncelle(self):
        if not hasattr(self, "secilen_calisan_id"):
            QMessageBox.warning(self, "Hata", "Lütfen önce bir çalışan seçin.")
            return
    
        isim = self.ui_menu.LE_Calisanadi.text()
        soyisim = self.ui_menu.LE_Soyadi.text()
        tel_no = self.ui_menu.LE_Tel.text()
        departman = self.ui_menu.LE_Departman.text()
        kullanici_adi = self.ui_menu.LE_Kullaniciadi.text()
        sifre = self.ui_menu.LE_Sifre.text()
    
        conn = sqlite3.connect("Veritabani_Yemek.db")
        curs = conn.cursor()
        curs.execute('''
            UPDATE calisanlar
            SET isim=?, soyisim=?, tel_no=?, departman=?, kullanici_adi=?, sifre=?
            WHERE id=?
        ''', (isim, soyisim, tel_no, departman, kullanici_adi, sifre, self.secilen_calisan_id))
        conn.commit()
        conn.close()
    
        QMessageBox.information(self, "Başarılı", "Çalışan bilgileri güncellendi.")
        self.calisan_tablosunu_doldur()
        
        
    """"Çlışan Sil"""
    def calisan_sil(self):
        if not hasattr(self, "secilen_calisan_id"):
            QMessageBox.warning(self, "Hata", "Lütfen önce silmek istediğiniz çalışanı tablodan seçin.")
            return
    
        cevap = QMessageBox.question(
            self, "Onay", "Bu çalışanı silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if cevap == QMessageBox.Yes:
            try:
                conn = sqlite3.connect("Veritabani_Yemek.db")
                curs = conn.cursor()
                curs.execute("DELETE FROM calisanlar WHERE id = ?", (self.secilen_calisan_id,))
                conn.commit()
                conn.close()
    
                QMessageBox.information(self, "Başarılı", "Çalışan başarıyla silindi.")
                self.calisan_tablosunu_doldur()  # tabloyu güncelle
    
                # Seçilen ID'yi sıfırla
                del self.secilen_calisan_id
    
                # Giriş kutularını temizle
                self.ui_menu.LE_Calisanadi.clear()
                self.ui_menu.LE_Soyadi.clear()
                self.ui_menu.LE_Tel.clear()
                self.ui_menu.LE_Departman.clear()
                self.ui_menu.LE_Kullaniciadi.clear()
                self.ui_menu.LE_Sifre.clear()
    
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Silme işlemi sırasında hata oluştu:\n{str(e)}")
                
                
                
    """UYGULAMAYI KAPATMA TUŞU ÇIKIŞ BUTONU METHODU"""
    

    from PyQt5.QtWidgets import QApplication

    def uygulamayi_kapat(self):
        cevap = QMessageBox.question(
            self, "Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if cevap == QMessageBox.Yes:
            for widget in QApplication.topLevelWidgets():
                widget.close()

            



# --- Uygulama Başlat ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = LoginEkrani()
    pencere.show()
    sys.exit(app.exec())







