from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit, QComboBox, QFileDialog, QMainWindow, QAction, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt
import sys
import pandas as pd

class GirisPenceresi(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Soru Bankası - Ana Menü")
        self.setGeometry(150, 150, 300, 150)
        layout = QVBoxLayout()

        self.btn_yeni_soru = QPushButton("Yeni Soru Ekle")
        self.btn_yeni_soru.clicked.connect(self.parent.yeni_soru_ekle_ui)
        layout.addWidget(self.btn_yeni_soru)

        self.btn_soru_sec = QPushButton("Soru Seç ve Yazdır")
        self.btn_soru_sec.clicked.connect(self.parent.soru_sec_ui)
        layout.addWidget(self.btn_soru_sec)

        self.setLayout(layout)

class SoruBankasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soru Bankasi")
        self.setGeometry(100, 100, 1200, 600)
        self.sorular = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.giris_penceresi = GirisPenceresi(self)
        self.setCentralWidget(self.giris_penceresi)

    def geri_don(self):
        self.giris_penceresi = GirisPenceresi(self)  # yeniden oluştur
        self.setCentralWidget(self.giris_penceresi)

    def yeni_soru_ekle_ui(self):
        layout = QVBoxLayout()

        self.soru_input = QTextEdit()
        self.cevap_inputlar = [QLineEdit() for _ in range(5)]
        self.dogru_combo = QComboBox()
        self.dogru_combo.addItems(["A", "B", "C", "D", "E"])

        layout.addWidget(QLabel("SORU"))
        layout.addWidget(self.soru_input)
        for i, input_box in enumerate(self.cevap_inputlar):
            layout.addWidget(QLabel(f"{chr(65+i)}. Şık"))
            layout.addWidget(input_box)

        layout.addWidget(QLabel("Doğru Cevap"))
        layout.addWidget(self.dogru_combo)

        self.ekle_btn = QPushButton("SORU BANKASINA EKLE")
        self.ekle_btn.clicked.connect(self.soru_ekle)
        layout.addWidget(self.ekle_btn)

        # Düzenle ve Sil
        btn_layout = QHBoxLayout()
        self.duzenle_btn = QPushButton("SEÇİLİ SORUYU DÜZENLE")
        self.duzenle_btn.clicked.connect(self.soru_duzenle)
        btn_layout.addWidget(self.duzenle_btn)

        self.sil_btn = QPushButton("SEÇİLİ SORUYU SİL")
        self.sil_btn.clicked.connect(self.soru_sil)
        btn_layout.addWidget(self.sil_btn)

        self.geri_btn = QPushButton("GERİ DÖN")
        self.geri_btn.clicked.connect(self.geri_don)
        btn_layout.addWidget(self.geri_btn)

        layout.addLayout(btn_layout)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["Soru", "A", "B", "C", "D", "E", "Cevap"])
        layout.addWidget(self.tablo)

        self.kaydet_btn = QPushButton("SORU BANKASINI EXCEL OLARAK KAYDET")
        self.kaydet_btn.clicked.connect(self.excel_kaydet)
        layout.addWidget(self.kaydet_btn)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.guncelle_tablo()

    def soru_sec_ui(self):
        layout = QVBoxLayout()
        self.secim_tablo = QTableWidget()
        self.secim_tablo.setColumnCount(8)
        self.secim_tablo.setHorizontalHeaderLabels(["Seç", "Soru", "A", "B", "C", "D", "E", "Cevap"])
        layout.addWidget(self.secim_tablo)

        self.secilecek_sorulari_goster()

        sec_btn = QPushButton("EXCEL DOSYASI OLARAK KAYDET")
        sec_btn.clicked.connect(self.excel_yazdir)
        layout.addWidget(sec_btn)

        yazdir_btn = QPushButton("YAZDIR (Excel)")
        yazdir_btn.clicked.connect(self.yazdir)
        layout.addWidget(yazdir_btn)

        self.geri_btn2 = QPushButton("GERİ DÖN")
        self.geri_btn2.clicked.connect(self.geri_don)
        layout.addWidget(self.geri_btn2)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def secilecek_sorulari_goster(self):
        self.secim_tablo.setRowCount(len(self.sorular))
        for i, soru in enumerate(self.sorular):
            checkbox = QCheckBox()
            self.secim_tablo.setCellWidget(i, 0, checkbox)
            for j in range(6):
                self.secim_tablo.setItem(i, j+1, QTableWidgetItem(soru[j]))
            self.secim_tablo.setItem(i, 7, QTableWidgetItem(soru[6]))

    def yazdir(self):
        secilen_sorular = []
        for i in range(self.secim_tablo.rowCount()):
            checkbox = self.secim_tablo.cellWidget(i, 0)
            if checkbox and checkbox.isChecked():
                soru = [self.secim_tablo.item(i, j).text() for j in range(1, 7)]
                secilen_sorular.append(soru)
        if secilen_sorular:
            df = pd.DataFrame(secilen_sorular, columns=["Soru", "A", "B", "C", "D", "E"])
            df.to_excel("secilen_sorular.xlsx", index=False)
            QMessageBox.information(self, "Yazdırıldı", "Seçilen sorular yazdırıldı: secilen_sorular.xlsx")
        else:
            QMessageBox.warning(self, "Uyarı", "Yazdırmak için en az bir soru seçilmelidir.")

    def excel_yazdir(self):
        path, _ = QFileDialog.getSaveFileName(self, "Excel Kaydet", "", "Excel Files (*.xlsx)")
        if path:
            secilen_sorular = []
            for i in range(self.secim_tablo.rowCount()):
                checkbox = self.secim_tablo.cellWidget(i, 0)
                if checkbox and checkbox.isChecked():
                    soru = [self.secim_tablo.item(i, j).text() for j in range(1, 7)]
                    secilen_sorular.append(soru)
            if secilen_sorular:
                df = pd.DataFrame(secilen_sorular, columns=["Soru", "A", "B", "C", "D", "E"])
                df.to_excel(path, index=False)
                QMessageBox.information(self, "Excel Kaydedildi", f"Dosya başarıyla kaydedildi: {path}")
            else:
                QMessageBox.warning(self, "Uyarı", "Lütfen en az bir soru seçin.")

    def dosya_sec(self):
        print("Kullanıcı dosya seçti.")

    def soru_ekle(self):
        soru = self.soru_input.toPlainText()
        secenekler = [box.text() for box in self.cevap_inputlar]
        cevap = self.dogru_combo.currentText()

        if soru and all(secenekler):
            self.sorular.append([soru] + secenekler + [cevap])
            self.guncelle_tablo()
            self.soru_input.clear()
            for box in self.cevap_inputlar:
                box.clear()
        else:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")

    def soru_sil(self):
        secili = self.tablo.currentRow()
        if secili != -1:
            del self.sorular[secili]
            self.guncelle_tablo()
        else:
            QMessageBox.warning(self, "Seçim Hatası", "Lütfen silmek için bir satır seçin.")

    def soru_duzenle(self):
        secili = self.tablo.currentRow()
        if secili != -1:
            satir = self.sorular[secili]
            self.soru_input.setText(satir[0])
            for i in range(5):
                self.cevap_inputlar[i].setText(satir[i+1])
            self.dogru_combo.setCurrentText(satir[6])
            del self.sorular[secili]
            self.guncelle_tablo()
        else:
            QMessageBox.warning(self, "Seçim Hatası", "Lütfen düzenlemek için bir satır seçin.")

    def guncelle_tablo(self):
        if hasattr(self, 'tablo'):
            self.tablo.setRowCount(len(self.sorular))
            for i, soru in enumerate(self.sorular):
                for j, deger in enumerate(soru):
                    self.tablo.setItem(i, j, QTableWidgetItem(deger))

    def excel_kaydet(self):
        path, _ = QFileDialog.getSaveFileName(self, "Excel Kaydet", "", "Excel Files (*.xlsx)")
        if path:
            df = pd.DataFrame(self.sorular, columns=["Soru", "A", "B", "C", "D", "E", "Cevap"])
            df.to_excel(path, index=False)
            QMessageBox.information(self, "Kaydedildi", f"Tüm soru bankası Excel olarak kaydedildi: {path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = SoruBankasi()
    pencere.show()
    sys.exit(app.exec_())