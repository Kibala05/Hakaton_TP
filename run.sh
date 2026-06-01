#!/bin/bash
INBOX_DIR="inbox"
echo "  Обработка корпоративной почты"

if [ ! -d "$INBOX_DIR" ]; then
    echo "ОШИБКА: папка inbox/ не найдена"
    exit 1
fi

COUNT=$(ls "$INBOX_DIR" | wc -l)
echo "Писем в inbox/: $COUNT"
echo ""

python3 main.py 2>&1 | tee run.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "СТАТУС: Успешно"
    echo "Лог сохранён в run.log"
else
    echo ""
    echo "СТАТУС: Ошибка"
fi