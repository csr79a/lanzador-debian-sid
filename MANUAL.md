# Manual de lanzador-debian-sid

## 1. Qué hace y qué no hace

El lanzador es una ventana que muestra una lista de acciones agrupadas por
secciones. Al pulsar **Ejecutar** en una acción:

1. Se abre una terminal (Konsole; si no existe, `x-terminal-emulator`).
2. Si el proyecto no está descargado, lo clona con `git clone`. Si ya está,
   ejecuta `git pull --ff-only`.
3. Ejecuta el script con `bash`, con la salida y las preguntas en esa terminal.
4. Al terminar muestra el código de salida del script y espera a que pulses
   Enter para cerrar.

No modifica los scripts, no ejecuta nada como root por su cuenta y no guarda
registros. Se niega a arrancar si lo lanzas como root.

## 2. Instalación

### 2.1. Sistema recién instalado

```bash
# Usuario normal, pide sudo solo para instalar paquetes
sudo apt install python3-pyqt6 git
git clone https://github.com/csr79a/lanzador-debian-sid.git ~/lanzador-debian-sid
cd ~/lanzador-debian-sid
bash instalar-lanzador.sh
```

`instalar-lanzador.sh` comprueba que existan `python3-pyqt6` y `git`, y si
falta alguno te dice el `sudo apt install` que necesitas y termina. Después
crea el archivo `~/.local/share/applications/lanzador-debian-sid.desktop`.
Se puede ejecutar varias veces: solo reescribe ese archivo.

Si `konsole` no está instalado avisa, pero no bloquea: el lanzador usará
`x-terminal-emulator` si existe.

### 2.2. Abrirlo

Desde el menú de aplicaciones, buscando **Bienvenida Debian Sid**, o a mano:

```bash
python3 ~/lanzador-debian-sid/lanzador.py
```

Si el icono no aparece enseguida, cierra sesión y vuelve a entrar, o usa el
comando anterior.

## 3. Dónde se guardan los proyectos

Cada repo se clona en `~/.local/share/lanzador-debian-sid/proyectos/<nombre-del-repo>`.
Esa carpeta se define con `carpeta_proyectos` en `proyectos.json`.

Son copias propias del lanzador, distintas de tus carpetas de trabajo (por
ejemplo `~/Documentos`). Si editas un script en tu carpeta de trabajo, el
lanzador no lo verá hasta que hagas `push` a GitHub.

## 4. Cómo se actualizan los scripts

Se actualizan solos: cada pulsación hace `git pull --ff-only` antes de
ejecutar. Si subes un cambio a GitHub, la siguiente vez que pulses el botón
usa la versión nueva.

- **Sin internet:** el `pull` falla, sale el aviso *«no se pudo actualizar; se
  usa la copia local»* y se ejecuta la copia ya descargada.
- **Copia local modificada o divergente:** `--ff-only` no fusiona nada por su
  cuenta, así que el `pull` falla con el mismo aviso y se usa la copia local.
  No edites las copias del lanzador; si alguna se estropea, bórrala (ver 7.5).
- **Cambios en el propio lanzador** (`lanzador.py`, `proyectos.json`): no se
  actualizan solos. Hazlo a mano:

```bash
# Usuario normal
git -C ~/lanzador-debian-sid pull --ff-only
```

## 5. Configurar la lista: `proyectos.json`

```json
{
  "carpeta_proyectos": "~/.local/share/lanzador-debian-sid/proyectos",
  "acciones": [
    {
      "seccion": "Terminal",
      "titulo": "Configurar terminal con Starship",
      "descripcion": "Versión para Debian.",
      "repo": "https://github.com/csr79a/terminal-starship-setup.git",
      "script": "setup-terminal-starship-debian.sh",
      "peligroso": false
    }
  ]
}
```

| Campo | Obligatorio | Significado |
| --- | --- | --- |
| `carpeta_proyectos` | Sí | Carpeta donde se clonan los repos. Admite `~`. |
| `seccion` | Sí | Tarjeta en la que aparece la acción. Las acciones con el mismo nombre se agrupan. |
| `titulo` | Sí | Nombre visible de la acción. |
| `descripcion` | No | Texto gris bajo el título. |
| `repo` | Sí | URL de clonado. La carpeta local se llama como el repo, sin `.git`. |
| `script` | Sí | Ruta del script **dentro del repo**, relativa a su raíz. |
| `peligroso` | No | Si es `true`, el botón sale con borde rojo y pide confirmación. |

### Añadir un script nuevo

1. Sube el proyecto a un repo público de GitHub.
2. Añade una entrada a `acciones` con su `repo` y la ruta de `script`.
3. Guarda el archivo y vuelve a abrir el lanzador.

Si cambias el nombre o la ruta de un script dentro de un repo, actualiza el
campo `script`; mientras tanto la terminal dirá que el archivo no existe.

## 6. Notas sobre los scripts incluidos

- Todos se niegan a correr como root y piden `sudo` por dentro; por eso el
  lanzador los ejecuta como usuario normal.
- `sched-ext-debian` necesita un kernel **ya arrancado** con
  `CONFIG_SCHED_CLASS_EXT=y`, según el README de ese repo. Si no lo tienes,
  hay que compilar uno antes (`kernel-debian-builder`) y reiniciar con él.
- Las acciones de limpiar y desinstalar pueden eliminar paquetes y archivos.
  Además de la confirmación del lanzador, algunos scripts piden su propia
  confirmación (por ejemplo escribir `BORRAR`).

## 7. Solución de problemas

### 7.1. La ventana no se abre

Lánzala desde una terminal para ver el error:

```bash
python3 ~/lanzador-debian-sid/lanzador.py
```

Si dice `No module named 'PyQt6'`, instala `python3-pyqt6`.

### 7.2. «No como root»

Lo has abierto con `sudo` o como root. Ábrelo con tu usuario normal.

### 7.3. «Sin terminal»

No hay `konsole` ni `x-terminal-emulator`. Instala Konsole:

```bash
# Usuario normal, pide sudo
sudo apt install konsole
```

### 7.4. «No se pudo clonar»

Comprueba la conexión y que la URL de `repo` es correcta y el repo es
público. Los repos privados piden credenciales y el lanzador no las gestiona.

### 7.5. Una copia descargada está rota

Borra solo esa copia del lanzador; se volverá a clonar al pulsar el botón.
Cambia el nombre por el del repo afectado:

```bash
# Usuario normal. Solo borra la copia del lanzador, no tu carpeta de trabajo
rm -rf ~/.local/share/lanzador-debian-sid/proyectos/sched-ext-debian
```

### 7.6. «No existe <script> en <carpeta>»

El repo se descargó pero la ruta del campo `script` no coincide con lo que
hay en él. Revisa `proyectos.json` frente al contenido real del repo.

## 8. Desinstalación

Esto quita el lanzador y las copias descargadas de los proyectos. **No**
desinstala lo que esos scripts hayan instalado en tu sistema; para eso usa las
acciones de desinstalar o limpiar de cada sección antes de quitar el lanzador.

```bash
# Usuario normal
rm ~/.local/share/applications/lanzador-debian-sid.desktop
rm -rf ~/.local/share/lanzador-debian-sid
rm -rf ~/lanzador-debian-sid
```

## 9. Seguridad

- El lanzador ejecuta lo que haya en la rama por defecto de cada repo, con
  `sudo` dentro de los scripts. Lo que se publique en esos repos se ejecuta en
  tu sistema.
- Protege la cuenta de GitHub con verificación en dos pasos.
- Revisa los cambios de un repo antes de pulsar el botón si no los has hecho tú.
