from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
import sys

class KeyboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Keyboard Input Display")
        self.setGeometry(100, 100, 400, 200)

        # Label to display the key pressed
        self.label = QLabel("Press any key", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    # Override keyPressEvent to capture keyboard inputs
    def keyPressEvent(self, event):
        key = event.text()  # Get the text of the key pressed
        if key:
            self.label.setText(f"Key pressed: {key}")
        else:
            # If key does not have a text representation (like arrow keys)
            self.label.setText(f"Key pressed: {event.key()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = KeyboardWindow()
    window.show()

    sys.exit(app.exec())
