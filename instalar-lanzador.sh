#!/usr/bin/env bash
# Crea la entrada del menú de aplicaciones para el lanzador.
# Idempotente: se puede ejecutar varias veces; solo reescribe el .desktop.
set -euo pipefail

if [[ $EUID -eq 0 ]]; then
    echo "No ejecutes este script como root; usa tu usuario normal." >&2
    exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

faltan=()
python3 -c 'import PyQt6.QtWidgets' 2>/dev/null || faltan+=("python3-pyqt6")
command -v git >/dev/null 2>&1 || faltan+=("git")
if ((${#faltan[@]})); then
    echo "Faltan paquetes: ${faltan[*]}"
    echo "Instálalos con: sudo apt install ${faltan[*]}"
    exit 1
fi
command -v konsole >/dev/null 2>&1 \
    || echo "AVISO: konsole no está instalado; se usará x-terminal-emulator si existe."

APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
cat > "$APPS/lanzador-debian-sid.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Bienvenida Debian Sid
Comment=Lanzador de scripts de configuración
Exec=python3 "$DIR/lanzador.py"
Icon=utilities-terminal
Terminal=false
Categories=System;Settings;
EOF

command -v update-desktop-database >/dev/null 2>&1 \
    && update-desktop-database "$APPS" || true

echo "Listo: busca «Bienvenida Debian Sid» en el menú de aplicaciones."
