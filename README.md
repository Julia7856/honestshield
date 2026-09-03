[![validate-examples](https://github.com/Julia7856/honestshield/actions/workflows/validate.yml/badge.svg)](https://github.com/Julia7856/honestshield/actions/workflows/validate.yml)

# HonestShield

Сертификат честности для приложений.

Как Energy Star для холодильников, только для приватности. Приложение публикует `honesty.txt` — декларацию о работе с данными. HonestShield проверяет реальное поведение против декларации. Совпало → зелёный знак. Соврало → красный.

## Проблема

Политики приватности — 40 страниц текста, которые никто не читает. Разработчики обещают одно, делают другое. Пользователи не знают, кому доверять.

## Решение

HonestShield делает приватность **видимой**:
- Машины читают honesty.txt за секунду
- Пользователи видят знак честности
- Разработчики получают рыночное давление (нет знака = нет доверия)

## Как работает

1. Сервис публикует `/.well-known/honesty.txt`
2. HonestShield парсит декларацию
3. Динамический аудит проверяет реальный трафик
4. Сверка: декларация против поведения
5. Выдача или отзыв сертификата

## Стандарт

Смотри [STANDARD.md](STANDARD.md) — полная спецификация honesty.txt.

## Валидатор

Эталонная реализация — `validator/validate.py` (чистый Python, без зависимостей):

```bash
python validator/validate.py examples/shop.honesty.txt
python validator/validate.py --url https://example.com
```

GitHub Actions прогоняет проверку при каждом коммите — значок сверху живое доказательство.

## Пример honesty.txt

```txt
# HONESTY.TXT — v1
App: com.example.app
Host: example.com
Version: 42
Contact: privacy@example.com
Updated: 2026-09-02
Expires: 2027-03-02

## DATA
email: purpose=auth; retain=90d; shared=none
location: purpose=delivery; retain=session; shared=none

## TRACKERS
none

## PROMISES
sell-data: no
delete-on-request: yes-72h
```

## Лицензия

MIT — используй свободно.

---

**Знак честности, который невозможно подделать.**
