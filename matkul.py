from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as mc
from PyQt5.QtWidgets import QTableWidgetItem, QDateEdit
# from datetime import datetime

class Ui_DataView(object):
    ##KONFIGURASI DATABASE DAN TABEL
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "db_kampus" ##########UBAH$DISINI#############
    }
    TABLE_NAME = "matkul" ##########UBAH$DISINI#############
    
    ##KONFIGURASI FIELDS
    # Format: name, label, x_label, y_label, x_input, y_input
    # Vertical spacing between fields is 60 units
    FIELDS = [
        ("id", "ID", 30, 30, 150, 30), ##########UBAH$DISINI#############
        ("nama", "Nama", 30, 90, 150, 90), ##########UBAH$DISINI#############
        ("kelas", "Kelas", 30, 150, 150, 150), ##########UBAH$DISINI#############
        ("jurusan", "Jurusan", 30, 210, 150, 210), ##########UBAH$DISINI#############
        ("semester", "Semester", 30, 270, 150, 270), ##########UBAH$DISINI#############
    ]

    def setupUi(self, DataView):
        DataView.setObjectName("DataView")
        # Modified window size to be more proportional
        DataView.resize(600, 750)  # Increased width from 485 to 600
        self.centralwidget = QtWidgets.QWidget(DataView)
        self.centralwidget.setObjectName("centralwidget")
        
        # Center the window on screen
        self.center_window(DataView)
        
        # Dictionary untuk menyimpan semua input fields
        self.input_fields = {}
        
        # Setup komponen UI
        self.setup_labels_and_inputs()
        self.setup_buttons()
        self.setup_search()
        self.setup_table()
        self.setup_result_label()
        
        DataView.setCentralWidget(self.centralwidget)
        
        # Setup signals dan slots
        self.connect_signals()
        
        self.retranslateUi(DataView)
        QtCore.QMetaObject.connectSlotsByName(DataView)
        
        # Load data awal
        self.loadData()

    def center_window(self, DataView):
        """Center the window on screen"""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = DataView.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        DataView.move(x, y)

    def setup_labels_and_inputs(self):
        """Setup labels dan input fields berdasarkan FIELDS"""
        for field_name, label_text, x_label, y_label, x_input, y_input in self.FIELDS:
            # Buat label
            label = QtWidgets.QLabel(self.centralwidget)
            label.setGeometry(QtCore.QRect(x_label, y_label, 91, 21))
            font = QtGui.QFont()
            font.setPointSize(10)
            label.setFont(font)
            label.setText(label_text)
            
            # Buat input field
            line_edit = QtWidgets.QLineEdit(self.centralwidget)
            line_edit.setGeometry(QtCore.QRect(x_input, y_input, 181, 20))
            line_edit.setObjectName(f"lineEdit_{field_name}")
            
            # Jika field adalah tanggal_input, gunakan QDateEdit
            # if field_name == "tanggal_input":
            #     date_edit = QDateEdit(self.centralwidget)
            #     date_edit.setGeometry(QtCore.QRect(x_input, y_input, 181, 20))
            #     date_edit.setObjectName(f"dateEdit_{field_name}")
            #     date_edit.setCalendarPopup(True)  # Menampilkan popup kalender
            #     date_edit.setDisplayFormat("yyyy-MM-dd")  # Format sesuai MySQL
            #     # Set tanggal default ke hari ini
            #     date_edit.setDate(QtCore.QDate.currentDate())
            #     self.input_fields[field_name] = date_edit
            # else:
            #     # Untuk field lain tetap gunakan QLineEdit
            #     line_edit = QtWidgets.QLineEdit(self.centralwidget)
            #     line_edit.setGeometry(QtCore.QRect(x_input, y_input, 181, 20))
            #     line_edit.setObjectName(f"lineEdit_{field_name}")
            #     self.input_fields[field_name] = line_edit
            
            # Simpan reference ke input field
            self.input_fields[field_name] = line_edit

    def setup_buttons(self):
        """Setup tombol CRUD"""
        # Posisi Y untuk tombol (sesuaikan dengan field terakhir)
        button_y = max(field[3] for field in self.FIELDS) + 60
        
        # Buat tombol CRUD
        self.buttons = {}
        button_configs = [
            ("INSERT", 60, button_y),
            ("UPDATE", 150, button_y),
            ("DELETE", 240, button_y)
        ]
        
        for text, x, y in button_configs:
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(QtCore.QRect(x, y, 81, 31))
            button.setText(text)
            self.buttons[text] = button

    def setup_search(self):
        """Setup komponen pencarian"""
        search_y = max(field[3] for field in self.FIELDS) + 100
        
        self.searchField = QtWidgets.QLineEdit(self.centralwidget)
        self.searchField.setGeometry(QtCore.QRect(30, search_y, 161, 31))
        self.searchField.setPlaceholderText("Search...")
        
        self.buttons["SEARCH"] = QtWidgets.QPushButton(self.centralwidget)
        self.buttons["SEARCH"].setGeometry(QtCore.QRect(200, search_y, 171, 31))
        self.buttons["SEARCH"].setText("SEARCH")

    def setup_table(self):
        """Setup tabel with increased width"""
        table_y = max(field[3] for field in self.FIELDS) + 140
        
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        # Increased table width from 361 to 540
        self.tableWidget.setGeometry(QtCore.QRect(10, table_y, 540, 221))
        self.tableWidget.setColumnCount(len(self.FIELDS))
        self.tableWidget.setHorizontalHeaderLabels([field[1] for field in self.FIELDS])
        # Increased minimum column width
        for i in range(len(self.FIELDS)):
            self.tableWidget.setColumnWidth(i, 105)  # Increased from 100 to 105

    def setup_result_label(self):
        """Setup label untuk menampilkan hasil operasi"""
        label_y = max(field[3] for field in self.FIELDS) + 40
        
        self.labelResult = QtWidgets.QLabel(self.centralwidget)
        self.labelResult.setGeometry(QtCore.QRect(20, label_y, 311, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.labelResult.setFont(font)

    def connect_signals(self):
        """Hubungkan semua sinyal dengan slot"""
        self.buttons["INSERT"].clicked.connect(self.insertData)
        self.buttons["UPDATE"].clicked.connect(self.updateData)
        self.buttons["DELETE"].clicked.connect(self.deleteData)
        self.buttons["SEARCH"].clicked.connect(self.searchData)
        self.tableWidget.cellClicked.connect(self.getById)

    def get_input_values(self):
        """Ambil semua nilai dari input fields"""
        values = {}
        for name, *_ in self.FIELDS:
            if name == "tanggal_input":
                # Ambil nilai tanggal dalam format MySQL
                date_value = self.input_fields[name].date().toString("yyyy-MM-dd")
                values[name] = date_value
            else:
                values[name] = self.input_fields[name].text()
        return values

    def execute_query(self, query, values=None, fetch=False):
        """Eksekusi query database dengan error handling"""
        try:
            mydb = mc.connect(**self.DB_CONFIG)
            cursor = mydb.cursor()
            
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
                
            if fetch:
                result = cursor.fetchall()
                mydb.commit()
                return result
                
            mydb.commit()
            return True
            
        except mc.Error as e:
            self.labelResult.setText(f"Database error: {str(e)}")
            return None
            
        finally:
            if 'mydb' in locals():
                mydb.close()

    def insertData(self):
        values = self.get_input_values()
        
        if not all(values.values()):
            self.labelResult.setText("Semua field harus diisi!")
            return
            
        fields = ', '.join(values.keys())
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {self.TABLE_NAME} ({fields}) VALUES ({placeholders})"
        
        if self.execute_query(query, tuple(values.values())):
            self.labelResult.setText("Data Berhasil Disimpan")
            self.clearInputs()
            self.loadData()

    def updateData(self):
        values = self.get_input_values()
        
        if not all(values.values()):
            self.labelResult.setText("Semua field harus diisi!")
            return
            
        set_clause = ', '.join([f"{k}=%s" for k in values.keys() if k != 'id'])
        query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE id=%s"
        
        update_values = [v for k, v in values.items() if k != 'id']
        update_values.append(values['id'])
        
        if self.execute_query(query, tuple(update_values)):
            self.labelResult.setText("Data Berhasil Diupdate")
            self.clearInputs()
            self.loadData()

    def deleteData(self):
        id_value = self.input_fields["id"].text()
        
        if not id_value:
            self.labelResult.setText("Pilih data yang akan dihapus!")
            return
            
        query = f"DELETE FROM {self.TABLE_NAME} WHERE id=%s"
        
        if self.execute_query(query, (id_value,)):
            self.labelResult.setText("Data Berhasil Dihapus")
            self.clearInputs()
            self.loadData()

    def searchData(self):
        search_text = self.searchField.text()
        
        if not search_text:
            self.loadData()
            return
            
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = %s"
        values = (search_text,)
        
        result = self.execute_query(query, values, fetch=True)
        if result:
            self.populate_table(result)
        else:
            self.labelResult.setText("Data tidak ditemukan")
            self.tableWidget.setRowCount(0)

    def loadData(self):
        query = f"SELECT * FROM {self.TABLE_NAME} ORDER BY id ASC"
        result = self.execute_query(query, fetch=True)
        if result:
            self.populate_table(result)

    def populate_table(self, data):
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for column_number, value in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, 
                                      QTableWidgetItem(str(value)))

    def getById(self, row, column):
        try:
            for col, (field_name, *_) in enumerate(self.FIELDS):
                value = self.tableWidget.item(row, col).text()
                if field_name == "tanggal_input":
                    # Convert string date to QDate
                    date = QtCore.QDate.fromString(value, "yyyy-MM-dd")
                    self.input_fields[field_name].setDate(date)
                else:
                    self.input_fields[field_name].setText(value)
            self.labelResult.setText("Data dipilih")
                
        except Exception as e:
            self.labelResult.setText("Gagal memilih data")

    def clearInputs(self):
        for field_name, field in self.input_fields.items():
            if field_name == "tanggal_input":
                # Reset tanggal ke hari ini
                field.setDate(QtCore.QDate.currentDate())
            else:
                field.setText("")

    def retranslateUi(self, DataView):
        _translate = QtCore.QCoreApplication.translate
        DataView.setWindowTitle(_translate("DataView", "Data View"))
        self.labelResult.setText(_translate("DataView", "Selamat Datang"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DataView = QtWidgets.QMainWindow()
    ui = Ui_DataView()
    ui.setupUi(DataView)
    DataView.show()
    sys.exit(app.exec_())