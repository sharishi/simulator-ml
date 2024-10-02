import re
from string import punctuation
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from joblib import Parallel, delayed


def clean_text(text: str) -> str:
    """Функция для очистки текста."""
    lemmatizer = WordNetLemmatizer()
    text = str(text)

    # Удаление URL и упоминаний
    text = re.sub(r"https?://[^,\s]+,?", "", text)
    text = re.sub(r"@[^,\s]+,?", "", text)

    stop_words = set(stopwords.words("english"))  # Используем set для более быстрой проверки
    transform_text = text.translate(str.maketrans("", "", punctuation))
    transform_text = re.sub(" +", " ", transform_text)  # Удаление лишних пробелов

    text_tokens = word_tokenize(transform_text)  # Токенизация
    lemma_text = [lemmatizer.lemmatize(word.lower()) for word in text_tokens]  # Лемматизация

    # Фильтрация стоп-слов
    cleaned_text = " ".join([word for word in lemma_text if word not in stop_words])
    return cleaned_text


def clear_data(source_path: str, target_path: str, n_jobs=-1):
    """Baseline process df

    Parameters
    ----------
    source_path : str
        Path to load dataframe from

    target_path : str
        Path to save dataframe to

    n_jobs : int
        Number of jobs for parallel processing (default is -1, which uses all available CPUs)
    """
    # Загрузка данных
    data = pd.read_parquet(source_path)
    data = data.copy().dropna().reset_index(drop=True)

    # Параллельная обработка текстов
    cleaned_text_list = Parallel(
        n_jobs=n_jobs, backend="multiprocessing", verbose=5 * n_jobs
    )(delayed(clean_text)(text) for text in data["text"])

    # Сохранение очищенных текстов в новый столбец
    data["cleaned_text"] = cleaned_text_list
    data.to_parquet(target_path)

# Пример вызова функции
# clear_data("source_data.parquet", "cleaned_data.parquet", n_jobs=2)

