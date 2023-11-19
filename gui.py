from __future__ import annotations
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from image_traitement import subtract_images, linear_gradient_generation
import threading


class ImageSelectorApp(QWidget):
    def __init__(self: ImageSelectorApp):
        super().__init__()

        self.image_path: str = ""
        self.gradient_path: str = ""

        self.setWindowTitle("SAE image")
        self.setGeometry(100, 100, 400, 200)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.image_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout: QHBoxLayout = QHBoxLayout()

        self.image: QLabel = QLabel()
        self.gradient: QLabel = QLabel()

        self.image_layout.addWidget(self.image)
        self.image_layout.addWidget(self.gradient)

        self.button1: QPushButton = QPushButton("Sélectionner une image")
        self.button2: QPushButton = QPushButton("Sélectionner un gradient")
        self.button3: QPushButton = QPushButton("Appliquer la soustration")
        self.button4: QPushButton = QPushButton("Générer un gradient linéaire")

        self.button1.clicked.connect(self.select_image)
        self.button2.clicked.connect(self.select_gradient)
        self.button3.clicked.connect(self.substraction_apply)
        self.button4.clicked.connect(self.generate_gradient)

        self.buttons_layout.addWidget(self.button1)
        self.buttons_layout.addWidget(self.button2)
        self.buttons_layout.addWidget(self.button4)
        self.buttons_layout.addWidget(self.button3)

        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

    def select_image(self: ImageSelectorApp):
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if image_path:
            pixmap: QPixmap = QPixmap(image_path)
            self.image.setPixmap(pixmap.scaledToWidth(200))
            self.image_path = image_path

    def select_gradient(self: ImageSelectorApp):
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un gradient", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if image_path:
            pixmap: QPixmap = QPixmap(image_path)
            self.gradient.setPixmap(pixmap.scaledToWidth(200))
            self.gradient_path = image_path

    def generate_gradient(self: ImageSelectorApp):
        try:
            thread = threading.Thread(
                target=linear_gradient_generation(self.image_path)
            )
            thread.start()

            succes_popup = QMessageBox()
            succes_popup.setIcon(QMessageBox.Icon.Information)
            succes_popup.setWindowTitle("Succés")
            succes_popup.setText("Opération effectués")
            succes_popup.exec()

        except Exception:
            error_popup = QMessageBox()
            error_popup.setIcon(QMessageBox.Icon.Critical)
            error_popup.setWindowTitle("Erreur")
            error_popup.setText("Merci de selectionner une image")
            error_popup.exec()

    def substraction_apply(self: ImageSelectorApp):
        try:
            thread = threading.Thread(
                target=subtract_images(self.image_path, self.gradient_path)
            )
            thread.start()

            succes_popup = QMessageBox()
            succes_popup.setIcon(QMessageBox.Icon.Information)
            succes_popup.setWindowTitle("Succés")
            succes_popup.setText("Opération effectués")
            succes_popup.exec()

        except Exception:
            error_popup = QMessageBox()
            error_popup.setIcon(QMessageBox.Icon.Critical)
            error_popup.setWindowTitle("Erreur")
            error_popup.setText(
                "Merci de selectionner une image et son gradient correspondant"
            )
            error_popup.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSelectorApp()
    window.show()
    sys.exit(app.exec())
