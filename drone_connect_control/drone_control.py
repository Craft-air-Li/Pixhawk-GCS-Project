from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from dronekit import VehicleMode

class DroneControlPanel(QWidget):
    def __init__(self, vehicle):
        super().__init__()
        self.vehicle = vehicle

        self.setFixedSize(400, 200) 

        self.status_label = QLabel("Disarmed")
        self.status_label.setFixedSize(150, 75)
        self.status_label.setFont(QFont("Extra Bold"))
        self.status_label.setStyleSheet("font-size: 20px; font-weight: 900; border: 1px solid white")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.update_status_color("Disarmed")

        self.mode_label = QLabel("Mode: Unknown")
        self.mode_label.setFixedSize(150, 75)
        self.mode_label.setFont(QFont("Extra Bold"))
        self.mode_label.setStyleSheet("font-size: 20px; font-weight: 900; border: 1px solid white")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.update_mode_color("Unknown")

        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(100)

    def setup_control_buttons(self, layout):
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.mode_label)
        layout.addLayout(status_layout)

        arm_disarm_layout = QHBoxLayout()
        self.arm_button = QPushButton("Arm")
        self.arm_button.clicked.connect(self.arm_drone)
        self.disarm_button = QPushButton("Disarm")
        self.disarm_button.clicked.connect(self.disarm_drone)
        
        arm_disarm_layout.addWidget(self.arm_button)
        arm_disarm_layout.addWidget(self.disarm_button)
        layout.addLayout(arm_disarm_layout)

        takeoff_land_layout = QHBoxLayout()
        self.takeoff_button = QPushButton("Takeoff")
        self.takeoff_button.clicked.connect(self.takeoff_drone)
        self.land_button = QPushButton("Land")
        self.land_button.clicked.connect(self.land_drone)

        takeoff_land_layout.addWidget(self.takeoff_button)
        takeoff_land_layout.addWidget(self.land_button)
        layout.addLayout(takeoff_land_layout)
        layout.addStretch() 

    def update_status(self):
        if self.vehicle:
            status = "Armed" if self.vehicle.armed else "Disarmed"
            mode = self.vehicle.mode.name if self.vehicle.mode else "Unknown"
            
            self.status_label.setText(status)
            self.update_status_color(status)
            
            self.mode_label.setText(f"{mode}")
            self.update_mode_color(mode)
        else:
            self.status_label.setText("Not Connected")
            self.update_status_color("Not Connected")
            self.mode_label.setText("Mode: N/A")
            self.update_mode_color("N/A")

    def update_status_color(self, status):
        color = "#00FF00" if status == "Armed" else "#800080" if status == "Disarmed" else "#808080"
        self.status_label.setStyleSheet(f"background-color: {color}; color: white; border-radius: 5px;")

    def update_mode_color(self, mode):
        color_map = {
            "GUIDED": "#0000FF",  
            "LAND": "#FF0000",    
            "LOITER": "#FFFF00",  
            "AUTO": "#00FFFF",    
            "Unknown": "#808080"  
        }
        color = color_map.get(mode, "#808080")
        self.mode_label.setStyleSheet(f"background-color: {color}; color: white; border-radius: 5px;")

    def arm_drone(self):
        if self.vehicle:
            self.vehicle.armed = True
            print("Drone armed.")

    def disarm_drone(self):
        if self.vehicle:
            self.vehicle.armed = False
            print("Drone disarmed.")

    def takeoff_drone(self):
        if self.vehicle:
            print("Taking off to 10 meters...")
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.simple_takeoff(10)

    def land_drone(self):
        if self.vehicle:
            print("Landing...")
            self.vehicle.mode = VehicleMode("LAND")
