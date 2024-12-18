#---------------------------------------
#------------Interfaz gráfica-----------
#----Daniel Bautista & Chris Villegas---
#---------------------------------------
import sys
from src.config.configurador import Configurador
from src.utils.manejador_errores import mostrar_error, mostrar_completado


import tkinter as tk
from tkinter import filedialog
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QFileDialog,
    QTextEdit, QVBoxLayout, QWidget, QLabel, QMessageBox,
    QSplitter, QListWidget
)
from PyQt6.QtCore import Qt
from src.config.configurador import Configurador
from pprint import pformat


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configurador = Configurador()
        self.gifs = []  # Lista para almacenar los GIFs
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Proyecto de Manejo de Archivos GIF")
        self.setGeometry(100, 100, 800, 400)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Etiqueta de bienvenida
        self.label = QLabel("Bienvenido al programa de lectura de metadatos en archivos GIF", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Crear un splitter para dividir la ventana
        self.splitter = QSplitter()
        layout.addWidget(self.splitter)

        # Crear contenedores para los layouts
        gif_container = QWidget()
        metadata_container = QWidget()

        # Crear layouts verticales para los contenedores
        gif_layout = QVBoxLayout(gif_container)
        self.label_gif_list = QLabel("Archivos GIF", self)
        gif_layout.addWidget(self.label_gif_list)
        self.gif_list = QListWidget()
        self.gif_list.itemClicked.connect(self.mostrar_metadatos)
        gif_layout.addWidget(self.gif_list)

        metadata_layout = QVBoxLayout(metadata_container)
        self.label_text_edit = QLabel("Metadatos", self)
        metadata_layout.addWidget(self.label_text_edit)
        self.text_edit = QTextEdit(self, readOnly=False)  # Allow editing
        metadata_layout.addWidget(self.text_edit)

        # Agregar los contenedores al splitter
        self.splitter.addWidget(gif_container)
        self.splitter.addWidget(metadata_container)

        self.save_button = QPushButton("Guardar cambios", self)
        self.save_button.clicked.connect(self.guardar_cambios)
        metadata_layout.addWidget(self.save_button)
        # Botón para seleccionar carpeta
        self.btn_select_folder = QPushButton("Seleccionar nueva carpeta", self)
        self.btn_select_folder.clicked.connect(self.seleccionar_path)
        layout.addWidget(self.btn_select_folder)

        self.showNormal()
        self.start()

    # Método que inicia el proceso de lectura
    def start(self):
        try:
            existe_archivo = self.configurador.existe_archivo()
            json_gifs = None

            if not existe_archivo:
                self.show_welcome_dialog()
            else:
                json_gifs = self.configurador.obtener_config()
                self.cargar_gifs(json_gifs)

            if json_gifs:
                self.text_edit.setPlainText(f"Metadatos obtenidos:\n{mostrar_completado(json_gifs)}")
        except Exception as e:
            self.text_edit.setPlainText(mostrar_error(f"Error inesperado: {e}"))

    def guardar_cambios(self):
        try:
            # Obtener los metadatos editados del QTextEdit
            nuevos_metadatos = self.text_edit.toPlainText()

            # Guardar los cambios en un archivo de texto
            with open("metadatos_editados.txt", "w") as f:
                f.write(nuevos_metadatos)

            QMessageBox.information(self, "Éxito", "Cambios guardados en metadatos.txt")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar los cambios: {str(e)}")
    def cargar_gifs(self, json_gifs):
        self.gif_list.clear()  # Limpiar la lista antes de cargar nuevos elementos
        for gif in json_gifs["gifs"]:
            self.gif_list.addItem(gif["nombre"])  # Asume que el nombre del GIF está en json_gifs

    def mostrar_metadatos(self, item):
        # Aquí puedes implementar la lógica para mostrar los metadatos del GIF seleccionado
        gif_nombre = item.text()
        # Buscar metadatos en la lista de GIFs
        for gif in self.configurador.obtener_config()["gifs"]:
            if gif["nombre"] == gif_nombre:
                self.text_edit.setPlainText(f"Metadatos de {gif_nombre}:\n{pformat(gif)}")
                break

    def show_welcome_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Bienvenido")
        msg_box.setText("Bienvenido al programa. No se ha encontrado un archivo de configuración.")
        msg_box.setInformativeText("Haz clic en 'Examinar' para seleccionar una carpeta con archivos GIF.")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setIcon(QMessageBox.Icon.Information)

        btn_examinar = msg_box.addButton("Examinar", QMessageBox.ButtonRole.AcceptRole)
        btn_examinar.clicked.connect(self.seleccionar_path)
        msg_box.addButton(QMessageBox.StandardButton.Cancel)
        msg_box.exec()

    def seleccionar_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selecciona una carpeta para configurar")
        if folder_path:
            json_gifs = self.configurador.configurar(folder_path)
            self.cargar_gifs(json_gifs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
