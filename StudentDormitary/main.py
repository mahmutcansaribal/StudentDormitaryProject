'''
MAHMUT CAN SARIBAL  16008119031 BİLGİSAYAR MÜHENDİSLİĞİ YOZGAT BOZOK ÜNİVERSİTESİ

GEREKLİ KÜTÜPHANELER

pip install PyQt5
pip install requests

'''
import os
import sys
import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QComboBox, QMessageBox, QFormLayout, QDialog,QTableWidget, QTableWidgetItem,QListWidget,QDateEdit,QListWidgetItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QDateEdit,QCalendarWidget
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, QFile, QTextStream
import http.client
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyQt5.QtCore import QByteArray
import sqlite3

conn = http.client.HTTPSConnection("api.collectapi.com") # APİ ÇEKİLDİĞİ SİTE


def connect_to_database():
    database_name = "StudentDormitary/VeriTabaniArayuz.db"
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    return connection, cursor

def veriTabaniSorgulama(kullaniciAdi,Sifre):
    connection, cursor = connect_to_database()
    try:
        sorgu = "SELECT * FROM Ogrenci WHERE ogr_Adi = ? AND Sifre = ?"
        cursor.execute(sorgu,(kullaniciAdi,Sifre))
        kullanici = cursor.fetchone()
    except:
        QMessageBox.warning(None,"Başarısız", "KULLANICI BULUNAMADI")
    try:
        if kullanici is not None:
            return kullanici[0]
        else:
            return None
    except Exception as e:
        print(f"Hata : {e}")
    finally:
        connection.close()
        


class VeritabaniIslemleri:
    def __init__(self, veritabani_adi):
        self.baglanti = sqlite3.connect(veritabani_adi)
        self.cursor = self.baglanti.cursor()
    def baglantiyi_kapat(self):
        self.baglanti.close()

    # BU KOD PARÇASI veriTabaniSorgulama FONKSİYONU İLE DEĞİŞTİRİLMİŞTİR.

    # def kullanici_giris_kontrol(self, kullanici_adi, sifre):
    #     sorgu = "SELECT * FROM Ogrenci WHERE ogr_Adi = ? AND Sifre = ?"
    #     self.cursor.execute(sorgu, (kullanici_adi, sifre))
    #     kullanici = self.cursor.fetchone()

    #     if kullanici is not None:
    #         # Eğer kullanıcı varsa, öğrenci ID'sini döndür
    #         return kullanici[0]  # Burada kullanici[0], Ogrenci tablosundaki Ogr_ID sütununu temsil eder.
    #     else:
    #         return None

    

class GirisEkrani(QDialog):
    def __init__(self, veritabani, parent=None):
        super().__init__(parent)
        self.veritabani = veritabani
        self.init_ui()
        self.setFixedSize(250, 250)

    def init_ui(self):
        self.setWindowTitle("Giriş Ekranı")

        layout = QFormLayout()

        self.kullaniciAdInput = QLineEdit()
        self.kullaniciSifre = QLineEdit()
        self.kullaniciSifre.setEchoMode(QLineEdit.Password)

        layout.addRow(QLabel("Kullanıcı Adı : "), self.kullaniciAdInput)
        layout.addRow(QLabel("Şifre : "), self.kullaniciSifre)

        giris_button = QPushButton('Giriş Yap')
        giris_button.clicked.connect(self.BilgileriKontrolEt)
        layout.addWidget(giris_button)

        kayitOlButon = QPushButton("Kayıt Ol!")
        layout.addWidget(kayitOlButon)

        kayitOlButon.clicked.connect(self.KayitOl)
        

        self.setLayout(layout)
    
    

    def BilgileriKontrolEt(self):
        kullaniciad = self.kullaniciAdInput.text()
        sifreKontrol = self.kullaniciSifre.text()

        # ogr_id = self.veritabani.kullanici_giris_kontrol(kullaniciad, sifreKontrol) ## ESKİ KOD PARÇASI
        ogr_id = veriTabaniSorgulama(kullaniciad,sifreKontrol)

        if ogr_id is not None:
            self.ogr_id = ogr_id
            print(int(self.ogr_id))
            print(type(self.ogr_id))
            QMessageBox.information(self, "Başarılı", "GİRİŞ BAŞARILIDIR")
            self.accept()
            anaSayfa = AnaSayfa(self.ogr_id)
            anaSayfa.exec_()
        else:
            QMessageBox.warning(self, 'Hata', 'Kullanıcı adı veya şifre hatalı!')
    def KayitOl(self):
       kayitOl = KayitOl()
       kayitOl.exec_()

    def closeEvent(self, event):
        self.veritabani.baglantiyi_kapat()
        event.accept()
