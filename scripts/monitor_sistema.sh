#!/usr/bin/env bash
# ==============================================================================
# Script de Monitorización Rápida del Sistema Linux
# Módulo: Administración de Sistemas / DevOps
# Autor: Jose Vizuete (eljoviz)
# ==============================================================================

set -euo pipefail
clear 2>/dev/null || true

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # Sin color

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${BOLD}DASHBOARD DE MONITORIZACIÓN DEL SISTEMA - LINUX${NC}                ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}  Fecha: $(date '+%Y-%m-%d %H:%M:%S')  |  Host: $(hostname)           ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. INFORMACIÓN DE CARGA Y CPU
echo -e "${BOLD}${BLUE}[1] CARGA DEL SISTEMA Y CPU${NC}"
UPTIME=$(uptime -p 2>/dev/null || uptime)
LOAD=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
CORES=$(nproc)
echo -e "  • ${BOLD}Tiempo activo:${NC} $UPTIME"
echo -e "  • ${BOLD}Carga media (1, 5, 15 min):${NC} $LOAD (Núcleos detectados: $CORES)"

echo -e "  • ${BOLD}Top 3 procesos por consumo de CPU:${NC}"
ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -n 4 | awk 'NR>1 {printf "    - PID %-6s %-10s CPU: %5s%%  MEM: %5s%%  (%s)\n", $1, $2, $3, $4, $5}'
echo ""

# 2. ESTADO DE MEMORIA RAM Y SWAP
echo -e "${BOLD}${BLUE}[2] ESTADO DE LA MEMORIA${NC}"
MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
SWAP_TOTAL=$(free -m | awk '/Swap:/ {print $2}')
SWAP_TOTAL=${SWAP_TOTAL:-0}
SWAP_USED=$(free -m | awk '/Swap:/ {print $3}')
SWAP_USED=${SWAP_USED:-0}

MEM_PCT=$(( 100 * (MEM_TOTAL - MEM_AVAIL) / MEM_TOTAL ))
if [ "$MEM_PCT" -gt 85 ]; then
    MEM_STATUS="${RED}CRÍTICO ($MEM_PCT%)${NC}"
elif [ "$MEM_PCT" -gt 70 ]; then
    MEM_STATUS="${YELLOW}AVISO ($MEM_PCT%)${NC}"
else
    MEM_STATUS="${GREEN}OK ($MEM_PCT%)${NC}"
fi

echo -e "  • ${BOLD}RAM Total:${NC} ${MEM_TOTAL} MB | ${BOLD}En uso:${NC} ${MEM_USED} MB | ${BOLD}Disponible:${NC} ${MEM_AVAIL} MB -> $MEM_STATUS"
if [ "$SWAP_TOTAL" -gt 0 ]; then
    SWAP_PCT=$(( 100 * SWAP_USED / SWAP_TOTAL ))
    echo -e "  • ${BOLD}Swap:${NC} ${SWAP_USED} MB / ${SWAP_TOTAL} MB ($SWAP_PCT% en uso)"
else
    echo -e "  • ${BOLD}Swap:${NC} No configurada o deshabilitada"
fi
echo ""

# 3. ESPACIO EN DISCO
echo -e "${BOLD}${BLUE}[3] ESPACIO EN PARTICIONES DE DISCO${NC}"
df -hP -x tmpfs -x devtmpfs -x squashfs | awk 'NR>1 {print $1, $2, $3, $4, $5, $6}' | while read -r fs size used avail pct mountpoint; do
    pct_num=$(echo "$pct" | tr -d '%' | tr -d ' ')
    if [ -n "$pct_num" ] && [ "$pct_num" -ge 90 ] 2>/dev/null; then
        alert="${RED}[CRÍTICO]${NC}"
    elif [ -n "$pct_num" ] && [ "$pct_num" -ge 80 ] 2>/dev/null; then
        alert="${YELLOW}[AVISO]${NC}"
    else
        alert="${GREEN}[OK]${NC}"
    fi
    printf "  • %-20s %-6s usado de %-6s (disp: %-6s) %s %-12s %b\n" "$mountpoint" "$used" "$size" "$avail" "$pct" "" "$alert"
done
echo ""

# 4. RED Y CONECTIVIDAD
echo -e "${BOLD}${BLUE}[4] INTERFACES DE RED Y PUERTOS EN ESCUCHA${NC}"
if command -v ip >/dev/null 2>&1; then
    ip -br addr show | awk '$1 !~ /^lo/ {printf "  • Interfaz %-10s Estado: %-8s IP: %s\n", $1, $2, $3}'
fi

echo -e "  • ${BOLD}Servicios escuchando en la máquina:${NC}"
if command -v ss >/dev/null 2>&1; then
    ss -tuln | awk 'NR>1 {printf "    - %-5s %s\n", $1, $5}' | head -n 6
fi
echo ""

echo -e "${CYAN}══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Chequeo de monitorización completado con éxito.${NC}"
