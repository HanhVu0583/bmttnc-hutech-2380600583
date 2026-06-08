import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_inputs(self, text, key):
        if not text:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Input text cannot be empty.")
            msg.setWindowTitle("Validation Error")
            msg.exec_()
            return False

        if not key:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Key cannot be empty.")
            msg.setWindowTitle("Validation Error")
            msg.exec_()
            return False

        # Playfair matrix only contains letters A-Z (excluding J, mapped to I).
        # Any spaces, punctuation, or numbers will cause the coordinate lookup to fail on the server.
        # So we validate that both key and text contain only letters.
        if not key.isalpha():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Key must contain only alphabetic characters (A-Z, a-z) with no spaces or symbols.")
            msg.setWindowTitle("Validation Error")
            msg.exec_()
            return False

        # Strip any whitespace from the text for validation
        text_no_space = text.replace(" ", "")
        if not text_no_space.isalpha():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Input text must contain only letters (A-Z, a-z). Spaces, digits, and special characters are not allowed.")
            msg.setWindowTitle("Validation Error")
            msg.exec_()
            return False

        return True

    def call_api_encrypt(self):
        # We strip surrounding whitespace but keep internal to validate.
        # Actually, since spaces aren't allowed, we validate the text.
        text = self.ui.textEdit.toPlainText().strip()
        key = self.ui.lineEdit.text().strip()

        # Remove spaces automatically or prompt the user?
        # Prompting the user is safer and conforms to key constraints request.
        if not self.validate_inputs(text, key):
            return

        # Playfair usually replaces spaces with X or removes them. Let's send text without spaces.
        text_clean = text.replace(" ", "")

        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": text_clean,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.ui.textEdit_2.setPlainText(data.get("encrypted_text", ""))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.setWindowTitle("Success")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

    def call_api_decrypt(self):
        text = self.ui.textEdit_2.toPlainText().strip()
        key = self.ui.lineEdit.text().strip()

        if not self.validate_inputs(text, key):
            return

        text_clean = text.replace(" ", "")

        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": text_clean,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.ui.textEdit.setPlainText(data.get("decrypted_text", ""))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.setWindowTitle("Success")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
