import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform
from dronekit import connect
from math import radians

class AttitudeIndicator(QWidget):
    def __init__(self, parent=None):
        super(AttitudeIndicator, self).__init__(parent)
        self.roll = 0  
        self.pitch = 0  

        current_dir = os.path.dirname(os.path.abspath(__file__))

        background_image_path = os.path.join(current_dir, "background.png")
        needle_image_path = os.path.join(current_dir, "needle.png")

        self.background_image = QPixmap(background_image_path) 
        self.needle_image = QPixmap(needle_image_path) 

    def update_attitude(self, roll, pitch):
        self.roll = roll * 80
        self.pitch = pitch * 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        size = min(self.width(), self.height())
        center = self.rect().center()

        painter.drawPixmap(center.x() - size // 2, center.y() - size // 2, size, size, self.background_image)

        pitch_offset = self.pitch * (size // 10)  
        roll_angle = self.roll  

        painter.save()
        painter.translate(center.x(), center.y() + pitch_offset)  
        transform = QTransform().rotate(-roll_angle)  
        rotated_needle = self.needle_image.transformed(transform, Qt.SmoothTransformation)

        painter.drawPixmap(-rotated_needle.width() // 2, -rotated_needle.height() // 2, rotated_needle)
        painter.restore()

class DroneControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Attitude Indicator")
        self.setGeometry(100, 100, 400, 400)

        self.attitude_indicator = AttitudeIndicator(self)

        layout = QVBoxLayout()
        layout.addWidget(self.attitude_indicator)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_attitude_data)
        self.timer.start(50)

        self.vehicle = None
        self.connect_drone()

    def connect_drone(self):
        try:
            connection_string = '172.30.16.1:14550'  
            self.vehicle = connect(connection_string, wait_ready=True)
            print("Drone connected successfully!")
        except Exception as e:
            print(f"Error connecting to drone: {e}")

    def update_attitude_data(self):
        if self.vehicle:
            roll = self.vehicle.attitude.roll
            pitch = self.vehicle.attitude.pitch
            self.attitude_indicator.update_attitude(roll, pitch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneControlWindow()
    window.show()
    sys.exit(app.exec())
