import re


def remove_html_tags(text: str) -> str:
    """Removes HTML tags from a given string."""
    clean_pattern = re.compile(r'<.*?>')
    return clean_pattern.sub('', text)


def parse_product_info(html: str) -> dict:
    """
    Extracts product information from the given HTML.

    Parameters:
        html (str): The input HTML data.

    Returns:
        product_info (dict): A dictionary containing the product's info.
    """

    # Регулярные выражения для извлечения информации
    title_pattern = r'<h1 class="product-title">(.+?)<\/h1>'
    category_pattern = r'<(.+?) class="product-category".*?>(.*?)<\/\1>'
    old_price_pattern = r'<span class="price-old">(.+?)<\/span>'
    new_price_pattern = r'<span class="price-new">(.+?)<\/span>'

    title = re.search(title_pattern, html)
    category = re.search(category_pattern, html)
    old_price = re.search(old_price_pattern, html)
    new_price = re.search(new_price_pattern, html)

    product_info = {
        'title': remove_html_tags(title.group(1)) if title else '',
        'category': remove_html_tags(category.group(2)) if category else '',
        'old_price': remove_html_tags(old_price.group(1)) if old_price else '',
        'new_price': remove_html_tags(new_price.group(1)) if new_price else '',
    }

    return product_info
