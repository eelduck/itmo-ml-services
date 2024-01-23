# ML-DEV: Классификация зловредного ПО

Цель проекта - разработать ML-сервис с подсистемой биллинга, который будет осуществлять предсказания на основе ML-моделей и списывать кредиты с личного счета пользователя за успешное выполнение предсказания. Сервис должен быть надежным, масштабируемым и готовым для использования в продакшн-окружении.

## Описание датасета 
Датасет содержит данные о мобильных устройствах на платформе Android и образцах зловредного программного обеспечения. Всего в датасете 4465 экземпляров ПО и 241 предварительно обработанный категориальный признак. Целевым признаком для классификации является значение поля label - отношение ПО к зловредному или доверенному.

## Реализация
1. Решена ML задача с помощью трех моделей: LGBM, Logistic Regression, Random Forest
2. Backend часть на FastAPI c JWT авторизацией
3. Frontend часть на Plotly Dash
4. Выполнение предсказаний с помощью синхронная очереди задач RQ
5. Деплой приложения с использованием docker и docker compose

## Содержание репозитория
- [backend/](/backend/) - исходный код backend части проекта.
- [backend/models](/backend/models/) - сохраненные модели в формате .joblib.
- [frontend/](/frontend/) - исходный код frontend части проекта.
- [data/](/data/) - датасет для построения модели и пример тестового датасета.
- [ml_task/](/ml_task/) - jupyter ноутбук с решением ML задачи.

## Запуск системы

У вас должен быть установлен docker и docker-compose

- Для запуска системы введите команду
    ```bash
    docker-compose up -d --build
    ```
  После этого у вас запустится Dash приложение по адресу http://localhost:8050/

## Демо
1. Зарегистрируйтесь в приложении - http://localhost:8050/register

![image](https://github.com/eelduck/itmo-ml-services/assets/41739221/c76efc92-1b23-423a-9567-3891c4efea0f)

2. Войдите в свой аккаунт - http://localhost:8050/login

![image](https://github.com/eelduck/itmo-ml-services/assets/41739221/d4090b43-ec5e-4d0d-8ff2-b4a205a21b2b)

3. Далее вас перенаправит на основную страницу приложения - http://localhost:8050/predictions

![image](https://github.com/eelduck/itmo-ml-services/assets/41739221/ba0b7673-c45a-48b3-bb11-41e0370d4466)

Здесь вы можете: 
- Увидеть свой баланс кредитов
- Выбрать модель для предсказания из выпадающего списка
- Загрузить тестовый датасет для предсказания. Формат должен быть как в [примере](/data/android_test_1.csv).
- Отправить задачу на предсказание
- Получить результаты своих предсказаний. Сами лейблы в колонке predictions
