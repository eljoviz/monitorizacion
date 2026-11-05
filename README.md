<div align="center">

<img src="img/banner.svg" alt="Monitorización en Linux" width="100%">

<p align="center">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash" />
  <img src="https://img.shields.io/badge/SysAdmin-ASIR-0ea5e9?style=for-the-badge" alt="ASIR" />
  <img src="https://img.shields.io/badge/DevOps-Monitoring-8b5cf6?style=for-the-badge" alt="DevOps" />
  <img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>Manual práctico de diagnóstico, métricas de rendimiento y monitorización de sistemas Linux.</b><br>
  Organizado por módulos temáticos con análisis paso a paso de capturas reales.
</p>

</div>

---

## 📑 Índice General

| Módulo | Documento | Descripción y Contenidos Clave |
| :--- | :---: | :--- |
| **1. Procesos y Rendimiento de CPU** | [**`1.md`**](1.md) | Ciclo de vida y estados (`R`, `S`, `D`, `T`, `Z`), comandos `ps` (`a`, `au`, `aux`, `-C`, `-u`), monitorización en tiempo real con `top` y `htop`, control de señales (`kill`, `pkill`) y caso práctico de los 10 procesos que más CPU consumen en 3 periodos consecutivos. |
| **2. Memoria, Espacio y Rendimiento del Disco** | [**`2.md`**](2.md) | Jerarquía de memoria RAM, Buffers, Caché y Swap (`free`, `vmstat`). Espacio en sistemas de archivos (`df -hT`, `du`, `ncdu`) y diagnóstico de cuellos de botella de entrada/salida y saturación de disco (*I/O wait* con `iostat -xz` e `iotop`). |
| **3. Tráfico y Diagnóstico de Red** | [**`3.md`**](3.md) | Interfaces físicas y estadísticas de enlace (`ip link`, `ethtool`), sockets y puertos en escucha (`ss -tulpn`, `lsof -i`), consumo de ancho de banda en tiempo real (`iftop`, `nload`) y captura e inspección de paquetes (`tcpdump`, `ping`, `mtr`). |

---

## 🛠️ Herramientas y Scripts Incluidos

### 📊 Dashboard de Monitorización Automatizada
En la carpeta [`scripts/`](scripts/) se incluye el script interactivo [`monitor_sistema.sh`](scripts/monitor_sistema.sh) para obtener un informe instantáneo del estado del sistema con alertas de umbral en color:

<div align="center">
  <img src="img/terminal_script.svg" alt="Ejecución de monitor_sistema.sh" width="95%">
</div>

```bash
# Dar permisos y ejecutar el chequeo rápido
chmod +x scripts/monitor_sistema.sh
./scripts/monitor_sistema.sh
```

---

## ⚡ Guía Rápida de Diagnóstico (Cheat Sheet)

| Síntoma / Problema | Comando Recomendado | Parámetros Clave | Qué buscar | Módulo |
| :--- | :--- | :--- | :--- | :---: |
| **Servidor lento / colapso de CPU** | `top` / `htop` | `load average`, `%CPU` | Carga superior al número de núcleos (`nproc`) o tareas en 100% CPU. | [1.md](1.md) |
| **Proceso descontrolado** | `ps aux --sort=-%cpu` | `PID`, `STAT` | Localizar el PID y enviar `kill -15` (cierre limpio) o `kill -9`. | [1.md](1.md) |
| **Falta de memoria / Aplicaciones se cierran** | `free -h` / `dmesg -T` | `available`, `oom-killer` | Memoria disponible cercana a 0 y uso continuo de Swap (*thrashing*). | [2.md](2.md) |
| **Disco lleno (No space left on device)** | `df -hT` | `%Uso`, `Inodos` (`df -i`) | Particiones al 100% de ocupación o agotamiento de inodos. | [2.md](2.md) |
| **Carpetas gigantes ocupando espacio** | `du -h --max-depth=1` | `/var`, `/home` | Localizar logs descontrolados o ficheros temporales huérfanos. | [2.md](2.md) |
| **Disco lento / CPU esperando I/O (%wa)** | `iostat -xz 1` | `%util`, `await` | `%util` cercano al 100% o tiempos de acceso `await > 15ms`. | [2.md](2.md) |
| **Servicio o puerto no responde** | `ss -tulpn` | `Local Address:Port` | Comprobar si el proceso está escuchando en `0.0.0.0` o solo en `127.0.0.1`. | [3.md](3.md) |
| **Saturación del ancho de banda** | `iftop -i <interfaz>` | Columnas de tasa | Identificar la IP o tráfico que satura la tarjeta de red. | [3.md](3.md) |

---

<div align="center">
  <sub>Módulo de Administración de Sistemas y DevOps • <b>Jose Vizuete</b></sub>
</div>
