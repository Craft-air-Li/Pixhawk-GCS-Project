import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, 
                               QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout)
from dronekit import connect, VehicleMode
import time
from pymavlink import mavutil

class DroneControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Control")
        self.setGeometry(100, 100, 400, 300)
        
        self.connection_label = QLabel("Connection Type:")
        self.connection_type = QComboBox()
        self.connection_type.addItems(["Serial", "TCP"])
        
        self.port_label = QLabel("Port/IP:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter port (Serial) or IP (TCP)")
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_drone)

        self.arm_button = QPushButton("Arm")
        self.arm_button.clicked.connect(self.arm_drone)
        self.takeoff_button = QPushButton("Takeoff (10m)")
        self.takeoff_button.clicked.connect(self.takeoff_drone)
        self.forward_button = QPushButton("Move Forward (10m)")
        self.forward_button.clicked.connect(self.move_forward)
        self.land_button = QPushButton("Land")
        self.land_button.clicked.connect(self.land_drone)
        self.disarm_button = QPushButton("Disarm")
        self.disarm_button.clicked.connect(self.disarm_drone)

        layout = QVBoxLayout()
        
        connection_layout = QHBoxLayout()
        connection_layout.addWidget(self.connection_label)
        connection_layout.addWidget(self.connection_type)
        connection_layout.addWidget(self.port_label)
        connection_layout.addWidget(self.port_input)
        connection_layout.addWidget(self.connect_button)
        
        layout.addLayout(connection_layout)
        layout.addWidget(self.arm_button)
        layout.addWidget(self.takeoff_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.land_button)
        layout.addWidget(self.disarm_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.vehicle = None  

    def connect_drone(self):
        connection_method = self.connection_type.currentText()
        port = self.port_input.text()

        try:
            if connection_method == "Serial":
                connection_string = f"com{port}"  
            elif connection_method == "TCP":
                connection_string = f"{port}:14550" 

            self.vehicle = connect(connection_string, wait_ready=True)
            print("Drone connected successfully!")

        except Exception as e:
            print(f"Error connecting to drone: {e}")

    def arm_drone(self):
        if self.vehicle:
            print("Arming drone...")
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.armed = True
            while not self.vehicle.armed:
                print("Waiting for arming...")
                time.sleep(1)
            print("Drone armed and ready.")

    def takeoff_drone(self):
        if self.vehicle:
            print("Taking off to 10 meters...")
            self.vehicle.simple_takeoff(10)

    def move_forward(self):
        if self.vehicle:
            print("Moving forward 10 meters...")
            self.send_ned_velocity(5, 0, 0, 20)  

    def land_drone(self):
        if self.vehicle:
            print("Landing the drone...")
            self.vehicle.mode = VehicleMode("LAND")

    def disarm_drone(self):
        if self.vehicle:
            print("Disarming drone...")
            self.vehicle.armed = False

    def send_ned_velocity(self, velocity_x, velocity_y, velocity_z, duration):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,       
            0, 0,    
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  
            0b0000111111000111,  
            0, 0, 0, 
            velocity_x, velocity_y, velocity_z,  
            0, 0, 0,  
            0, 0)     

        for _ in range(0, duration):
            self.vehicle.send_mavlink(msg)
            self.vehicle.flush() 
            time.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneControlWindow()
    window.show()
    sys.exit(app.exec())
