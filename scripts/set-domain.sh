#!/usr/bin/env bash
# Użycie: ./scripts/set-domain.sh https://twoja-domena.pl
# Podmienia tymczasowy adres domeny w canonical, Open Graph, robots.txt i sitemap.xml.
set -euo pipefail
[ $# -eq 1 ] || { echo "Podaj domenę, np. https://twoja-domena.pl"; exit 1; }
DOMAIN="${1%/}"
cd "$(dirname "$0")/.."
grep -rl 'https://TWOJA-DOMENA.pl' --include='*.html' --include='*.txt' --include='*.xml' . \
  | xargs sed -i "s|https://TWOJA-DOMENA.pl|${DOMAIN}|g"
echo "Ustawiono domenę: ${DOMAIN}"
