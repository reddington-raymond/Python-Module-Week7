from PyQt6 import QtWidgets, uic
import sys
import os
import io
import pandas as pd
from utils import download_excel_file

Basvurular_FILE_ID = "1mEAsoYddFYarFmu3INHhrNwuwCrCQD74"
VIT1_FILE_ID = "1KuAOSCmLwQigrCgJETuJEYm7_3VbOpSQ"
VIT2_FILE_ID = "1Ka5HkkadYXZZsrwCO92Vl_iyFk8xrOqc"

class ApplicationsWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent_menu = parent
        uic.loadUi("ui/applications_menu.ui", self)
        self.df = None  # DataFrame'i saklamak için
        self.load_table_data()
        #self.show_table(self.df)
        self.lineEdit_search.textChanged.connect(self.filter_table)  
        self.pushButton_all_applications.clicked.connect(self.show_applications)
        self.pushButton_planned_mentor_meetings.clicked.connect(self.planned_mentor_meetings)
        self.pushButton_unscheduled_mentor_meetings.clicked.connect(self.unscheduled_mentor_meetings)
        self.pushButton_pre_vit_control.clicked.connect(self.previous_VIT_control)
        self.pushButton_repeted_registeration.clicked.connect(self.repeated_registration)
        self.pushButton_dif_registeration.clicked.connect(self.different_registration)
        self.pushButton_filter_application.clicked.connect(self.filter_applications)
        self.pushButton_BackMenu.clicked.connect(self.back_to_menu)
        self.pushButton_exit.clicked.connect(self.close)    
        
              
                   
    def load_table_data(self):
        try:
            self.df = download_excel_file(Basvurular_FILE_ID)
            if self.df is not None:
                self.show_table(self.df)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")


    def show_table(self, df):
        self.tableWidget_application_dashboard.setRowCount(len(df))
        self.tableWidget_application_dashboard.setColumnCount(len(df.columns))
        self.tableWidget_application_dashboard.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                self.tableWidget_application_dashboard.setItem(row, col, QtWidgets.QTableWidgetItem(value))


    def show_applications(self):
        try:
            self.df = download_excel_file(Basvurular_FILE_ID)
            self.show_table(self.df[["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")
            
            
    
    def filter_table(self):
        if self.df is None:
            return
        search_text = self.lineEdit_search.text().lower()
        if search_text == "":
            filtered_df = self.df[["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]]
        else:
            # 'Adınız Soyadınız' sütununda arama yap
            filtered_df = self.df[self.df['Adınız Soyadınız'].str.lower().str.contains(search_text)][["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]]
            self.show_table(filtered_df)
        
    # Show all applications in the table
    def show_applications(self):
        try:
            self.df = download_excel_file(Basvurular_FILE_ID)
            search_text = self.lineEdit_search.text().lower() if hasattr(self, 'lineEdit_search') else ""
            filtered_df = self.df[self.df['Adınız Soyadınız'].str.lower().str.contains(search_text)][["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]]
            self.show_table(filtered_df)
        except Exception as e:
            print(f"Error downloading or processing file: {e}")
            return pd.DataFrame(columns=["Error"], data=[[str(e)]])
    
    def planned_mentor_meetings(self):
        self.df = download_excel_file(Basvurular_FILE_ID)
        self.df.columns = self.df.columns.str.strip()
        # Select only the desired columns after filtering
        filtered =self.df[self.df["Mentor gorusmesi"] == "OK"][["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]]
        self.show_table(filtered)


    def unscheduled_mentor_meetings(self):
        self.df = download_excel_file(Basvurular_FILE_ID)
        # Remove possible leading/trailing spaces in column names
        self.df.columns = self.df.columns.str.strip()
        # Filter rows where 'Mentor gorusmesi' is not 'OK'
        filtered = self.df[self.df["Mentor gorusmesi"] != "OK"][["Zaman damgası", "Adınız Soyadınız",
                                                   "Mail adresiniz","Telefon Numaranız",
                                                   "Posta Kodunuz","Yaşadığınız Eyalet",
                                                   "Ekonomik Durumunuz"]]
        self.show_table(filtered)



    def previous_VIT_control(self):
        vit1_df = download_excel_file(VIT1_FILE_ID)
        vit2_df = download_excel_file(VIT2_FILE_ID)
        vit1_df.columns = vit1_df.columns.str.strip()
        vit2_df.columns = vit2_df.columns.str.strip()
        self.df.columns = self.df.columns.str.strip()

    # First merge vit1 and vit2
        merged_df = pd.merge(vit1_df, vit2_df, on=["Adınız Soyadınız", "Mail adresiniz"], how="inner", suffixes=('_VIT1', '_VIT2'))
    # Then merge with self.df
        merged_df = pd.merge(merged_df, self.df, on=["Adınız Soyadınız", "Mail adresiniz"], how="inner")

    # Select only the desired columns after merging
        filtered = merged_df[["Zaman damgası_VIT1", "Adınız Soyadınız",
                          "Mail adresiniz", "Telefon Numaranız",
                          "Posta Kodunuz", "Yaşadığınız Eyalet",
                          "Ekonomik Durumunuz"]]
        self.show_table(filtered)



    def repeated_registration(self):
        self.df = download_excel_file(Basvurular_FILE_ID)
        self.df.columns = self.df.columns.str.strip()
        # same name and email
        filtered = self.df[self.df.duplicated(subset=["Adınız Soyadınız", "Mail adresiniz"], keep=False)]
        filtered = filtered[["Zaman damgası", "Adınız Soyadınız",
                         "Mail adresiniz","Telefon Numaranız",
                         "Posta Kodunuz","Yaşadığınız Eyalet",
                         "Ekonomik Durumunuz"]]
        self.show_table(filtered)

    def different_registration(self):
        #Farklı Kayıt Butonu tıklandığında Driveda kayıtlı olan VIT1 ve VIT2 
        # de ortak olmayan adaylar ekrana getirilmeli
        vit1_df = download_excel_file(VIT1_FILE_ID)
        vit2_df = download_excel_file(VIT2_FILE_ID)
        vit1_df.columns = vit1_df.columns.str.strip()
        vit2_df.columns = vit2_df.columns.str.strip()
        self.df.columns = self.df.columns.str.strip()
       
        merged_df = pd.merge(vit1_df, vit2_df, on=["Adınız Soyadınız", "Mail adresiniz"], how="outer", suffixes=('_VIT1', '_VIT2'))

        filtered = self.df[~self.df.set_index(["Adınız Soyadınız", "Mail adresiniz"]).index.isin(merged_df.set_index(["Adınız Soyadınız", "Mail adresiniz"]).index)]
        filtered = filtered[["Zaman damgası", "Adınız Soyadınız",
                            "Mail adresiniz","Telefon Numaranız",
                            "Posta Kodunuz","Yaşadığınız Eyalet",
                            "Ekonomik Durumunuz"]]
        self.show_table(filtered)
        
        
    def filter_applications(self):
        self.df = download_excel_file(Basvurular_FILE_ID)
        self.df.columns = self.df.columns.str.strip()

        filtered = self.df.drop_duplicates(subset=["Adınız Soyadınız", "Mail adresiniz"])
        filtered = filtered[["Zaman damgası", "Adınız Soyadınız",
                         "Mail adresiniz","Telefon Numaranız",
                         "Posta Kodunuz","Yaşadığınız Eyalet",
                         "Ekonomik Durumunuz"]]
        self.show_table(filtered)

    def back_to_menu(self):
        if self.parent_menu is not None:
            self.parent_menu.show()
        self.close()

    
# Test amaçlı çalıştırmak için:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationsWindow()
    window.show()
    sys.exit(app.exec())