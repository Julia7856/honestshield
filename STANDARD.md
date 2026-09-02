# Стандарт honesty.txt v1

## Формат

Файл: `/.well-known/honesty.txt`  
Кодировка: UTF-8  
Тип: plain text

## Структура

```txt
# HONESTY.TXT — v1
# Комментарий

## Поля шапки
App: com.example.app
Host: example.com
Version: 42
Contact: privacy@example.com
Updated: 2026-09-02
Expires: 2027-03-02

## DATA
поле: purpose=зачем; retain=срок; shared=кому

## THIRD-PARTIES
название: домен (описание)

## TRACKERS
none | список

## PERMISSIONS
permission: использование

## PROMISES
promise: yes|no|детали

## SIGNATURE
badge: HS-YYYY-NNNNNN
```

## Секции

### DATA

Каждая строка описывает один тип данных:

```txt
email: purpose=auth; retain=90d; shared=none
location: purpose=delivery; retain=session; shared=none
photos: purpose=user-content; retain=user-forever; shared=none
```

Формат: `поле: purpose=значение; retain=срок; shared=значение`

**purpose** (цель):
- auth — аутентификация
- delivery — доставка/логистика
- user-content — пользовательский контент
- analytics — аналитика
- other — другое

**retain** (срок хранения):
- session — только на время сессии
- 7d, 30d, 90d, 1y, 5y — дни/годы
- user-forever — пока пользователь не удалит
- forever — бессрочно

**shared** (передача третьим лицам):
- none — никому не передаём
- название — передаём указанной стороне

### THIRD-PARTIES

```txt
payments: stripe.com (card data never touches us)
analytics: plausible.io (no cookies)
```

### TRACKERS

```txt
none
```

Или список:

```txt
facebook
google-analytics
```

### PERMISSIONS

```txt
camera: qr-login
network: core-function
microphone: voice-notes
```

### PROMISES

```txt
sell-data: no
ad-identifiers: no
delete-on-request: yes-72h
breach-notify: yes-72h
encryption: yes-aes256
```

Формат: `обещание: yes|no|детали`

### SIGNATURE

```txt
badge: HS-2026-000042
```

Ссылка на сертификат HonestShield.

## Проверка

HonestShield проверяет:
1. Декларация корректна (синтаксис)
2. Реальное поведение совпадает с декларацией
3. Сертификат действителен (не истёк, не отозван)

При несоответствии знак отзывается.

## Машиночитаемость

ИИ-агенты могут парсить honesty.txt для автоматических решений:
- Разрешить/запретить взаимодействие
- Выбрать альтернативный сервис
- Предупредить пользователя

## Лицензия

Спецификация свободна для использования.
