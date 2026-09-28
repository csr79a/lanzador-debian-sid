# Centro de Control Debian Sid

_(repo: `lanzador-debian-sid`)_

Panel gráfico para **Debian Sid** que reúne mis scripts de configuración en
una sola ventana. Cada botón descarga o actualiza el proyecto desde GitHub y
ejecuta su script tal cual, sin modificarlo, **dentro de la propia ventana**.

- Ventana hecha con **PyQt6**, con los colores de tu tema de Plasma (claro u oscuro).
- El progreso, las preguntas, los avisos y la contraseña de `sudo` aparecen en
  la misma ventana: no se abre ninguna terminal aparte.
- Los cuadros `whiptail` de tipo sí/no y aviso se convierten en preguntas de
  texto; los scripts con menús o listas se abren en **Konsole**.
- Las aplicaciones con ventana propia (como AutoFirma) se abren sin terminal.
- El lanzador corre como **usuario normal** y no necesita `sudo` por sí mismo.
- En una instalación limpia solo hace falta este repo: el resto de proyectos
  se descargan al pulsar cada botón.

## Requisitos

- Debian Sid (o derivado basado en APT).
- Los paquetes `python3-pyqt6` y `git`, ambos en los repositorios oficiales.
- `sudo` configurado para tu usuario, porque los scripts lo usan por dentro.
- `konsole` (KDE Plasma): opcional. Solo hace falta si algún script usa menús o
  listas, o si una acción lleva `"modo": "terminal"`. Si no está, usa
  `x-terminal-emulator`.

## Uso rápido

```bash
sudo apt install python3-pyqt6 git
git clone https://github.com/csr79a/lanzador-debian-sid.git ~/lanzador-debian-sid
cd ~/lanzador-debian-sid
bash instalar-lanzador.sh
```

Después busca **Centro de Control Debian Sid** en el menú de aplicaciones.
También puedes abrirlo directamente:

```bash
python3 ~/lanzador-debian-sid/lanzador.py
```

## Proyectos incluidos

| Sección | Repo | Acciones |
| --- | --- | --- |
| Base | `debian-sid-setup` | Convertir Testing a Sid / Configurar / Limpiar Debian Sid |
| Gaming | `setup-gaming-debian-sid` | Instalar / Limpiar gaming |
| Rendimiento | `sched-ext-debian` | Instalar sched-ext / Instalar gestor de sched-ext (GUI) / Desinstalar sched-ext |
| Gráficos NVIDIA | `nvidia-debian-setup` | Instalar driver NVIDIA |
| Hardware ASUS | `asusctl-rogcontrol-debian` | Instalar / Desinstalar asusctl y ROG Control |
| Terminal | `terminal-starship-setup` | Configurar terminal con Starship (versión Debian) |
| Firma electrónica | `autofirma-debian` | Instalar AutoFirma |

Las acciones que eliminan cosas (limpiar y desinstalar) piden una confirmación
extra antes de ejecutar el script.

## Contenido de este repo

- `lanzador.py` — la ventana y la lógica de ejecución.
- `proyectos.json` — la lista de proyectos, repos y scripts que muestra la ventana.
- `instalar-lanzador.sh` — crea la entrada en el menú de aplicaciones.
- [`MANUAL.md`](MANUAL.md) — funcionamiento detallado, modos de ejecución, cómo añadir scripts y solución de problemas.

## Seguridad

Cada clic ejecuta, con `sudo` dentro de los scripts, lo que haya en la rama
por defecto del repo correspondiente. Conviene proteger la cuenta de GitHub
con verificación en dos pasos.
