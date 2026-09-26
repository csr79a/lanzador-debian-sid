#!/usr/bin/env python3
"""Centro de Control Debian Sid: ventana que reúne los scripts de
configuración del sistema (PyQt6).

Cada botón abre una terminal (Konsole) que clona o actualiza el repo del
proyecto y ejecuta el script tal cual, así sudo, read y whiptail siguen
funcionando. El lanzador no toca los scripts y corre como usuario normal.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget)

CONFIG = Path(__file__).resolve().parent / "proyectos.json"

# Los colores base salen de la paleta del tema (Plasma claro u oscuro).
STYLE = """
QLabel#titulo { font-size: 26pt; font-weight: 700; }
QLabel#subtitulo { color: gray; font-size: 11pt; }
QLabel#pie { color: gray; font-size: 9pt; }
QLabel#seccion { font-size: 14pt; font-weight: 700; color: palette(highlight); }
QLabel#nombre { font-size: 12pt; font-weight: 600; }
QLabel#detalle { color: gray; font-size: 10pt; }
QFrame#tarjeta { background: palette(base); border: 1px solid palette(mid);
                 border-radius: 14px; }
QFrame#linea { background: palette(midlight); border: none; }
QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: transparent; }
QPushButton { min-width: 130px; min-height: 38px; padding: 0 18px;
              border-radius: 10px; font-size: 11pt; font-weight: 600;
              border: 2px solid transparent; }
QPushButton[peligroso="false"] { background: palette(highlight);
              color: palette(highlighted-text); }
QPushButton[peligroso="false"]:hover { border-color: palette(highlighted-text); }
QPushButton[peligroso="true"] { background: transparent; color: #d64545;
              border-color: #d64545; }
QPushButton[peligroso="true"]:hover { background: #d64545; color: white; }
"""

# Script de bash fijo: recibe DIR, URL y SCRIPT como $1, $2 y $3 (sin
# interpolar nada en el texto, para evitar problemas de quoting).
BASH_RUNNER = r'''
d=$1; url=$2; s=$3
pause() { echo; read -rp "Pulsa Enter para cerrar..." _; }
if [ -d "$d/.git" ]; then
    git -C "$d" pull --ff-only || echo "AVISO: no se pudo actualizar; se usa la copia local."
else
    mkdir -p "$(dirname "$d")" && git clone "$url" "$d" || { echo "ERROR: no se pudo clonar $url"; pause; exit 1; }
fi
[ -f "$d/$s" ] || { echo "ERROR: no existe $s en $d"; pause; exit 1; }
bash "$d/$s"; rc=$?
echo; echo "El script terminó con código $rc."
pause
'''


def find_terminal():
    for term in ("konsole", "x-terminal-emulator"):
        if shutil.which(term):
            return term
    return None


def repo_name(url):
    return url.rstrip("/").removesuffix(".git").split("/")[-1]


class Launcher(QWidget):
    def __init__(self, config):
        super().__init__()
        self.base = Path(os.path.expanduser(config["carpeta_proyectos"]))
        self.setWindowTitle("Centro de Control · Debian Sid")
        self.setMinimumSize(780, 600)
        self.resize(1000, 780)

        titulo = QLabel("Centro de Control Debian Sid")
        titulo.setObjectName("titulo")
        titulo.setWordWrap(True)
        subtitulo = QLabel("Elige qué quieres configurar. Cada botón abre una "
                           "terminal, actualiza el proyecto desde GitHub y "
                           "ejecuta su script.")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setWordWrap(True)

        contenido = QWidget()
        col = QVBoxLayout(contenido)
        col.setContentsMargins(0, 0, 8, 0)
        col.setSpacing(18)
        secciones = {}
        for item in config["acciones"]:
            secciones.setdefault(item["seccion"], []).append(item)
        for nombre, items in secciones.items():
            col.addWidget(self.build_card(nombre, items))
        col.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(contenido)

        pie = QLabel(f"Los proyectos se guardan en {self.base}")
        pie.setObjectName("pie")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 20)
        layout.setSpacing(6)
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(14)
        layout.addWidget(scroll, 1)
        layout.addSpacing(6)
        layout.addWidget(pie)

    def build_card(self, nombre, items):
        card = QFrame()
        card.setObjectName("tarjeta")
        col = QVBoxLayout(card)
        col.setContentsMargins(24, 18, 24, 18)
        col.setSpacing(14)
        cabecera = QLabel(nombre)
        cabecera.setObjectName("seccion")
        col.addWidget(cabecera)
        for i, item in enumerate(items):
            if i:
                linea = QFrame()
                linea.setObjectName("linea")
                linea.setFixedHeight(1)
                col.addWidget(linea)
            col.addLayout(self.build_row(item))
        return card

    def build_row(self, item):
        row = QHBoxLayout()
        row.setSpacing(16)
        textos = QVBoxLayout()
        textos.setSpacing(2)
        nombre = QLabel(item["titulo"])
        nombre.setObjectName("nombre")
        detalle = QLabel(item.get("descripcion", ""))
        detalle.setObjectName("detalle")
        detalle.setWordWrap(True)
        textos.addWidget(nombre)
        textos.addWidget(detalle)
        boton = QPushButton("▶  Ejecutar")
        boton.setCursor(Qt.CursorShape.PointingHandCursor)
        boton.setProperty("peligroso", "true" if item.get("peligroso") else "false")
        boton.clicked.connect(lambda _=False, it=item: self.run(it))
        row.addLayout(textos, 1)
        row.addWidget(boton, 0, Qt.AlignmentFlag.AlignVCenter)
        return row

    def run(self, item):
        if item.get("peligroso"):
            answer = QMessageBox.question(
                self, "Confirmar",
                f"«{item['titulo']}» puede eliminar paquetes y archivos.\n\n"
                "¿Abrir el script en la terminal?")
            if answer != QMessageBox.StandardButton.Yes:
                return
        terminal = find_terminal()
        if terminal is None:
            QMessageBox.critical(self, "Sin terminal",
                                 "No se encontró konsole ni x-terminal-emulator.")
            return
        dest = self.base / repo_name(item["repo"])
        subprocess.Popen(
            [terminal, "-e", "bash", "-c", BASH_RUNNER, "_",
             str(dest), item["repo"], item["script"]],
            start_new_session=True)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    if os.geteuid() == 0:
        QMessageBox.critical(None, "No como root",
                             "Ejecuta el lanzador como usuario normal; "
                             "los scripts piden sudo por sí mismos.")
        return 1
    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        window = Launcher(config)
    except (OSError, ValueError, KeyError) as err:
        QMessageBox.critical(None, "Error de configuración",
                             f"No se pudo leer {CONFIG}:\n{err}")
        return 1
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
