import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
from PySide6.QtCore import Qt
import time

class DroneControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Control")
        self.setGeometry(300, 300, 300, 150)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.arm_button = QPushButton("Arm Drone")
        self.disarm_button = QPushButton("Disarm Drone")
        self.takeoff_button = QPushButton("Takeoff 10m")
        self.land_button = QPushButton("Land")

        self.layout.addWidget(self.arm_button)
        self.layout.addWidget(self.disarm_button)
        self.layout.addWidget(self.takeoff_button)
        self.layout.addWidget(self.land_button)

        self.arm_button.clicked.connect(self.arm_vehicle)
        self.disarm_button.clicked.connect(self.disarm_vehicle)
        self.takeoff_button.clicked.connect(self.takeoff_vehicle)
        self.land_button.clicked.connect(self.land_vehicle)

        self.connection_string = '172.30.16.1:14550'
        self.vehicle = connect(self.connection_string, wait_ready=True)

        self.velocity_x = 0
        self.velocity_y = 0

    def arm_vehicle(self):
        print("Arming vehicle...")
        self.vehicle.mode = VehicleMode("GUIDED")
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialize...")
            time.sleep(1)
        self.vehicle.arm()
        while not self.vehicle.armed:
            print(" Waiting for vehicle to arm...")
            time.sleep(1)
        print("Vehicle armed!")

    def disarm_vehicle(self):
        print("Disarming vehicle...")
        self.vehicle.disarm()
        while self.vehicle.armed:
            print(" Waiting for vehicle to disarm...")
            time.sleep(1)
        print("Vehicle disarmed!")

    def takeoff_vehicle(self):
        altitude = 10  
        print(f"Taking off to {altitude} meters...")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.arm()
        while not self.vehicle.armed:
            print(" Waiting for vehicle to arm...")
            time.sleep(1)
        self.vehicle.simple_takeoff(altitude)
        while True:
            current_altitude = self.vehicle.location.global_relative_frame.alt
            print(f" Altitude: {current_altitude}")
            if current_altitude >= altitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def land_vehicle(self):
        print("Landing...")
        self.vehicle.mode = VehicleMode("LAND")

    def send_velocity(self, vx, vy, vz):

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0,    
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  
            0b0000111111000111,  
            0, 0, 0,  
            vx, vy, vz,  
            0, 0, 0, 
            0, 0)  
        self.vehicle.send_mavlink(msg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.velocity_x = 1  
        elif event.key() == Qt.Key_Down:
            self.velocity_x = -1  
        elif event.key() == Qt.Key_Left:
            self.velocity_y = -1  
        elif event.key() == Qt.Key_Right:
            self.velocity_y = 1  

        self.send_velocity(self.velocity_x, self.velocity_y, 0)

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Down]:
            self.velocity_x = 0  
        elif event.key() in [Qt.Key_Left, Qt.Key_Right]:
            self.velocity_y = 0  

        self.send_velocity(self.velocity_x, self.velocity_y, 0)

    def closeEvent(self, event):
        self.vehicle.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DroneControlWidget()
    widget.show()
    sys.exit(app.exec())
