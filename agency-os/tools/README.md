# Growth Cycle — первый исполняемый инструмент

Python 3, стандартная библиотека. Сетевых запросов и публикации нет. Все входные клиентские файлы держать в закрытом клиентском проекте.

## Команды

```bash
python agency-os/tools/growth_cycle.py baseline --input /private/media.json --since 2026-09-07 --out /private/baseline.json
python agency-os/tools/growth_cycle.py retrospective --input /private/media.json --baseline /private/baseline.json --media-id REAL_MEDIA_ID --out /private/retrospective.json
python agency-os/tools/growth_cycle.py record --experiment /private/experiment.json --input /private/new-media.json --out /private/snapshots/7d.json
python agency-os/tools/growth_cycle.py decide --experiment /private/experiment.json --snapshots /private/snapshots/7d.json --out /private/decision.json
python -m unittest discover -s agency-os/tools -p 'test_*.py'
```

## Входы и смысл результата

Выгрузка: объект с `data`, список строк Windsor.ai. Нужны `media_id`, `timestamp`, `data_fetched_at`, `media_type`, `media_product_type`, доступные `media_reach`, `media_views`, `media_shares`, `media_saved`, `media_comments_count`, `media_like_count`. Поля — из discovery провайдера. Подписи и данные аккаунта инструменту не нужны.

`baseline` считает медианы отдельно по форматам. Недостаточно зрелые посты исключаются по фактическому времени источника. Это зрелый lifetime-ориентир с разным возрастом постов; он не является результатом за одинаковые 48 часов или 7 дней. Trial, реклама и коллаборации могут смешиваться, если соответствующие признаки не получены.

`retrospective` записывает решение о новом тесте по реально опубликованному посту. Гипотеза формируется после публикации; это явно ретроспективная приоритизация.

`record` проверяет точный media_id, время и формат. `decide` использует заранее зафиксированную операционную цель, реальный возраст и источник свежего замера. Достигнутая цель приводит к RETEST для проверки повторяемости. Никакой причинности, статистической значимости или matched-age winner инструмент не объявляет.

Отсутствующие числа остаются null, нули сохраняются как нули. Повторные lifetime-строки нельзя суммировать. Старый кэш не становится новым замером от запуска программы. `data_fetched_at` без зоны интерпретируется как UTC, согласно контракту Windsor.ai.

Windsor.ai может сохранять старые дни в кэше. Каждый контрольный замер проверять по `data_fetched_at`; если источник не обновился к нужному возрасту, результат INCONCLUSIVE. Требуется свежий Insights-замер; перестановка даты в JSON недопустима.
