# def word_count1(texts):
#     count = {}
#     for text in texts:
#         for word in text.split():
#             count[word] = count.get(word, 0) + 1
#     return count


def word_count(batch, count=None):
    """word_count"""
    if count is None:
        count = {}
    for text_group in batch:
        for text in text_group:
            for word in text.split():
                count[word] = count.get(word, 0) + 1
    return count

