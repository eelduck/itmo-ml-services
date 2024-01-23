# ML-DEV: Классификация зловредного ПО

Цель проекта - разработать ML-сервис с подсистемой биллинга, который будет осуществлять предсказания на основе ML-моделей и списывать кредиты с личного счета пользователя за успешное выполнение предсказания. Сервис должен быть надежным, масштабируемым и готовым для использования в продакшн-окружении.

## Описание датасета 
Датасет содержит данные о мобильных устройствах на платформе Android и образцах зловредного программного обеспечения. Всего в датасете 4465 экземпляров ПО и 241 предварительно обработанный категориальный признак. Целевым признаком для классификации является значение поля label - отношение ПО к зловредному или доверенному.

## Содержание репозитория
- [backend/](/backend/) - исходный код backend части проекта.
- [frontend/](/frontend/) - исходный код frontend части проекта.
- [data/](/data/) - датасет для построения модели и пример тестового датасета.
- [ml_task/](/ml_task/) - jupyter ноутбук с решением ML задачи.

## Запуск системы

- Для запуска системы введите команды
    ```bash
    cd src/
    python gradio_app.py
    ```
  После этого у вас запустится Gradio приложение по адресу http://localhost:7860/

## Демо
- Введите желаемую должность, сколько лет опыта, ваши ключевые навыки и описание опыта работы.
- Нажмите кнопку __Подобрать вакансии__
- В течение 5 секунд вам выведется топ 5 вакансий под ваше резюме

![image](https://github.com/DmitryChatBotov/resume-vacancy-matching/assets/41739221/e1622b08-68c6-4cc3-a00f-4c88b2bad0d7)

### Оценка производительность демо:
 - RPS: 10
 - Объем данных в базе вакансий: 1200+. Выбирали только IT вакансии. Ищем тоже собственно по IT вакансиям
   
## Эксперименты
- FAISS search + Reranker (cross-encoder) - [/notebooks/experiments/faiss_reranker.ipynb](/notebooks/experiments/faiss_reranker.ipynb). Этот подход реализован в демо приложении
- BM25 search + SBERT + Reranker (cross-encoder) - [/notebooks/experiments/bm25_sbert_ranking.ipynb](/notebooks/experiments/bm25_sbert_ranking.ipynb)
- BerTopic - [/notebooks/experiments/bertopic.ipynb](/notebooks/experiments/bertopic.ipynb)
- Milvus search - [/notebooks/experiments/baseline_milvus.ipynb](/notebooks/experiments/baseline_milvus.ipynb) (для запуска нужно запустить файл docker-compose.yaml, который поднимет базу для milvus)
### Метрики
| Подход | F1 | Precision | Recall | TopK|
| --- | --- | --- | --- | --- |
|FAISS+Rerancer | 0.17 | 0.12 | 0.14 | 10 |
| BM25+SBERT+Reranker|0.15|0.11|0.13|10|
| BerTopic|0.07 | 0.09| 0.07 | 10|
|Milvus |0.1 | 0.1| 0.11|10|


## Сравнение энкодеров
Был собран датасет из 15 вакансий и 15 резюме, с помощью GPT-4 он был размечен на релевантность. Каждая вакансия с каждым резюме. На основе этого датасета и косинусной близости были просчитаны метрики работы энкодеров

| Модель | Accuracy |  Precision@10 | Recall@10 | F1@10 |
| --- | --- | --- | --- | --- |
| [intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)| 0.830 |  0.175 | 0.124 | 0.145 |
| [sentence-transformers/paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)| 0.805 |  0.156 | 0.180 | 0.127 |
| [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)| 0.810 |  0.138 | 0.094 | 0.111 |
| [sentence-transformers/distiluse-base-multilingual-cased-v1](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1)| 0.831 |  0.131 | 0.091 | 0.107 |
| [cointegrated/LaBSE-en-ru](https://huggingface.co/cointegrated/LaBSE-en-ru)| 0.823 |  0.169 | 0.119 | 0.139 |
