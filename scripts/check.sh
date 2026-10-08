#!/usr/bin/env bash
# Kontrola przed wdrożeniem: czy w plikach nie został tymczasowy adres domeny / placeholdery.
cd "$(dirname "$0")/.."
bad=$(grep -rn 'TWOJA-DOMENA\|+48XXXXXXXXX' --include='*.html' --include='*.txt' --include='*.xml' --include='*.webmanifest' . | grep -v '<!--' || true)
if [ -n "$bad" ]; then echo "UWAGA – nieuzupełnione placeholdery:"; echo "$bad"; exit 1; fi
echo "OK – brak placeholderów."