class KayitOl(QDialog):
    def __init__(self):
        super().__init__()
        self.kayitOlForm()
        self.setFixedSize(250, 250)
    def kayitOlForm(self):
        layout = QFormLayout()

        self.OgrenciAdi = QLineEdit()
        self.OgrenciSifre = QLineEdit()
        self.Bolum = QComboBox()
        self.Bolum.addItems(['Bilgisayar Mühendisliği', 'Elektrik Mühendisliği','Tıp',"Okul Öncesi","FizyoTerapist"])
        # Resim Seç butonu ve etkinlik işleyicisi
        self.resim_sec_btn = QPushButton('Resim Seç')
        self.resim_sec_btn.clicked.connect(self.resimSec)

        self.KaydetBtn = QPushButton('Kaydol!')
        self.KaydetBtn.clicked.connect(self.BilgileriKontrolEt)

        layout.addRow(QLabel("OgrenciAdi : "), self.OgrenciAdi)
        layout.addRow(QLabel("Şifre : "), self.OgrenciSifre)
        layout.addRow(QLabel("Bolum : "), self.Bolum)

        # Resim Seç butonunu ekleyin
        layout.addRow(QLabel("Resim Seç : "), self.resim_sec_btn)
        layout.addWidget(self.KaydetBtn)

        self.setLayout(layout)

    def resimSec(self):
        
        self.resimDosyasi, _ = QFileDialog.getOpenFileName(self, 'Resim Seç', '', 'Resim Dosyaları (*.png *.jpg *.bmp *.jpeg)')
        if self.resimDosyasi:
            with open(self.resimDosyasi, 'rb') as file:
                self.resimBytes = file.read()
            # print(self.resimDosyasi)
    
    def BilgileriKontrolEt(self):
        kullaniciad = self.OgrenciAdi.text()
        sifreKontrol = self.OgrenciSifre.text()
        resimKontrol = getattr(self, 'resimBytes', None)
        turkceKarakter = "ŞşÇçĞğÖöÜüİı"
        if kullaniciad == "":
            QMessageBox.warning(self, 'Hata', 'Kullanici Adı bos gecilemez!')
            return False
        if resimKontrol is None:
            QMessageBox.warning(self, 'Hata', 'Resim seçilmemiş!')
            return False
        for karakter in sifreKontrol:
            if karakter in turkceKarakter:
                QMessageBox.warning(self, 'Hata', 'şifreniz Türkçe karakter içermemelidir.')
                return False
            
        if len(kullaniciad) < 5:
            QMessageBox.warning(self, 'Hata', 'Kullanici Adı 5 karakterden kısa olamaz!')
            return False
        if True:
            self.sifreKontrol(sifreKontrol)
        

    def sifreKontrol(self, kelime):
        if kelime == "":
            QMessageBox.warning(self, 'Hata', 'Şifre bos gecilemez ')
            return False
        if len(kelime) < 5:
            QMessageBox.warning(self, 'Hata', 'Şifre 5 karakterden kısa olamaz!')
            return False
        if not any(harf.islower() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre küçük karakter içermeli ')
            return False
        if not any(harf.isupper() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre büyük karakter içermeli ')
            return False
        if not any(not harf.isalnum() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre özel karakter içermeli ')
            return False
        if(True):
            self.OgrenciEkle()
    def OgrenciEkle(self):
        connection, cursor = connect_to_database()
        OgrenciAdi = self.OgrenciAdi.text()
        OgrenciSifre = self.OgrenciSifre.text()
        

        # İzin verilerini ekleme sorgusu
        insert_query = "INSERT INTO Ogrenci (ogr_Adi, Sifre, fotograf, bolum) VALUES (?, ?, ?, ?)"
        # Burada sorguya uygun değerleri ekleyin. Örneğin, ogr_id'yi self.OgrenciNumarasi olarak aldık.
        values = (self.OgrenciAdi.text(),self.OgrenciSifre.text(),self.resimBytes,self.Bolum.currentText())
        
        try:
            cursor.execute(insert_query, values)
            connection.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla tamamlandı!")
            ogr_id = veriTabaniSorgulama(OgrenciAdi,OgrenciSifre)
            ogrIzinEkle = "INSERT INTO IzinTablosu (KalanIzin, Ogr_ID) VALUES (45, ?)"
            values = (ogr_id,)
            cursor.execute(ogrIzinEkle, values)
            connection.commit()
            self.close()
        except Exception as e:
            print(f"Hata : {e}")


class izinEkrani(QDialog): # İZİN EKRANI SINIFI
    def __init__(self,ogr_id,parent=None):
        super().__init__()
        self.OgrenciNumarasi = ogr_id
        # self.parent_widget = parent 
        self.ana_sayfa = parent  # ANA SAYFA SINIFINDAN MİRAS (KALITIM) ALINIR.
        self.izinSayfasi() # İZİN SAYFASI FONKSİYONU ÇAĞRILIR
        
    
    def izinSayfasi(self):
        
        
        self.setWindowTitle("İzin Al") # İZİN SAYFASININ BAŞLIĞI
        # print("Ogrenci ID",self.OgrenciNumarasi)
        layout = QVBoxLayout()

        tarih_label = QLabel("Baslangic Tarihi : ")
        self.baslangic_tarihi = QDateEdit()
        self.baslangic_tarihi.setCalendarPopup(True) # TAKVİM POP-UP OLARAK AÇILIR
        self.baslangic_tarihi.setDate(QDate.currentDate()) # ŞUANKİ BİLGİSAYARDA OLAN TARİHİ YAZAR.
        self.baslangic_tarihi.setMinimumDate(QDate.currentDate()) # ŞUANKİ TARİHTEN ÖNCESİNİ KAPATIR VE SEÇİLEMEZ HALE GETİRİR.
        layout.addWidget(tarih_label)
        layout.addWidget(self.baslangic_tarihi)

        bitis_tarih_label = QLabel("Bitiş Tarihi:")
        self.bitis_tarihi = QDateEdit()
        self.bitis_tarihi.setDate(QDate.currentDate())
        self.bitis_tarihi.setCalendarPopup(True)
        self.bitis_tarihi.setMinimumDate(QDate.currentDate())
        layout.addWidget(bitis_tarih_label)
        layout.addWidget(self.bitis_tarihi)

        izin_al_button = QPushButton('İzin Al')
        izin_al_button.clicked.connect(self.izin_al) # BUTONA TIKLANDIKTAN SONRA İZİN_AL FONKSİYONUNA GİDER.
        layout.addWidget(izin_al_button)

        self.setLayout(layout)
    
    def izin_al(self):
        
        baslangic_tarihi = self.baslangic_tarihi.date() # İZİN SAYFASINDAN GELEN BAŞLANGIÇ TARİHİNİ TEXT OLARAK ATAR.
        bitis_tarihi = self.bitis_tarihi.date() # İZİN SAYFASINDAN GELEN BİTİŞ TARİHİNİ TEXT OLARAK ATAR.

        # Gün farkını hesapla
        gun_farki = baslangic_tarihi.daysTo(bitis_tarihi) # BAŞLANGIÇ TARİHİ İLE BİTİŞ TARİHİ ARASINDAKİ GÜN FARKINI HESAPLAR BU SAYEDE İZİN HAKKINDAN GÜN AZALTILIR.

        # Eğer gün farkı negatifse (bitiş tarihi başlangıç tarihinden önceyse), hata göster
        if gun_farki <= 0:
            QMessageBox.warning(self, 'Hata', 'Geçerli bir tarih aralığı seçiniz!')
            return
        # ANA SAYFAMIZDA BELİRLEDİĞİMİZ İZİN HAKKIMIZ (45 GÜN) GÜN FARKINDAN AZ İSE İZİN HAKKIMIZ KALMAMIŞTIR DEMEKTEDİR.
        
        if gun_farki >= 45:
            QMessageBox.warning(self, 'Hata', '45 günden fazla izin alamazsınız')
            return
        durum = self.izinHakkiSorgulama(gun_farki)
        if durum == True:
            self.accept()
            self.izin_verilerini_veritabanina_ekle(baslangic_tarihi, bitis_tarihi, gun_farki)
        else:
            QMessageBox.information(self, 'Bilgi', 'İzin Eklenemedi')

    def izin_verilerini_veritabanina_ekle(self, baslangic_tarihi, bitis_tarihi, AlinanIzin):
        connection, cursor = connect_to_database()
        

        # İzin verilerini ekleme sorgusu
        insert_query = "INSERT INTO IzinTablosu (BaslangicTarihi, Ogr_ID, BitisTarih,AlinanIzin) VALUES (?, ?, ?, ?)"
        # Burada sorguya uygun değerleri ekleyin. Örneğin, ogr_id'yi self.OgrenciNumarasi olarak aldık.
        values = (baslangic_tarihi.toString('yyyy-MM-dd'), self.OgrenciNumarasi, bitis_tarihi.toString('yyyy-MM-dd'),AlinanIzin)

        try:
            cursor.execute(insert_query, values)
            connection.commit()
            QMessageBox.information(self, "Başarılı", "İzin başarıyla eklendi!")

            update_query = "UPDATE IzinTablosu SET KalanIzin = KalanIzin - ? WHERE Ogr_ID = ?"
            update_values = (AlinanIzin, self.OgrenciNumarasi)
            cursor.execute(update_query, update_values)

            connection.commit()

        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hata nedeni: {str(e)}")
        finally:
            self.ana_sayfa.izinTablo.clear()
            self.ana_sayfa.get_izinler_from_database()
            self.ana_sayfa.KalanIzinHakkıGetir()
            connection.close()
    
    def izinHakkiSorgulama(self,gelenDeger):

        connection, cursor = connect_to_database()
        try:
            sorgu = "select KalanIzin from IzinTablosu where Ogr_ID = ?"
            cursor.execute(sorgu,(self.OgrenciNumarasi,))
            result = cursor.fetchone()

            print(result[0])
            if gelenDeger > result[0]:
                QMessageBox.warning(self,'UYARI','KALAN IZIN HAKKINIZDAN FAZLA İZİN ALAMAZSINIZ')
                return False
            if result[0] <= 0:
                QMessageBox.warning(self,'UYARI','İZİN HAKKINIZ KALMAMIŞTIR!')
                return False
            else:
                return True
        except Exception as e:
            QMessageBox.warning(self,'HATA',f'{e}')
        finally:
            connection.close()
    
class ProfilAyarlarForm(QDialog):
    def __init__(self,ogr_id,parent=None):
        super().__init__()
        self.OgrenciNumarasi = ogr_id
        self.ana_sayfa = parent
        self.initUI()
        

    def initUI(self):
        # print(self.OgrenciNumarasi)
        self.setWindowTitle('Profil Ayarları')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.profilResimLabel = QLabel(self)
        self.profilResimLabel.setFixedSize(150, 150)

        self.resimSecBtn = QPushButton('Resim Seç')
        self.resimSecBtn.clicked.connect(self.resimSec)

        self.OgrenciAdi = QLineEdit()
        self.OgrenciSifre = QLineEdit()
        self.Bolum = QComboBox()
        self.Bolum.addItems(['Bilgisayar Mühendisliği', 'Elektrik Mühendisliği','Tıp',"Okul Öncesi","FizyoTerapist"])

        self.kaydetBtn = QPushButton('Profil Güncelle')
        self.kaydetBtn.clicked.connect(self.sifreKontrol)

        formLayout = QFormLayout()
        formLayout.addRow('Profil Resmi:', self.profilResimLabel)
        formLayout.addRow('Resim Seç:', self.resimSecBtn)
        formLayout.addRow("Bolum Seç:",self.Bolum)
        formLayout.addRow('Kullanıcı Sifre:', self.OgrenciSifre)


        layout.addLayout(formLayout)
        layout.addWidget(self.kaydetBtn)

        self.setLayout(layout)

    def sifreKontrol(self):
        kelime = self.OgrenciSifre.text()
        if kelime == "":
            QMessageBox.warning(self, 'Hata', 'Şifre bos gecilemez ')
            return False
        if len(kelime) < 5:
            QMessageBox.warning(self, 'Hata', 'Şifre 5 karakterden kısa olamaz!')
            return False
        if not any(harf.islower() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre küçük karakter içermeli ')
            return False
        if not any(harf.isupper() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre büyük karakter içermeli ')
            return False
        if not any(not harf.isalnum() for harf in kelime):
            QMessageBox.warning(self, 'Hata', 'Şifre özel karakter içermeli ')
            return False
        if(True):
            self.AyarlariKaydet()
    def resimSec(self):
        
        self.resimDosyasi, _ = QFileDialog.getOpenFileName(self, 'Resim Seç', '', 'Resim Dosyaları (*.png *.jpg *.bmp *.jpeg)')
        if self.resimDosyasi:
            with open(self.resimDosyasi, 'rb') as file:
                self.resimBytes = file.read()
                self.gosterResim(self.resimDosyasi)
            print(self.resimDosyasi)
    
    def gosterResim(self, resimDosyasi):
        # Resmi QLabel içinde göster
        self.resim = QPixmap(resimDosyasi)
        self.profilResimLabel.setPixmap(self.resim.scaledToWidth(150))

    # Profil güncelleme fonksiyonu
    def AyarlariKaydet(self):
        connection, cursor = connect_to_database()
        

        try:
            update_query = "UPDATE Ogrenci SET Sifre = ?, fotograf = ?, bolum = ? Where Ogr_ID = ?"
            update_values = (self.OgrenciSifre.text(), self.resimBytes,self.Bolum.currentText(),self.OgrenciNumarasi)
            cursor.execute(update_query, update_values)

            connection.commit()
            QMessageBox.information(self,"Bilgi","Profil Bilgileri Basariyla Guncellendi!")
            QMessageBox.warning(self,"Uyari","Resmin guncellenmesi için tekrar giriş yapiniz!")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hata nedeni: {str(e)}")
        finally:
            self.ana_sayfa.ResimYukleOgrenci()
            connection.close()

class Sabahyemegi(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(575,500)
        self.SabahYemegiSayfasi()

    def SabahYemegiSayfasi(self):
        kahvalti_layout = QVBoxLayout(self)

        table_widget = QTableWidget(self)
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        table_widget.setColumnCount(4)
        table_widget.setColumnWidth(1, 200)
        table_widget.setHorizontalHeaderLabels(["Tarih", "Kahvaltı", "Yanında", "Ekstra"])

        connection, cursor = connect_to_database()

        bugun = QDate.currentDate()
        for gun in range(30):
            tarih = bugun.addDays(gun)
            tarih_str = tarih.toString("dd.MM.yyyy")

            # SQLite sorgusu ile SabahYemegi tablosundan verileri çek
            cursor.execute("SELECT KahvaltiAdi, Yaninda, Ekstra FROM SabahYemegi")
            results = cursor.fetchall()

            if results:
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                table_widget.setItem(row_position, 0, QTableWidgetItem(tarih_str))

                for row_position, result in enumerate(results):

                    kahvalti_adi, yaninda, ekstra = result
                    table_widget.setItem(row_position, 1, QTableWidgetItem(kahvalti_adi))
                    table_widget.setItem(row_position, 2, QTableWidgetItem(yaninda))
                    table_widget.setItem(row_position, 3, QTableWidgetItem(ekstra))

        # Bağlantıyı kapat
        connection.close()

        kahvalti_layout.addWidget(table_widget)
        self.setLayout(kahvalti_layout)


# SABAH KAHVALTISI İLE AYNI İŞLEMLER YAPILMAKTADIR.
class AksamYemegi(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(575,500)
        self.AksamYemegiSayfasi()

    def AksamYemegiSayfasi(self):
        aksam_layout = QVBoxLayout(self)

        table_widget = QTableWidget(self)
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        table_widget.setColumnCount(4)
        table_widget.setColumnWidth(1,200)
        table_widget.setHorizontalHeaderLabels(["Tarih", "Yemek","Yanında","Ekstra"])

        connection, cursor = connect_to_database()

        bugun = QDate.currentDate()
        for gun in range(30):
            tarih = bugun.addDays(gun)
            tarih_str = tarih.toString("dd.MM.yyyy")

            # SQLite sorgusu ile SabahYemegi tablosundan verileri çek
            cursor.execute("SELECT Yemek, Yaninda, Ekstra FROM AksamYemegi")
            results = cursor.fetchall()

            if results:
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                table_widget.setItem(row_position, 0, QTableWidgetItem(tarih_str))

                for row_position, result in enumerate(results):

                    kahvalti_adi, yaninda, ekstra = result
                    table_widget.setItem(row_position, 1, QTableWidgetItem(kahvalti_adi))
                    table_widget.setItem(row_position, 2, QTableWidgetItem(yaninda))
                    table_widget.setItem(row_position, 3, QTableWidgetItem(ekstra))

        # Bağlantıyı kapat
        connection.close()

        aksam_layout.addWidget(table_widget)
        self.setLayout(aksam_layout)    

class AnaSayfa(QDialog):
    def __init__(self,ogr_id):
        super().__init__()
        self.ogrNumarasi = ogr_id # Giriş yap sınıfından parametre olarak alındı.
        self.setFixedSize(1250,750) # ARAYÜZ EKRANIN BOYUTU AYARLANIR
        self.izinTablo = QListWidget(self) 
        self.izinHakki = 0 

        self.KullaniciSayfasi()
        self.yukle() # ÖNCEDEN ALINMIŞ VÜCÜT KİTLE ENDEKSİ VERİLERİNİ YÜKLER
        self.yurtDuyurulari()
        self.hava_durumu() # APİ ÜZERİNDEN HAVA DURUMU VERİLERİ ÇAĞRILIR.
        self.setWindowTitle("Yurt Takip Sistemi")
        self.get_izinler_from_database()
        self.KalanIzinHakkıGetir()
        self.ResimYukleOgrenci()
        
    def arizaTalepForm(self):
        connection,cursor = connect_to_database() 
        talepMetni = self.arizaForm.toPlainText()  
        try:
            sorgu =  "INSERT INTO ArizaTaleb (arizaYorum,Ogr_ID) VALUES (?,?)"
            values = (talepMetni,self.ogrNumarasi)
            cursor.execute(sorgu,values)
            connection.commit()
            QMessageBox.information(self,"Bilgi","Talebiniz Basariyla Gönderildi")
        except Exception as e:
            print(f"Hata : {e}")
        finally:
            self.arizaForm.clear()
            connection.close()
    def yukle(self):
        connection,cursor = connect_to_database()
        try:

            sorgu = "Select OgrenciAd,Yas,boy,Kilo,IdealKilo,Vki,Tarih,Fark,Durum from VucutKitle where Ogr_ID = ?"
            cursor.execute(sorgu,(self.ogrNumarasi,))
            veriler = cursor.fetchall()

            header = "AD\tYAŞ\tBOY\tKİLO\tİDEALKİLO\tVKİ\tTARİH\tFARK\tDURUM\n"
            formatted_veriler = [f"{veri[0]}\t{veri[1]}\t{veri[2]}\t{veri[3]}\t{veri[4]}\t{veri[5]}\t{veri[6]}\t{veri[7]}\t{veri[8]}\n" for veri in veriler]
            self.kilo_veri_girisi.insertPlainText(header + ''.join(formatted_veriler))
            
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata Nedeni: {str(e)}')
        finally:
            connection.close()
    def yurtDuyurulari(self):
        connection,cursor = connect_to_database()
        try:
            sorgu = "select Duyuru from YurtDuyurulari"
            cursor.execute(sorgu)
            duyurular  = cursor.fetchall()

            for duyuru in duyurular:
                self.yurtUyarıText.append(duyuru[0])
        except Exception as e:
            print(f"Hata : {e}")
        finally:
            connection.close()

    def ResimYukleOgrenci(self):
        connection,cursor = connect_to_database()
        try:
            sorgu = "select fotograf from Ogrenci where Ogr_ID = ?"
            cursor.execute(sorgu,(self.ogrNumarasi,))
            veri = cursor.fetchone()

            if veri:
                byte_array = QByteArray(veri[0])
                image = QImage.fromData(byte_array)
                # RESİM TANIMLAMASI
                kullaniciResimLabel = QLabel(self)
                kullaniciResim = QPixmap.fromImage(image)
                kullaniciResim = kullaniciResim.scaledToWidth(150)
                kullaniciResimLabel.setPixmap(kullaniciResim)
                kullaniciResimLabel.move(50,50)
        except Exception as e:
            print(f"Hata Resim icin : {e}")
        finally:
            connection.close()


    def KalanIzinHakkıGetir(self):
        connection, cursor = connect_to_database()
        try:
            sorgu = "select KalanIzin from IzinTablosu where Ogr_ID = ?"
            cursor.execute(sorgu,(self.ogrNumarasi,))
            results = cursor.fetchone()
            # print(results[0])
            self.guncelle_izin_Label(results[0])
        except:
            self.guncelle_izin_Label(45)
        finally:
            connection.close()
    def profilGuncelle(self,ogr_id):
        profilAyarlari = ProfilAyarlarForm(ogr_id,parent=self) # SABAH YEMEGİ SINIFINA GİDER
        profilAyarlari.exec_()

    def KullaniciSayfasi(self):

        #   BUTON TANIMLAMALARI YAPILDI.
        profilAyarlari = QPushButton("Profil Ayarlari",self)
        izinButon = QPushButton("İzin Al",self)
        izinButon.setStyleSheet("background-color: orange; color: black;")  
        sabahYemekButon = QPushButton("Sabah Yemegi",self)
        sabahYemekButon.setStyleSheet("background-color: orange; color:black;")
        aksamYemekButon = QPushButton("Aksam Yemegi",self)
        aksamYemekButon.setStyleSheet("background-color:orange; color: black;")
        arizaTalepButon = QPushButton("Talep Gonder",self)
        arizaTalepButon.setStyleSheet("background-color:orange;color:black;")
        pdfOlusturButon = QPushButton("PDF olustur",self)
        pdfOlusturButon.setStyleSheet("background-color:red; color: white;")
        kiloVerisiSilButon = QPushButton("Temizle",self)
        kiloVerisiSilButon.setStyleSheet("background-color:yellow; color:black;")
        self.kaydet_button = QPushButton('Kaydet',self)
        self.kaydet_button.setStyleSheet("background-color:green;color:white;")
        self.kiloPdfButon = QPushButton("PDF Olustur",self)
        self.kiloPdfButon.setStyleSheet("background-color:red; color: white;")
        #   BUTON KONUMLANDIRILMALARI YAPILDI.
        izinButon.setGeometry(400,300,100,100)
        sabahYemekButon.setGeometry(505,300,100,100)
        aksamYemekButon.setGeometry(610,300,100,100)
        arizaTalepButon.setGeometry(50,600,100,50)
        pdfOlusturButon.setGeometry(610,600,100,50)
        profilAyarlari.setGeometry(50,0,100,50)
        
        self.kaydet_button.setGeometry(800,600,100,50)
        kiloVerisiSilButon.setGeometry(950,600,100,50)
        self.kiloPdfButon.setGeometry(1100,600,100,50)

        # LABEL TANIMLAMALARI YAPILDI
        font = QFont()
        font.setPointSize(9)
        self.izinLabel = QLabel(f"KALAN İZİN GÜN HAKKI : {self.izinHakki} ",self)
        self.izinLabel.setStyleSheet("background-color:lightblue;color:black")
        self.izinLabel.move(400,600)
        self.izinLabel.setFont(font)
        self.izinTablo.setGeometry(400,410,308,190)


        # BUTON TIKLAMALARI
        izinButon.clicked.connect(lambda:self.izin_al_ekranina_git(self.ogrNumarasi)) # İZİN_AL_EKRANİNA_GİT FONKSİYONUNA GİDER
        sabahYemekButon.clicked.connect(self.sabah_kahvalti_ekranina_git) # SABAH_KAHVALTİ_EKRANİNA_GİT FONKSİYONUNA GİDER
        aksamYemekButon.clicked.connect(self.aksam_yemegi_ekranina_git)
        arizaTalepButon.clicked.connect(self.arizaTalepForm) # ARIZA TALEP FORM FONKSİYONUNA GİDER
        pdfOlusturButon.clicked.connect(self.createPdfIzin) # CREATE PDF IZIN FONKSİYONUNA GİDER VE İZİN PDF'İ OLUŞTURUR
        self.kaydet_button.clicked.connect(self.kaydet) # VUCUT KİTLE ENDEKSİNDEKİ VERİLERİ KAYDETMEK İÇİN KAYDET FONKSİYONUNA GİDER
        self.kiloPdfButon.clicked.connect(self.createPdf) # VUCUT KİTLE ENDEKSİNDEKİ VERİLERİ PDF'E YAZDIRMAK İÇİN CREATEPDF FONKSİYONUNA GİDER
        kiloVerisiSilButon.clicked.connect(self.temizleKiloVerisi) # VUCUT KİTLE ENDEKSİNDEKİ VERİLERİNİ SİLMEK İÇİN TEMİZLE KİLO VERİSİ FONKSİYONUNA GİDER
        profilAyarlari.clicked.connect(lambda:self.profilGuncelle(self.ogrNumarasi))

        # HAVA DURUMU
        fontHava = QFont()
        fontHava.setPointSize(20)
        self.result_label = QLabel(self)
        self.result_label.setGeometry(1100, 140, 300, 100)
        self.result_label.setFont(fontHava)


        # ARIZA BİLDİRİM FORMU
        arizaLabel = QLabel("ARIZA TALEP",self)
        arizaLabel.setStyleSheet("background-color: lightblue; color: black;")
        arizaLabel.setGeometry(50,280,100,15)
        arizaLabel.setFont(font)
        self.arizaForm = QTextEdit(self)
        self.arizaForm.setGeometry(50,300,300,300)

        # YURT DUYURULARI

        yurtUyariLabel = QLabel("YURT DUYURULARI",self)
        yurtUyariLabel.setStyleSheet("background-color:lightblue;color:black")
        yurtUyariLabel.setFont(font)
        yurtUyariLabel.setGeometry(400,10,150,12)

        self.yurtUyarıText = QTextEdit(self)
        self.yurtUyarıText.setReadOnly(True)
        self.yurtUyarıText.setGeometry(400,30,310,230)

        # FOOTER

        # VUCUT KITLE ENDEKSİ KONTROL
        
        
        boy_label = QLabel('Boy (cm):',self)
        boy_label.setStyleSheet("background-color:lightblue;color:black")
        boy_label.setGeometry(800,10,200,15)
        boy_label.setFont(font)
        boy_label2 = QLabel('Örnek veri girişi : 1.76',self)
        boy_label2.setGeometry(800,30,200,15)
        boy_label2.setFont(font)
        self.boyInput = QLineEdit(self)
        self.boyInput.setGeometry(800,50,200,20)

        kilo_label = QLabel('Kilo (kg):',self)
        kilo_label.setStyleSheet("background-color:lightblue;color:black")
        kilo_label.setGeometry(800,80,200,15)
        kilo_label.setFont(font)
        self.kilo_input = QLineEdit(self)
        self.kilo_input.setGeometry(800,100,200,20)

        cinsiyet_label = QLabel('Cinsiyet:',self)
        cinsiyet_label.setStyleSheet("background-color:lightblue;color:black")
        cinsiyet_label.setFont(font)
        cinsiyet_label.setGeometry(800,120,100,15)
        self.cinsiyet_combobox = QComboBox(self)
        self.cinsiyet_combobox.setGeometry(800,140,100,20)
        self.cinsiyet_combobox.addItems(['Erkek', 'Kadın'])

        self.yas_label = QLabel('Yaş:',self)
        self.yas_label.setStyleSheet("background-color:lightblue;color:black")
        self.yas_label.setFont(font)
        self.yas_label.setGeometry(800,160,100,15)
        self.yas_input = QLineEdit(self)
        self.yas_input.setGeometry(800,180,200,20)

        self.vucutKitle_label = QLabel('Vücut Kitle Endeksi',self)
        self.vucutKitle_label.setStyleSheet("background-color:lightblue;color:black")
        self.vucutKitle_label.setFont(font)
        self.vucutKitle_label.setGeometry(800,210,150,15)
        self.vucutKitle = QLabel('',self)
        self.vucutKitle.setFont(font)
        self.vucutKitle.setGeometry(800,230,100,15)
        self.VucutKitleUyari = QLabel('',self)
        self.VucutKitleUyari.setFont(font)
        self.VucutKitleUyari.setGeometry(800,250,100,15)

        self.olmasi_gereken_kilo_label = QLabel('Olması Gereken Kilo:')
        self.olmasi_gereken_kilo_label.setGeometry(800,250,100,15)
        self.olmasi_gereken_kilo = QLabel('')
        self.olmasi_gereken_kilo.setGeometry(800,270,100,15)

        self.ad_soyad_label = QLabel('Adı Soyadı:',self)
        self.ad_soyad_label.setStyleSheet("background-color:lightblue;color:black;")
        self.ad_soyad_label.setFont(font)
        self.ad_soyad_label.setGeometry(800,280,100,15)
        self.ad_soyad_input = QLineEdit(self)
        self.ad_soyad_input.setReadOnly(True)
        self.ad_soyad_input.setGeometry(800,300,200,20)
        try:
            connection,cursor = connect_to_database()
            ogrenciAdiSorgulama = "Select ogr_Adi from Ogrenci where Ogr_ID = ?"       
            adSoyad = cursor.execute(ogrenciAdiSorgulama, (self.ogrNumarasi,)).fetchone()
            # print(adSoyad[0])
            self.ad_soyad_input.setPlaceholderText(adSoyad[0])
        except:
            pass
        finally:
            connection.close()

        self.kilo_veri_girisi_label = QLabel('Son 10 Günlük Kilo Veri Girişleri:',self)
        self.kilo_veri_girisi_label.setFont(font)
        self.kilo_veri_girisi_label.setGeometry(800,320,200,15)
        self.kilo_veri_girisi = QTextEdit(self)
        self.kilo_veri_girisi.setReadOnly(True)
        self.kilo_veri_girisi.setGeometry(800,340,400,260)
        # self.kilo_veri_girisi.setPlainText("AD\tYAŞ\tBOY\tKİLO\tİDEALKİLO\tVKİ\tTARİH\tFARK\tDURUM\n")
        
    def get_izinler_from_database(self):
        connection, cursor = connect_to_database()

        sorgu = "Select BaslangicTarihi,BitisTarih,AlinanIzin from IzinTablosu WHERE Ogr_ID = ?"
        cursor.execute(sorgu,(self.ogrNumarasi,))
        veriler = cursor.fetchall()

        for veri in veriler:
            item_text = f"{veri[0]} - {veri[1]} ({veri[2]} gün)"
            item = QListWidgetItem(item_text)
            self.izinTablo.addItem(item)
        connection.close()

        
    def kaydet(self):
        try:
            try:
                connection,cursor = connect_to_database()
                ogrenciAdiSorgu = "SELECT Ogrenci.ogr_Adi FROM Ogrenci JOIN VucutKitle ON Ogrenci.Ogr_ID = VucutKitle.Ogr_ID WHERE Ogrenci.Ogr_ID = ?"
                adSoyad = cursor.execute(ogrenciAdiSorgu, (self.ogrNumarasi,)).fetchone()
                # print(adSoyad[0])
                self.ad_soyad_input.setPlaceholderText(adSoyad[0])
            except Exception as e:
                ogrenciAdiSorgulama = "Select ogr_Adi from Ogrenci where Ogr_ID = ?"
                adSoyad = cursor.execute(ogrenciAdiSorgulama, (self.ogrNumarasi,)).fetchone()
                # print(adSoyad[0])
                self.ad_soyad_input.setPlaceholderText(adSoyad[0])
                print(f"Hata: {e}")
            finally:
                connection.close()
            kilo = int(self.kilo_input.text())  # KULLANICININ GİRDİĞİ KİLO İNPUT'UNDAKİ VERİYİ TEXT OLARAK ALIR.
            boy = float(self.boyInput.text())
            cinsiyet = self.cinsiyet_combobox.currentText() # COMBOBOX OLARAK SEÇİM YAPTIRILIR
            yas = int(self.yas_input.text())
            tarih = datetime.now() # BUGUNÜN TARİHİ ALINIR
            tarihStr = tarih.strftime("%d.%m.%Y") 
            vki = kilo / (boy * boy) # VÜCÜT KİTLE ENDEKSİ (VKİ) HESAPLANIR
            durum = ""

            if cinsiyet == "Erkek":
                idealKilo = 50 + 2.3 * ((boy * 100 / 2.54) - 60) # ERKEK İÇİN VKİ HESAPLANIR
            else:
                idealKilo = 45.5 + 2.3 * ((boy * 100 / 2.54) - 60) # KADIN İÇİN VKİ HESAPLANIR

            if vki < 18.5:
                durum = 'İdeal Kilo Altında'
            elif 18.5 <= vki <= 24.99:
                durum = 'İdeal Kilo'
            elif 25 <= vki <= 29.99:
                durum = 'İdeal Kilo Üstü'
            elif 30 <= vki <= 39.99:
                durum = 'İdeal Kilo Aşırı Üstü'
            elif vki >= 40:
                durum = 'Obez'

            self.VucutKitleUyari.setText(durum) # VUCUT KİTLE UYARI LABELİNE DURUM DEĞİŞKENİNDEN GELEN VERİ EKLENİR.

            self.olmasi_gereken_kilo.setText(str(round(idealKilo, 2))) # OLMASI GEREKEN KİLO LABELİNE İDEAL KİLOYU YAZAR
            self.vucutKitle.setText(str(round(vki, 2)))
            fark = abs(kilo - idealKilo) # ŞUANKİ KİO VE İDEAL KİLO ARASINDAKİ KİLO FARKINI YAZAR

            self.yeni_veri = f"{adSoyad[0]}\t{yas}\t{boy}\t{kilo}\t{round(idealKilo, 2)}\t{round(vki, 2)}\t{tarihStr}\t{round(fark, 2)}\t{durum}\t"

            kilo_veri_girisi = self.kilo_veri_girisi.toPlainText().split('\n')  # Varolan kilo veri girişini satır bazında bir listeye dönüştürür.
            kilo_veri_girisi = [veri for veri in kilo_veri_girisi if veri] # Boş satırları temizler.

            

            self.kilo_veri_girisi.setPlainText(
                "AD\tYAŞ\tBOY\tKİLO\tİDEALKİLO\tVKİ\tTARİH\tFARK\tDURUM\n" + '\n'.join(kilo_veri_girisi[1:])) # : Son 10 günlük kilo veri girişini oluşturur ve QPlainTextEdit widget'ına ekler.

            kilo_veri_girisi.insert(1, self.yeni_veri) # Yeni giriş verisini listenin ikinci satırına ekler.
            kilo_veri_girisi = kilo_veri_girisi[:15] #  Liste uzunluğunu en fazla 15 satıra sınırlar.
            self.kilo_veri_girisi.setPlainText('\n'.join(kilo_veri_girisi)) # Güncellenmiş verileri QPlainTextEdit widget'ına ekler.
            self.kiloVeriGirisiKaydet(durum, round(idealKilo,2), tarihStr, adSoyad[0], round(fark,2), round(vki,2)) # KİLO VERİLERİNİ VERİ TABANINA KAYDETMEK İÇİN Kilo Veri Girisi Kaydet fonksiyonuna gider
        except ValueError:
            QMessageBox.warning(self, 'Hata', 'Lütfen geçerli sayısal değerler girin.')

    def kiloVeriGirisiKaydet(self,durum,idealKilo,tarih_str,adSoyad,fark,vki):
        connection, cursor = connect_to_database()

        try:
            sorgu = """
                INSERT INTO VucutKitle (Boy, Kilo, Cinsiyet, Yas, Ogr_ID, Tarih, IdealKilo, Durum, OgrenciAd, Fark, Vki)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                float(self.boyInput.text()),
                float(self.kilo_input.text()),
                self.cinsiyet_combobox.currentText(),
                int(self.yas_input.text()),
                self.ogrNumarasi,
                tarih_str,
                idealKilo,
                durum,
                adSoyad,
                fark,
                vki
            )
            cursor.execute(sorgu, values)
            connection.commit()


            QMessageBox.information(self, "Bilgi", "Veri başarıyla kaydedildi.")
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata Nedeni: {str(e)}')
        finally:
            connection.close()

    

    def hava_durumu(self):
        try:
            url = "https://weatherapi-com.p.rapidapi.com/current.json" # Hava durumu API'sinin endpoint'i belirlenir.
            querystring = {"q": "39.818663392,34.802663456"}
            headers = {
                "X-RapidAPI-Key": "d3cee19ac8mshc3f2051cc92a9ccp1e3a8fjsn8d357b01eca1",  # API anahtarınızı buraya ekleyin
                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com" # API'ye gönderilecek parametreler, bu durumda koordinat bilgisi olarak belirlenmiş bir konum (enlem ve boylam) içerir.
            }
            response = requests.get(url, headers=headers, params=querystring) #  Python'un requests kütüphanesi kullanılarak API'ye HTTP GET isteği gönderilir.
            data = response.json() # API'den gelen JSON formatındaki yanıt, Python veri yapısına dönüştürülür.

            # city = data.get("location", {}).get("name")
            temperature_c = data.get("current", {}).get("temp_c")
            # condition = data.get("current", {}).get("condition", {}).get("text")
            icon_url = "https:" + data.get("current", {}).get("condition", {}).get("icon")
            result_text = f"{temperature_c}°C"
            self.result_label.setText(result_text)

            # İkonu göstermek için
            self.show_icon(icon_url)
        except Exception as e:
            print("Hata : ",e)
    def show_icon(self,url):
        # İkonu göstermek için QLabel ve QPixmap kullanabilirsiniz.
        HavaResimLabel = QLabel(self)
        HavaResim = requests.get(url).content
        HavaResim = QPixmap()
        HavaResim.loadFromData(requests.get(url).content)
        HavaResim = HavaResim.scaledToWidth(100)
        HavaResimLabel.setPixmap(HavaResim)
        HavaResimLabel.setGeometry(1080,50,150,150)
        HavaResimLabel.show()

    def guncelle_izin_Label(self,yeni_deger):
        self.izinLabel.setText(f"KALAN İZİN GÜN HAKKI : {yeni_deger}")

    def izin_al_ekranina_git(self,ogrNumarasi): # İZİN AL BUTONUNA TIKLADIKTAN SONRA BURADAN IZINEKRANI SINIFINA GİDER
        izin_ekrani = izinEkrani(ogrNumarasi,parent=self)
        izin_ekrani.exec_()
    
    def sabah_kahvalti_ekranina_git(self):
        sabahKahvalti = Sabahyemegi() # SABAH YEMEGİ SINIFINA GİDER
        sabahKahvalti.exec_()
    
    def aksam_yemegi_ekranina_git(self):
        aksamYemegi = AksamYemegi()
        aksamYemegi.exec_()


    def temizleKiloVerisi(self):

        sonuc = QMessageBox.question(None,"Dikkat!","Veriler silinsin mi?", QMessageBox.Yes | QMessageBox.No)
        if sonuc == QMessageBox.Yes:
            self.kilo_veri_girisi.clear()
        else:
            QMessageBox.information(None,"Bilgi","Verilerin silinmesinden vazgecildi!")
    def createPdf(self):
        try:
            
            kilo_verileri = self.kilo_veri_girisi.toPlainText().split('\n')[1:]
            file_path = os.path.join(str(self.ogrNumarasi), "Kilo_verileri.pdf")

            # Dosya yolundaki klasörü kontrol et ve oluştur
            folder_path = os.path.dirname(file_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica", 12)

            # PDF'e başlık ekle
            c.drawString(100, 750, "Kilo Verileri Raporu")

            # Verileri PDF'e ekle
            y_position = 730
            for veri in kilo_verileri:
                c.drawString(100, y_position, veri.replace('\t', '  ').encode("latin-1", "replace").decode("latin-1"))
                y_position -= 20

            c.save()

            QMessageBox.information(self, 'Bilgi', f'PDF dosyası oluşturuldu: {file_path}')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata Nedeni: {str(e)}')
    def createPdfIzin(self):
        try:
            file_path = os.path.join(str(self.ogrNumarasi+100), "Izin.pdf")
            folder_path = os.path.dirname(file_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            c = canvas.Canvas(file_path, pagesize=letter) # ifadesi ile bir PDF canvas'ı oluşturulur. pagesize=letter parametresi ile sayfanın boyutu belirlenir.
            c.setFont("Helvetica", 12)

            # PDF'e başlık ekle
            c.drawString(100, 750, "İzin Tablosu Raporu")

            # Verileri PDF'e ekle
            y_position = 730
            for index in range(self.izinTablo.count()): # öngüsü, bir tablonun içindeki öğeleri almak için kullanılır.
                item = self.izinTablo.item(index) #  ile tablodaki belirli bir öğe alınır.
                veri = f"{item.text()}" #  ile tablodaki belirli bir öğe alınır.
                c.drawString(100, y_position, veri.replace('\t', '  ')) # ifadesi ile PDF'e metin eklenir. replace('\t', ' ') ifadesi, metindeki sekme karakterlerini iki boşluk karakteriyle değiştirir.
                y_position -= 20 # ile bir sonraki yazının yatay konumu belirlenir ve sayfanın yukarıya doğru kaydırılmasını sağlar.

            c.save() #  ifadesi ile PDF dosyası kaydedilir.

            QMessageBox.information(self, 'Bilgi', f'PDF dosyası oluşturuldu: {file_path}')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata Nedeni: {str(e)}')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    veriTabaniAdi = "StudentDormitary/VeriTabaniArayuz.db"
    veritabani_islemleri = VeritabaniIslemleri(veriTabaniAdi)
    giris_ekrani = GirisEkrani(veritabani_islemleri) # İLK OLARAK GİRİŞ EKRANINA YÖNLENDİRİLİR BURADAN KULLANICI GİRİŞ YAPAR
    ''' İZİN EKRANINDAN BAŞARIYLA GİRİŞ YAPILIRSA ANASAYFAYA ÖĞRENCİ PANELİNE ERİŞİLİR.'''
    giris_ekrani.show()
    sys.exit(app.exec_())
