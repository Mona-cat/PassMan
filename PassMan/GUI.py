from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt, QSize
import pyperclip
from API import APIClient
from pasman import Password

class LoginWindow(QWidget):


    def __init__(self): #__init__ wird immer von Funktionen aufgerufen wird hier genutzt um direkt Wert zu setzen

        super().__init__() # super() ist eine Funktion um auf Parentklassen zuzugreifen (hier APIClient)

        self.setWindowTitle("Password Manager")
        self.setFixedSize(400,150)
        self.Main = None

        label = QLabel("Masterpassword", self)
        self.errorlabel = QLabel("Wrong Password! Access denied!", self)
        self.errorlabel.hide()

        self.passwordline = QLineEdit(self)
        self.passwordline.setEchoMode(QLineEdit.Password)

        login = QPushButton("Login", self)
        login.clicked.connect(self.login)
        self.passwordline.returnPressed.connect(self.login)

        #Sizes
        login.setObjectName("Login")
        self.passwordline.setObjectName("passwordline")
        self.setStyleSheet(""" 
                            QLineEdit#passwordline{
                            min-width: 200px;
                            min-height: 30px;
                            max-width: 200px;
                            max-height: 30px;
                            }
                           """)

        #Position
        label.move(160, 20)
        self.passwordline.move(100, 45)
        login.move(100, 82)
        self.errorlabel.move(120, 118)


    def login(self):


        self.api = APIClient()
        response = self.api.login(self.passwordline.text())
        
        if response.status_code == 200:
            self.Main = MainWindow()
            self.Main.show()
            self.hide()
        else: 
            self.errorlabel.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.add_window = None
        self.setWindowTitle("Passwort Manager")
        self.setFixedSize(QSize(1250,800))

        self.api = APIClient()
        self.table = QTableWidget(self)

        #Size Table
        self.table.setFixedSize(824,800)
        self.table.setEnabled(False)

        #table Function
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["id", "Service", "Email",  "Password"])
        for i in range(4):
            self.table.setColumnWidth(i, 200)

        

        #Buttons
        self.all_data = QPushButton("Show Data", self)
        self.change = QPushButton("Change", self)
        self.Search = QPushButton("Search", self)
        self.New = QPushButton("New", self)
        self.Delete = QPushButton("Delete", self)
        self.Edit = QLineEdit(self)
        self.copy = QPushButton("Copy", self)
        self.copy_edit = QLineEdit(self)
        self.LineDelete = QLineEdit(self)

        #Button Function
        self.Edit.setPlaceholderText("Enter ID")
        self.copy_edit.setPlaceholderText("Enter ID")
        self.LineDelete.setPlaceholderText("Enter ID")
        self.Search.clicked.connect(self.load_account)
        self.all_data.clicked.connect(self.load_accounts)
        self.copy.clicked.connect(self.Copy_password)
        self.Delete.clicked.connect(self.delete_entry)
        self.New.clicked.connect(self.addWindow)
        self.change.clicked.connect(self.changeWindow)


        # QButtons/QEditLine Sheets
        self.Search.setObjectName("SearchButton")
        self.copy.setObjectName("copyButton")
        self.Delete.setObjectName("DeleteButton")
        self.setStyleSheet("""
                        QPushButton#DeleteButton,
                        QPushButton#copyButton,
                        QPushButton#SearchButton{
                           min-width: 100px;
                           min-height: 30px;
                           max-width: 100px;
                           max-height: 30px;
                           }""")

        #Position
        self.Edit.move(0,0)
        self.Search.move(102,0)
        self.all_data.move(0,32)
        self.change.move(0,64)     
        self.New.move(0,96)
        self.table.move(202,0)

        self.Delete.move(102,770)
        self.LineDelete.move(0,770)

        self.copy_edit.move(1026,0)
        self.copy.move(1128,0)


    def load_accounts(self):

        account = self.api.get_passwords()
        self.table.setRowCount(len(account))

        for i, data in enumerate(account):
            self.table.setItem(i, 0, QTableWidgetItem(str(data["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(data["service"]))
            self.table.setItem(i, 2, QTableWidgetItem(data["email"]))
            self.table.setItem(i, 3, QTableWidgetItem(data["password"]))
        self.table.show()

    def load_account(self):

        try:
            account_id = int(self.Edit.text().strip())
            self.Edit.clear()

            data = self.api.get_password(account_id)[0]
            self.table.setRowCount(1)

            self.table.setItem(0, 0, QTableWidgetItem(str(data["id"])))
            self.table.setItem(0, 1, QTableWidgetItem(data["service"]))
            self.table.setItem(0, 2, QTableWidgetItem(data["email"]))
            self.table.setItem(0, 3, QTableWidgetItem(data["password"]))
            self.table.show()

        except (ValueError,KeyError):
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte eine gültige ID eingeben oder der Eintrag existiert nicht!"
            )
            return


    def Copy_password(self):
            
            try:
                pw_id = int(self.copy_edit.text().strip())
                self.copy_edit.clear()
            except ValueError:
                    return
            
            data = self.api.copy_password(pw_id)
            pyperclip.copy(data["password"])
    
    def delete_entry(self):
                         
         try:
                self.eingabe = int(self.LineDelete.text())
                data = self.api.get_password(self.eingabe)
                if not data:
                     QMessageBox(
                          self,
                          f"No Entry {self.eingabe} was found"
                     )
                     return

                msg = QMessageBox(self)
                msg.setText("Do you want to delete entry permantently?")
    
                ok = msg.addButton("Delete", QMessageBox.AcceptRole)
                msg.addButton("Cancel", QMessageBox.RejectRole)
                msg.exec()

                if msg.clickedButton() == ok:
                    self.api.delete_password(self.eingabe)
                    msgdelete = QMessageBox(self)
                    msgdelete.setText("Entry is deleted")     

         except ValueError: 
                QMessageBox.warning(
                        self,
                        "Fehler",
                        f"No Entry with id: '{self.LineDelete.text()}' was Found!"
                    )
                return

    def addWindow(self):
         
         sec_window = add_Window(self)
         sec_window.exec()

    def changeWindow(self):
         window = add_Window("Change",self)
         window.exec()

    def closeEvent(self, event):
         pyperclip.copy('')
         event.accept()

#Second Window uses for add and Change
class add_Window(QDialog):

    def __init__(self, button_name, parent=None):
         super().__init__(parent)
         self.api = APIClient()
         self.setWindowTitle("Add Entry")

         self.labelemail = QLabel("Email: ", self)
         self.labelservice = QLabel("Service: ", self)
         self.labelpassword = QLabel("Password: ", self)
         self.labellength = QLabel("Password length: ", self)
         self.labelid = QLabel("Enter ID: ", self)

         self.emailline = QLineEdit(self)
         self.serviceline = QLineEdit(self)
         self.passwordline = QLineEdit(self)
         self.length = QLineEdit(self)
         self.idEdit = QLineEdit(self)

         self.password = QPushButton("Gen. Password", self)
         self.addButton = QPushButton("Add", self)
         self.changeButton = QPushButton("Change", self)

         #Stylesheet
         self.emailline.setObjectName("Emailline")
         self.serviceline.setObjectName("Serviceline")
         self.passwordline.setObjectName("Passwordline")
         self.length.setObjectName("LengthEdit")
         self.idEdit.setObjectName("IDLine")

         self.setStyleSheet("""
                            QLineEdit#Emailline,
                            QLineEdit#Serviceline,
                            QLineEdit#Passwordline{
                             min-width: 300px;
                             min-height: 30px;
                             max-width: 300px;
                             max-height: 30px;
                             font-size: 15px;
                            }
                            QLabel{
                                font-size: 15px;
                                border-radius: 5 px;
                            }
                            QLineEdit#IDLine,
                            QLineEdit#LengthEdit,
                            QPushButton{
                             min-width: 145px;
                             min-height: 30px;
                             max-width: 145px;
                             max-height: 30px;}
                            """)

         self.password.setFocusPolicy(Qt.NoFocus)
         self.addButton.setFocusPolicy(Qt.NoFocus)
         self.changeButton.setFocusPolicy(Qt.NoFocus)

         #Functions
         self.addButton.clicked.connect(self.add_account)
         self.password.clicked.connect(self.Password_Gen)
         self.length.returnPressed.connect(self.Password_Gen)
         self.idEdit.returnPressed.connect(self.load_line)
         self.changeButton.clicked.connect(self.change_account)

         #Position
         self.labelemail.move(10,5)
         self.labelservice.move(8,43)
         self.labelpassword.move(5,81)
         self.emailline.move(100,0)
         self.serviceline.move(100,38)
         self.passwordline.move(100,76)

         self.password.move(255, 112)
         self.length.move(255, 150)
         self.labellength.move(120, 155)
         self.addButton.move(100, 112)
         self.changeButton.move(100, 112)

         self.idEdit.move(255, 188)
         self.labelid.move(120,193)

         if button_name == "Change":
              self.addButton.hide()
              self.changeButton.show()
              self.idEdit.show()
              self.labelid.show()
              self.setFixedSize(510,255)
         else:
              self.addButton.show()
              self.changeButton.hide()
              self.idEdit.hide()
              self.labelid.hide()
              self.setFixedSize(510,190)

    def add_account(self):

            if (self.emailline.text() and
                 self.passwordline.text() and 
                 self.serviceline.text()):

                email_ = self.emailline.text()
                password_ = self.passwordline.text()
                service_ = self.serviceline.text()

                self.api.add_password(service_, email_, password_)
                self.close()

            else:
                QMessageBox.warning(self, "Error", "Alle Felder ausfüllen!")
                return

    def load_line(self):
            try: 
                self.id = int(self.idEdit.text().strip())
                account = self.api.get_password(self.id)[0]
                self.emailline.setText(account["email"])
                self.serviceline.setText(account["service"])
                self.passwordline.setText(account["password"])

            except KeyError:
                pass  

               
    def change_account(self):

            msg = QMessageBox(self)
            msg.setText("Are sure about changing?")
            ok = msg.addButton("Yes", QMessageBox.AcceptRole)
            msg.addButton("Cancel", QMessageBox.RejectRole)
            msg.exec()

            if msg.clickedButton() == ok:
                try:
                    email = self.emailline.text()
                    service = self.serviceline.text()
                    password = self.passwordline.text()
                    self.api.change_password(service, email, password, self.id)
                    self.close()

                except KeyError:
                     print("Wurde nicht geändert!")

    def Password_Gen(self):

        if self.length.text().strip():

            try: 
                l = int(self.length.text().strip()) 
                password = Password(1, l)
                self.passwordline.setText(f"{password}")
                self.length.clear()
            except KeyError:
                 pass
            
        else:
                password = Password(1, 16)
                self.passwordline.setText(f"{password}")
                self.length.clear()

