import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pystray
from PIL import Image
import threading
import webbrowser

class CrosshairWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)

        self.image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors", "green.png")
        self.update_crosshair(self.image_path)

        self.show()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        widget_geometry = self.geometry()
        x = (screen_geometry.width() - widget_geometry.width()) // 2
        y = (screen_geometry.height() - widget_geometry.height()) // 2
        self.move(x, y)

    def update_crosshair(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load crosshair: {image_path}")
            return
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.center()

def quit_app(icon, item):
    icon.stop()
    QApplication.quit()

def open_github(icon, item):
    webbrowser.open("https://github.com/CoderYello/Lightweight-Crosshair")

def change_crosshair(crosshair_widget, image_name):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors", image_name)
    crosshair_widget.update_crosshair(image_path)

def create_system_tray_icon(crosshair_widget):
    colors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors")
    alternative_crosshairs = ["green.png", "red.png", "blue.png", "pink.png", "black.png", "white.png"]

    menu_items = {}

    def create_menu_item(image_name):
        return pystray.MenuItem(
            image_name.capitalize().split('.')[0],
            lambda icon, item: change_crosshair(crosshair_widget, image_name),
        )

    for crosshair in alternative_crosshairs:
        menu_items[crosshair] = create_menu_item(crosshair)

    image_path = os.path.join(colors_path, "green.png")
    image = Image.open(image_path)

    colors_menu = pystray.Menu(
        *menu_items.values()
    )

    icon = pystray.Icon("crosshair", image, "Lightweight Crosshair", menu=pystray.Menu(
        pystray.MenuItem("🎨 Colors", colors_menu),
        pystray.MenuItem("🐱 GitHub", open_github),
        pystray.MenuItem("✖️ Quit", quit_app)
    ))
    icon.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    crosshair_widget = CrosshairWidget()

    tray_thread = threading.Thread(target=create_system_tray_icon, args=(crosshair_widget,))
    tray_thread.setDaemon(True)
    tray_thread.start()

    sys.exit(app.exec_())