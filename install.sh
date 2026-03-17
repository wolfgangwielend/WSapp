#!/bin/bash
# WS App - Frappe Framework Setup Script
# Installiert und konfiguriert die komplette Frappe-Umgebung

set -e

BENCH_DIR="/home/frappe/frappe-bench"
SITE_NAME="wsapp.localhost"
ADMIN_PASSWORD="admin"
DB_ROOT_PASSWORD="123"
APP_DIR=$(pwd)

echo "=== WS App - Frappe Setup ==="
echo ""

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Prüfe ob als frappe User oder root
if [ "$(id -u)" = "0" ]; then
    warn "Läuft als root. Empfohlen: Als Benutzer 'frappe' ausführen"
fi

# 1. System-Abhängigkeiten
info "Installiere System-Abhängigkeiten..."
apt-get update -qq
apt-get install -y -qq \
    git python3-dev python3-pip \
    redis-server mariadb-server mariadb-client \
    nodejs npm \
    wkhtmltopdf \
    libmysqlclient-dev \
    supervisor nginx

# 2. Services starten
info "Starte Dienste..."
service mariadb start || true
service redis-server start || true

# 3. MariaDB konfigurieren
info "Konfiguriere MariaDB..."
mysql -u root -e "
    ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';
    FLUSH PRIVILEGES;
" 2>/dev/null || true

# 4. frappe-bench installieren
info "Installiere frappe-bench..."
pip3 install frappe-bench -q

# 5. Frappe-Benutzer anlegen (falls nicht vorhanden)
if ! id "frappe" &>/dev/null; then
    info "Lege Benutzer 'frappe' an..."
    useradd -m -s /bin/bash frappe
fi

# 6. Bench initialisieren
info "Initialisiere Frappe-Bench (Version 15)..."
if [ ! -d "$BENCH_DIR" ]; then
    su - frappe -c "bench init --frappe-branch version-15 $BENCH_DIR"
else
    warn "Bench-Verzeichnis existiert bereits: $BENCH_DIR"
fi

# 7. App verlinken
info "Verlinke WS App..."
ln -sf "$APP_DIR" "$BENCH_DIR/apps/wsapp" 2>/dev/null || true

# 8. Site erstellen
info "Erstelle Frappe-Site: $SITE_NAME"
cd "$BENCH_DIR"
su - frappe -c "
    cd $BENCH_DIR &&
    bench new-site $SITE_NAME \
        --db-root-password $DB_ROOT_PASSWORD \
        --admin-password $ADMIN_PASSWORD \
        --set-default
"

# 9. App installieren
info "Installiere WS App auf Site..."
su - frappe -c "
    cd $BENCH_DIR &&
    bench --site $SITE_NAME install-app wsapp
"

# 10. Entwicklungsmodus aktivieren
su - frappe -c "
    cd $BENCH_DIR &&
    bench set-config developer_mode 1 &&
    bench --site $SITE_NAME set-config developer_mode 1
"

echo ""
echo "================================================"
echo -e "${GREEN}Installation erfolgreich!${NC}"
echo "================================================"
echo ""
echo "Starte den Entwicklungsserver mit:"
echo "  cd $BENCH_DIR && bench start"
echo ""
echo "Öffne im Browser:"
echo "  http://localhost:8000"
echo ""
echo "Login:"
echo "  Benutzer: Administrator"
echo "  Passwort: $ADMIN_PASSWORD"
echo ""
