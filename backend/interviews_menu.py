from PyQt6 import QtWidgets, uic
import pandas as pd
import sys
import os
from utils import download_excel_file

MULAKATLAR_FILE_ID = "1Mh9FnLlZ__mBE2qZlGKfqbrIWr351uTa"

class InterviewsMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_menu = parent  # Ebeveyn menüyü sakla
        uic.loadUi("ui/interviews_menu.ui", self)
        self.df = None  # DataFrame'i saklamak için
        self.load_table_data()
        self.lineEdit_search.textChanged.connect(self.filter_table)  # Arama kutusuna bağla
        self.pushButton_all_submitted_projects.clicked.connect(self.show_all_submitted_projects)
        self.pushButton_project_arrivals.clicked.connect(self.show_project_arrivals)
        self.pushButton_BackMenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close)
        
    def load_table_data(self):
        try:
            self.df = download_excel_file(MULAKATLAR_FILE_ID)
            self.show_table(self.df)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")

    def show_table(self, df):
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def filter_table(self):
        if self.df is None:
            return
        search_text = self.lineEdit_search.text().lower()
        if search_text == "":
            filtered_df = self.df
        else:
            # 'Name Surname' sütununda arama yap
            filtered_df = self.df[self.df['Name Surname'].str.lower().str.contains(search_text)]
        self.show_table(filtered_df)
    
    def show_all_submitted_projects(self):
        if self.df is None:
            return
        # 'Project Sending Date' sütununda boş olmayanları filtrele
        filtered_df = self.df[self.df['Project Sending Date'].notna() & (self.df['Project Sending Date'] != "")]
        self.show_table(filtered_df)

    def show_project_arrivals(self):
        if self.df is None:
            return
        # 'Project Arrival Date' sütununda boş olmayanları filtrele
        filtered_df = self.df[self.df['Project Arrival Date'].notna() & (self.df['Project Arrival Date'] != "")]
        self.show_table(filtered_df)

    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterviewsMenuWindow()
    window.show()
    sys.exit(app.exec())