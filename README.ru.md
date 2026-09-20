[![validate-examples](https://github.com/Julia7856/honestshield/workflows/validate-examples/badge.svg)](https://github.com/Julia7856/honestshield/actions)

[English](README.md) | **Русский**

# HonestShield

Сертификат честности для приложений.

Как Energy Star для холодильников, только для работы с данными. Приложение публикует `honesty.txt` — декларацию о работе с данными. HonestShield проверяет реальное поведение против декларации. Совпало → зелёный знак. Соврало → красный.

## Проблема

Политики обработки данных — 40 страниц текста, которые никто не читает. Разработчики обещают одно, делают другое. Пользователи не знают, кому доверять.

## Решение

HonestShield делает работу с данными **прозрачной**:
- Машины читают honesty.txt за секунду
- Пользователи видят знак честности
- Разработчики получают рыночное давление (нет знака = нет доверия)

## Как работает

1. Сервис публикует `/.well-known/honesty.txt`
2. HonestShield парсит декларацию
3. Динамический аудит проверяет реальный трафик
4. Сверка: декларация против поведения
5. Выдача или отзыв сертификата
6. Ежедневный бот перепроверяет каждый зарегистрированный сервис — результаты открыты

## Живые инструменты

- **Веб-валидатор**: https://julia7856.github.io/honestshield/ — проверка любой декларации в браузере, ссылка-отчёт, копирование бейджа
- **Статус реестра**: https://julia7856.github.io/honestshield/status.html — кто честен сегодня, обновляется каждый день через GitHub Actions

## Как внедрить за 5 минут

### Шаг 1. Создай honesty.txt

Скопируй пример и замени данные на свои. Обязательно заполни:
- шапку (App, Host, Contact, даты)
- секцию DATA (какие данные и зачем)
- секцию PROMISES (`sell-data: no` обязательно)

### Шаг 2. Положи по адресу

```
https://твой-сайт.com/.well-known/honesty.txt
```

Это RFC 8615 — стандартное место для метаданных сайта.

### Шаг 3. Прогони валидатор

Локально:
```bash
python validator/validate.py honesty.txt
```

Или через URL:
```bash
python validator/validate.py --url https://твой-сайт.com
```

Или в браузере: [веб-валидатор](https://julia7856.github.io/honestshield/).

Должно быть `result: OK` (warnings допустимы).

### Шаг 4. Добавь ссылку в футер

```html
<footer>
  <a href="/.well-known/honesty.txt">honesty.txt</a>
</footer>
```

### Шаг 5 (опционально). Добавь бейдж

Бейджи уже существуют — скопируй готовый сниппет из веб-валидатора (он подберёт нужный по результату), или используй:

```html
<img src="https://raw.githubusercontent.com/Julia7856/honestshield/main/assets/badge-verified.svg" alt="honesty.txt: verified" height="20">
```

## Стандарт

Смотри STANDARD.md — полная спецификация honesty.txt.

## Валидатор

Эталонная реализация — `validator/validate.py` (чистый Python, без зависимостей):

```bash
python validator/validate.py examples/shop.honesty.txt
python validator/validate.py --url https://example.com
```

GitHub Actions прогоняет проверку при каждом коммите — значок сверху живое доказательство.

## Бейджи

Три состояния проверки:

![verified](assets/badge-verified.svg) — декларация полностью совпадает с поведением.
![warnings](assets/badge-warnings.svg) — декларация корректна, но есть мелкие замечания.
![failed](assets/badge-failed.svg) — декларация не совпадает с поведением.

Чтобы разместить бейдж на своём сайте, используйте:

```html
<img src="https://raw.githubusercontent.com/Julia7856/honestshield/main/assets/badge-verified.svg" alt="honesty.txt: verified" height="20">
```

## Пример honesty.txt

```txt
# HONESTY.TXT — v1
App: com.example.app
Host: example.com
Version: 42
Contact: data@example.com
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
