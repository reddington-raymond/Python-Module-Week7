import sys
import os
import io
import pandas as pd
from PyQt6 import QtWidgets, uic
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from preference_menu import PreferenceMenuWindow
from admin_preference_menu import AdminPreferenceMenuWindow
from utils import download_excel_file


KULLANICILAR_FILE_ID = "1tlQ9SVhEwwlmWCHKpRnXYfeTpFYltbt_"


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.pushButton_login.clicked.connect(self.handle_login)  # Giriş butonu
        self.pushButton_exit.clicked.connect(QtWidgets.QApplication.quit)  # Exit butonu
        self.label_status.setText("")  # Uyarı etiketi

    def handle_login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        try:
            df = download_excel_file(KULLANICILAR_FILE_ID)
            df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
            user = df[(df['username'] == username) & (df['password'] == password)]
            if not user.empty:
                rol = user.iloc[0]['rol']
                self.label_status.setText("Giriş başarılı!")
                if rol == "admin":
                    self.open_admin_menu()
                elif rol == "user":
                    self.open_user_menu()
                else:
                    self.label_status.setText("Rol tanımsız!")
            else:
                self.label_status.setText("Kullanıcı adı veya şifre yanlış!")
        except Exception as e:
            self.label_status.setText(f"Hata: {e}")

    def open_admin_menu(self):
        self.admin_menu = AdminPreferenceMenuWindow()
        self.admin_menu.show()
        self.close()

    def open_user_menu(self):
        self.user_menu = PreferenceMenuWindow()
        self.user_menu.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
    
    
