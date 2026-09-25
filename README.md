# lanzador-debian-sid

Pantalla de bienvenida gráfica para **Debian Sid** que reúne mis scripts de
configuración en una sola ventana. Cada botón abre una terminal, descarga o
actualiza el proyecto desde GitHub y ejecuta su script tal cual, sin
modificarlo.

- Ventana hecha con **PyQt6**, con los colores de tu tema de Plasma (claro u oscuro).
- Los scripts se ejecutan en **Konsole**, así que `sudo`, `read` y `whiptail`
  funcionan igual que si los lanzaras a mano.
- El lanzador corre como **usuario normal** y no necesita `sudo` por sí mismo.
- En una instalación limpia solo hace falta este repo: el resto de proyectos
  se descargan al pulsar cada botón.

## Requisitos

- Debian Sid (o derivado basado en APT).
- Los paquetes `python3-pyqt6` y `git`, ambos en los repositorios oficiales.
- `konsole` (KDE Plasma). Si no está, usa `x-terminal-emulator`.
- `sudo` configurado para tu usuario, porque los scripts lo usan por dentro.

## Uso rápido

```bash
sudo apt install python3-pyqt6 git
git clone https://github.com/csr79a/lanzador-debian-sid.git ~/lanzador-debian-sid
cd ~/lanzador-debian-sid
bash instalar-lanzador.sh
```

Después busca **Bienvenida Debian Sid** en el menú de aplicaciones. También
puedes abrirlo directamente:

```bash
python3 ~/lanzador-debian-sid/lanzador.py
```

## Proyectos incluidos

| Sección | Repo | Acciones |
| --- | --- | --- |
| Base | `debian-sid-setup` | Configurar / Limpiar Debian Sid |
| Gaming | `setup-gaming-debian-sid` | Instalar / Limpiar gaming |
| Rendimiento | `sched-ext-debian` | Instalar / Desinstalar sched-ext |
| Hardware ASUS | `asusctl-rogcontrol-debian` | Instalar / Desinstalar asusctl y ROG Control |
| Terminal | `terminal-starship-setup` | Configurar terminal con Starship (versión Debian) |

Las acciones que eliminan cosas (limpiar y desinstalar) piden una confirmación
extra antes de abrir el script.

## Contenido de este repo

- `lanzador.py` — la ventana y la lógica de ejecución.
- `proyectos.json` — la lista de proyectos, repos y scripts que muestra la ventana.
- `instalar-lanzador.sh` — crea la entrada en el menú de aplicaciones.
- [`MANUAL.md`](MANUAL.md) — funcionamiento detallado, cómo añadir scripts y solución de problemas.

## Seguridad

Cada clic ejecuta, con `sudo` dentro de los scripts, lo que haya en la rama
por defecto del repo correspondiente. Conviene proteger la cuenta de GitHub
con verificación en dos pasos.
