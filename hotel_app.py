import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QDateEdit, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QDate

class HotelManagementSystem(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("نظام إدارة الفنادق - Modern HMS")
        self.setGeometry(100, 100, 1000, 600)

        # بيانات تجريبية
        self.rooms = [
            {"number": "101", "type": "Standard", "status": "Available", "price": 100},
            {"number": "102", "type": "Deluxe", "status": "Booked", "price": 150},
            {"number": "201", "type": "Suite", "status": "Available", "price": 250},
        ]
        self.guests = []
        self.bookings = []

        # إنشاء الواجهة
        self.init_ui()

    def init_ui(self):
        # إنشاء التاب (Tabs)
        tabs = QTabWidget()

        # تبويب الغرف
        rooms_tab = QWidget()
        rooms_tab_layout = QVBoxLayout()
        self.setup_rooms_tab(rooms_tab_layout)
        rooms_tab.setLayout(rooms_tab_layout)

        # تبويب الحجوزات
        bookings_tab = QWidget()
        bookings_tab_layout = QVBoxLayout()
        self.setup_bookings_tab(bookings_tab_layout)
        bookings_tab.setLayout(bookings_tab_layout)

        # تبويب العملاء
        guests_tab = QWidget()
        guests_tab_layout = QVBoxLayout()
        self.setup_guests_tab(guests_tab_layout)
        guests_tab.setLayout(guests_tab_layout)

        # إضافة التاب إلى الواجهة
        tabs.addTab(rooms_tab, "الغرف")
        tabs.addTab(bookings_tab, "الحجوزات")
        tabs.addTab(guests_tab, "العملاء")

        # إضافة التاب إلى النافذة الرئيسية
        self.setCentralWidget(tabs)

        # تصميم عصري
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

    def setup_rooms_tab(self, layout):
        # عنوان
        title = QLabel("إدارة الغرف")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # جدول عرض الغرف
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(4)
        self.rooms_table.setHorizontalHeaderLabels(["رقم الغرفة", "النوع", "الحالة", "السعر"])
        self.update_rooms_table()
        layout.addWidget(self.rooms_table)

        # زر إضافة غرفة
        add_room_btn = QPushButton("إضافة غرفة جديدة")
        add_room_btn.clicked.connect(self.add_room_dialog)
        layout.addWidget(add_room_btn)

    def setup_bookings_tab(self, layout):
        # عنوان
        title = QLabel("إدارة الحجوزات")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # جدول عرض الحجوزات
        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(5)
        self.bookings_table.setHorizontalHeaderLabels(["رقم الحجز", "اسم العميل", "رقم الغرفة", "تاريخ الوصول", "تاريخ المغادرة"])
        self.update_bookings_table()
        layout.addWidget(self.bookings_table)

        # نموذج إضافة حجز
        form_layout = QHBoxLayout()

        # اسم العميل
        self.guest_name_input = QLineEdit()
        self.guest_name_input.setPlaceholderText("اسم العميل")
        form_layout.addWidget(self.guest_name_input)

        # رقم الغرفة
        self.room_number_input = QComboBox()
        for room in self.rooms:
            if room["status"] == "Available":
                self.room_number_input.addItem(f"{room['number']} ({room['type']}) - ${room['price']}")
        form_layout.addWidget(self.room_number_input)

        # تاريخ الوصول
        self.checkin_date_input = QDateEdit()
        self.checkin_date_input.setDate(QDate.currentDate())
        self.checkin_date_input.setCalendarPopup(True)
        form_layout.addWidget(self.checkin_date_input)

        # تاريخ المغادرة
        self.checkout_date_input = QDateEdit()
        self.checkout_date_input.setDate(QDate.currentDate().addDays(1))
        self.checkout_date_input.setCalendarPopup(True)
        form_layout.addWidget(self.checkout_date_input)

        # زر إضافة حجز
        add_booking_btn = QPushButton("حجز غرفة")
        add_booking_btn.clicked.connect(self.add_booking)
        form_layout.addWidget(add_booking_btn)

        layout.addLayout(form_layout)

    def setup_guests_tab(self, layout):
        # عنوان
        title = QLabel("إدارة العملاء")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # جدول عرض العملاء
        self.guests_table = QTableWidget()
        self.guests_table.setColumnCount(4)
        self.guests_table.setHorizontalHeaderLabels(["الاسم", "رقم الهاتف", "البريد الإلكتروني", "الجنسية"])
        self.update_guests_table()
        layout.addWidget(self.guests_table)

        # زر إضافة عميل
        add_guest_btn = QPushButton("إضافة عميل جديد")
        add_guest_btn.clicked.connect(self.add_guest_dialog)
        layout.addWidget(add_guest_btn)

    def update_rooms_table(self):
        self.rooms_table.setRowCount(0)
        for room in self.rooms:
            row = self.rooms_table.rowCount()
            self.rooms_table.insertRow(row)
            self.rooms_table.setItem(row, 0, QTableWidgetItem(room["number"]))
            self.rooms_table.setItem(row, 1, QTableWidgetItem(room["type"]))
            self.rooms_table.setItem(row, 2, QTableWidgetItem(room["status"]))
            self.rooms_table.setItem(row, 3, QTableWidgetItem(f"${room['price']}"))

    def update_bookings_table(self):
        self.bookings_table.setRowCount(0)
        for booking in self.bookings:
            row = self.bookings_table.rowCount()
            self.bookings_table.insertRow(row)
            self.bookings_table.setItem(row, 0, QTableWidgetItem(str(booking["id"])))
            self.bookings_table.setItem(row, 1, QTableWidgetItem(booking["guest_name"]))
            self.bookings_table.setItem(row, 2, QTableWidgetItem(booking["room_number"]))
            self.bookings_table.setItem(row, 3, QTableWidgetItem(booking["checkin_date"].toString("yyyy-MM-dd")))
            self.bookings_table.setItem(row, 4, QTableWidgetItem(booking["checkout_date"].toString("yyyy-MM-dd")))

    def update_guests_table(self):
        self.guests_table.setRowCount(0)
        for guest in self.guests:
            row = self.guests_table.rowCount()
            self.guests_table.insertRow(row)
            self.guests_table.setItem(row, 0, QTableWidgetItem(guest["name"]))
            self.guests_table.setItem(row, 1, QTableWidgetItem(guest["phone"]))
            self.guests_table.setItem(row, 2, QTableWidgetItem(guest["email"]))
            self.guests_table.setItem(row, 3, QTableWidgetItem(guest["nationality"]))

    def add_room_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("إضافة غرفة جديدة")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout()

        # حقول الإدخال
        self.room_number_input = QLineEdit()
        self.room_number_input.setPlaceholderText("رقم الغرفة")
        layout.addWidget(self.room_number_input)

        self.room_type_input = QComboBox()
        self.room_type_input.addItems(["Standard", "Deluxe", "Suite", "Family"])
        layout.addWidget(self.room_type_input)

        self.room_price_input = QLineEdit()
        self.room_price_input.setPlaceholderText("السعر (دولار)")
        layout.addWidget(self.room_price_input)

        # زر الإضافة
        add_btn = QPushButton("إضافة الغرفة")
        add_btn.clicked.connect(lambda: self.add_room(dialog))
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.show()

    def add_room(self, dialog):
        room_number = self.room_number_input.text()
        room_type = self.room_type_input.currentText()
        room_price = self.room_price_input.text()

        if not room_number or not room_price:
            QMessageBox.warning(self, "خطأ", "يجب تعبئة جميع الحقول!")
            return

        try:
            price = float(room_price)
        except ValueError:
            QMessageBox.warning(self, "خطأ", "السعر يجب أن يكون رقمًا!")
            return

        # إضافة الغرفة
        self.rooms.append({
            "number": room_number,
            "type": room_type,
            "status": "Available",
            "price": price
        })
        self.update_rooms_table()
        dialog.close()
        QMessageBox.information(self, "نجاح", "تم إضافة الغرفة بنجاح!")

    def add_booking(self):
        guest_name = self.guest_name_input.text()
        room_number = self.room_number_input.currentText().split(" ")[0]
        checkin_date = self.checkin_date_input.date()
        checkout_date = self.checkout_date_input.date()

        if not guest_name:
            QMessageBox.warning(self, "خطأ", "يجب إدخال اسم العميل!")
            return

        if checkin_date >= checkout_date:
            QMessageBox.warning(self, "خطأ", "تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول!")
            return

        # التحقق من توافر الغرفة
        room_available = False
        for room in self.rooms:
            if room["number"] == room_number and room["status"] == "Available":
                room_available = True
                # تحديث حالة الغرفة
                room["status"] = "Booked"
                break

        if not room_available:
            QMessageBox.warning(self, "خطأ", "الغرفة غير متاحة!")
            return

        # إضافة الحجز
        booking_id = len(self.bookings) + 1
        self.bookings.append({
            "id": booking_id,
            "guest_name": guest_name,
            "room_number": room_number,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date
        })

        # إضافة العميل إذا لم يكن موجودًا
        guest_exists = any(guest["name"] == guest_name for guest in self.guests)
        if not guest_exists:
            self.guests.append({
                "name": guest_name,
                "phone": "",
                "email": "",
                "nationality": ""
            })

        # تحديث الجداول
        self.update_rooms_table()
        self.update_bookings_table()
        self.update_guests_table()

        QMessageBox.information(self, "نجاح", "تم الحجز بنجاح!")

    def add_guest_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("إضافة عميل جديد")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout()

        # حقول الإدخال
        self.guest_name_input_dialog = QLineEdit()
        self.guest_name_input_dialog.setPlaceholderText("اسم العميل")
        layout.addWidget(self.guest_name_input_dialog)

        self.guest_phone_input = QLineEdit()
        self.guest_phone_input.setPlaceholderText("رقم الهاتف")
        layout.addWidget(self.guest_phone_input)

        self.guest_email_input = QLineEdit()
        self.guest_email_input.setPlaceholderText("البريد الإلكتروني")
        layout.addWidget(self.guest_email_input)

        self.guest_nationality_input = QLineEdit()
        self.guest_nationality_input.setPlaceholderText("الجنسية")
        layout.addWidget(self.guest_nationality_input)

        # زر الإضافة
        add_btn = QPushButton("إضافة العميل")
        add_btn.clicked.connect(lambda: self.add_guest(dialog))
        layout.addWidget(add_btn)

        dialog.setLayout(layout)
        dialog.show()

    def add_guest(self, dialog):
        name = self.guest_name_input_dialog.text()
        phone = self.guest_phone_input.text()
        email = self.guest_email_input.text()
        nationality = self.guest_nationality_input.text()

        if not name:
            QMessageBox.warning(self, "خطأ", "يجب إدخال اسم العميل!")
            return

        self.guests.append({
            "name": name,
            "phone": phone,
            "email": email,
            "nationality": nationality
        })

        self.update_guests_table()
        dialog.close()
        QMessageBox.information(self, "نجاح", "تم إضافة العميل بنجاح!")

if __name__ == "__main__":   # التعديل هنا
    app = QApplication(sys.argv)
    window = HotelManagementSystem()
    window.show()
    sys.exit(app.exec())
