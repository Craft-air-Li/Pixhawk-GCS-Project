import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from dronekit import connect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from math import radians

class AttitudeIndicator(QWidget):
    def __init__(self, parent=None):
        super(AttitudeIndicator, self).__init__(parent)
        self.roll = 0  
        self.pitch = 0  

    def update_attitude(self, roll, pitch):
        self.roll = roll * 100 
        self.pitch = pitch 
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        size = min(self.width(), self.height())  
        radius = size // 2
        center = self.rect().center()

        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(center)
        painter.setBrush(QBrush(QColor(135, 206, 235))) 
        painter.drawEllipse(-radius, -radius, size, size)

        pitch_offset = self.pitch * (radius / 10) 
        roll_angle = radians(self.roll)

        painter.save()
        painter.setBrush(QBrush(QColor(160, 82, 45))) 
        painter.translate(0, pitch_offset)
        painter.rotate(-self.roll)  
        painter.drawPie(-radius, -radius, size, size, 0, 180 * 16)  
        painter.restore()


        painter.setPen(QPen(QColor(255, 69, 0), 5))
        painter.drawLine(-50, 0, 50, 0)  

        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawLine(-radius + 20, 0, radius - 20, 0)

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
