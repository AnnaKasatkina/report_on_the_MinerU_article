# report_on_the_MinerU_article

## О проекте

**MinerU** — это open-source инструмент для точного извлечения структурированного содержимого из PDF-документов.  
Он поддерживает:
- извлечение текста и структуры (layout),
- OCR для сканированных документов,
- таблицы и формулы,
- экспорт результатов в Markdown и JSON.

Данный репозиторий используется как **учебно-исследовательский проект** по практическому машинному обучению:  
запуск, анализ работы модели на разных типах документов и подготовка отчётных материалов (результаты, скриншоты, презентация).

## Структура репозитория

```text
demo/                    # демо-скрипты MinerU
mineru/                  # основной код библиотеки
run_one.py               # запуск на одном PDF
run_all.py               # батч-прогон на наборе PDF
results/                 # результаты обработки (md, json, pdf)
slides.pdf               # презентация
environment.yml          # conda-окружение
README.md
```

## Установка (с помощью Conda)

### 1. Клонирование репозитория

```bash
git clone https://github.com/AnnaKasatkina/report_on_the_MinerU_article
cd MinerU
```
### 2. Создание conda-окружения

```bash
conda env create -f environment.yml
conda activate mineru
```

### 3. Установка проекта

> Выполнять **из корня репозитория**, при активированном окружении

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[core]"
```

## Загрузка модельных весов

Перед первым запуском необходимо скачать модели:

```bash
mineru-models-download
```

Далее выбрать:

* **источник**: `huggingface`
* **тип моделей**: `pipeline`

## Тестовый запуск

### 1. Запуск на одном документе

Поместите ваш файл `sample.pdf` в папку:

```text
demo/pdfs_testset/
```

И выполните в терминале

```bash
python run_one.py
```

Результаты будут сохранены в:

```text
results/sample/
```

Содержимое:

* `sample.md` — итоговый Markdown
* `sample_middle.json` — промежуточный формат
* `sample_model.json` — вывод модели
* `*_layout.pdf` — визуализация layout bounding boxes

---

### 3. Батч-прогон на наборе документов

```bash
python run_all.py
```

После выполнения:

* `results/<doc_name>/` — результаты по каждому PDF
* `results/summary.csv` — сравнительная таблица
* `results/summary.json` — метаданные прогонов
