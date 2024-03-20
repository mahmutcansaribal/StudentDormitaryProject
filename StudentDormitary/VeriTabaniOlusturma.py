import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('StudentDormitary/Dormitary.db')

# Bir cursor nesnesi oluştur
cursor = conn.cursor()

# Ogrenci tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ogrenci (
    Ogr_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ogr_Adi TEXT NOT NULL,
    Sifre TEXT NOT NULL,
    fotograf BLOB,
    bolum TEXT NOT NULL
)
''')

# IzinTablosu tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS IzinTablosu (
    izin_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    KalanIzin INTEGER NOT NULL DEFAULT 45,
    BaslangicTarihi TEXT,
    Ogr_ID INTEGER,
    BitisTarih TEXT,
    AlinanIzin INTEGER,
    FOREIGN KEY(Ogr_ID) REFERENCES Ogrenci(Ogr_ID)
)
''')

# VucutKitle tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS VucutKitle (
    Vki_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    boy FLOAT NOT NULL,
    Kilo FLOAT NOT NULL,
    Cinsiyet TEXT NOT NULL,
    Yas INTEGER NOT NULL,
    Ogr_ID INTEGER,
    Tarih TEXT,
    IdealKilo REAL,
    Durum TEXT,
    OgrenciAd TEXT,
    Fark REAL,
    Vki REAL,
    FOREIGN KEY(Ogr_ID) REFERENCES Ogrenci(Ogr_ID)
)
''')

# YurtDuyurulari tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS YurtDuyurulari (
    Duyuru_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Duyuru TEXT
)
''')

# SabahYemegi tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS SabahYemegi (
    Sabahid INTEGER PRIMARY KEY AUTOINCREMENT,
    KahvaltiAdi TEXT,
    Yaninda TEXT,
    Ekstra TEXT
)
''')

# AksamYemegi tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS AksamYemegi (
    Aksamid INTEGER PRIMARY KEY AUTOINCREMENT,
    Yemek TEXT,
    Yaninda TEXT,
    Ekstra TEXT
)
''')

# ArizaTaleb tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS ArizaTaleb (
    ariza_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    arizaYorum TEXT NOT NULL,
    Ogr_ID INTEGER,
    FOREIGN KEY(Ogr_ID) REFERENCES Ogrenci(Ogr_ID)
)
''')

# Veritabanı değişikliklerini kaydet
conn.commit()

# Bağlantıyı kapat
conn.close()
