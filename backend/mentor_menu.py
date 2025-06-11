from PyQt6 import QtWidgets, uic
import sys
import os
import io
import pandas as pd
from utils import download_excel_file

Mentor_FILE_ID = "1q1Qsaxhil_hIy19liwyOZZ45QJQeKiIu"


class MentorMeetingWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent_menu = parent
        uic.loadUi("ui/mentor_menu.ui", self)
        self.df = None  # DataFrame'i saklamak için
        self.load_table_data()
        #self.show_table(self.df)
        self.pushButton_AllApplication.clicked.connect(self.show_applications)
        self.pushButton_search.clicked.connect(self.search_applications)
        self.comboBox_secenekler.currentIndexChanged.connect(self.listComboBoxChanged)
        self.pushButton_backmenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close) 
        self.comboBox_secenekler.addItems([
            "VIT projesinin tamamına katılması uygun olur",
            "VIT projesi ilk IT eğitimi alıp ITPH a yönlendirilmesi uygun olur",
            "VIT projesi ingilizce eğitimi alıp ITPH a yönlendirilmesi uygun olur",
            "VIT projesi kapsamında direkt ITPH a yönlendirilmesi uygun olur.",
            "Direkt bireysel koçluk ile işe yönlendirilmesi uygun olur",
            "Bir sonraki VIT projesine katilmasi daha uygun olur",
            "Başka bir sektöre yönlendirilmeli",
            "Diger"
        ])
        self.comboBox_secenekler.setCurrentIndex(0)  # İlk seçeneği varsayılan olarak ayarla
        self.comboBox_secenekler.setEditable(True)  # Kullanıcıya yeni seçenek ekleme imkanı ver
        self.comboBox_secenekler.lineEdit().setPlaceholderText("Sonuç Seçiniz")  # Placeholder ekle
        self.comboBox_secenekler.lineEdit().setReadOnly(False)  # Kullanıcı yazabilir olsun
               
        
      
    def load_table_data(self):
        try:
            self.df = download_excel_file(Mentor_FILE_ID)
            if self.df is not None:
                self.show_table(self.df)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")


    def show_table(self, df):
        self.tableWidget_mentor_menu_dashboard.setRowCount(len(df))
        self.tableWidget_mentor_menu_dashboard.setColumnCount(len(df.columns))
        self.tableWidget_mentor_menu_dashboard.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                self.tableWidget_mentor_menu_dashboard.setItem(row, col, QtWidgets.QTableWidgetItem(value))


    def show_applications(self):
        try:
            self.df = download_excel_file(Mentor_FILE_ID)
            self.df.columns = self.df.columns.str.strip()  # <-- Add this line
            self.show_table(self.df[["Gorusme tarihi", 
                                 "Mentinin adi soyadi",
                                 "Mentorün adı-soyadı",
                                 "Katılımcı hakkında ne düşünüyorsunuz",
                                 "Katilimci hakkinda yorumlar"
                                 ]])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")   
    
    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()    
        
        
    def search_applications(self):
        search_text = self.lineEdit_search.text().lower()
        if search_text == "":
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen arama metni girin.")
            return
        filtered_df = self.df[self.df["Mentinin adi soyadi"].str.lower().str.contains(search_text)]
        if filtered_df.empty:
            QtWidgets.QMessageBox.information(self, "Sonuç", "Arama kriterlerine uygun başvuru bulunamadı.")
        else:
            self.show_table(filtered_df)
            
            
    def listComboBoxChanged(self):
        listed_options = ["VIT projesinin tamamına katılması uygun olur",
                          "VIT projesi ilk IT eğitimi alıp ITPH a yönlendirilmesi uygun olur",
                          "VIT projesi ingilizce eğitimi alıp ITPH a yönlendirilmesi uygun olur",
                          "VIT projesi kapsamında direkt ITPH a yönlendirilmesi uygun olur.",
                          "Direkt bireysel koçluk ile işe yönlendirilmesi uygun olur",
                          "Bir sonraki VIT projesine katilmasi daha uygun olur",
                          "Başka bir sektöre yönlendirilmeli",
                          "Diger"]
        selected_option = self.comboBox_secenekler.currentText()
        if selected_option not in listed_options:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir seçenek seçin.")
            return
        filtered_df = self.df[self.df['VIT projesinin tamamına katılması uygun olur'] == selected_option]
        
        if filtered_df.empty:
            QtWidgets.QMessageBox.information(self, "Sonuç", "Seçilen kritere uygun başvuru bulunamadı.")
        else:
            self.show_table(filtered_df)
            QtWidgets.QMessageBox.information(self, "Sonuç", f"{len(filtered_df)} başvuru bulundu.")

         
# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MentorMeetingWindow()
    window.show()
    sys.exit(app.exec())