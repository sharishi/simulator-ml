import re
from collections import Counter
from typing import Dict, List
import requests


def normalize_domains(domains):
    normalized_domains = []
    for domain in domains:
        # Убираем пробелы, точки в конце и слэш, если он есть
        clean_domain = domain.strip().rstrip('/').rstrip('.')
        normalized_domains.append(clean_domain)
    return normalized_domains


def parse_urls(message: str) -> Dict[str, int]:
    """Parse a list of URL strings and check their reachability."""
    pattern = re.compile(r'(https?://)?(www\.)?([a-zA-Z0-9.-]+\.(com|org|co\.uk)(/[\w\-./?%&=:]*)?)')

    matches = pattern.findall(message)
    domains = [match[2] for match in matches]
    new_domains = normalize_domains(domains)

    # Проверка доступности URL
    reachable_urls = check_url_reachability(new_domains)

    # Подсчет только доступных доменов
    domain_count = Counter(reachable_urls)

    return dict(domain_count)


def check_url_reachability(urls: List[str]) -> List[str]:
    """Check the reachability of the list of URLs."""
    reachable_urls = []
    for url in urls:
        # Добавляем https:// перед проверкой
        full_url = f"https://{url}"

        try:
            response = requests.head(full_url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                reachable_urls.append(url)  # Сохраняем домен без протокола
                continue
        except requests.RequestException:
            pass

        try:
            response = requests.head(full_url, allow_redirects=False, timeout=5)
            if response.status_code == 200:
                reachable_urls.append(url)  # Сохраняем домен без протокола
        except requests.RequestException as e:
            print(e)

    return reachable_urls
