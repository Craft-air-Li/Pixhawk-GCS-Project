import sys
import folium
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from dronekit import connect, VehicleMode
import time

class DroneMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Map")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create QWebEngineView to display the map
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)

        # Connect to the drone
        self.connection_string = '127.0.0.1:14550'
        self.vehicle = connect(self.connection_string, wait_ready=True)

        # Generate and display the map
        self.update_map()

    def update_map(self):
        # Get drone location
        location = self.vehicle.location.global_frame
        lat = location.lat
        lon = location.lon
        print(f"Drone Location: Lat={lat}, Lon={lon}")

        # Create map centered on drone location
        map_center = [lat, lon]
        drone_map = folium.Map(location=map_center, zoom_start=15)

        # Add marker for drone location
        folium.Marker(
            location=map_center,
            popup='Drone Location',
            icon=folium.Icon(color='blue')
        ).add_to(drone_map)

        # Save map to HTML file
        map_html = 'drone_map.html'
        drone_map.save(map_html)

        # Load the HTML map into QWebEngineView
        self.map_view.setUrl(f"file://{map_html}")

    def closeEvent(self, event):
        # Clean up and close the connection to the drone
        self.vehicle.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneMapApp()
    window.show()
    sys.exit(app.exec())
