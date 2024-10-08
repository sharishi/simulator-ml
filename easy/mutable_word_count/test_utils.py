import utils


def test_word_count() -> None:
    """Check stable work of the function."""
    batch = ["hello world", "hello world", "hello world"]
    count = utils.word_count(batch, {})
    assert count == {"hello": 3, "world": 3}


def test_word_count_tricky():
    """Test tricky word count"""
    count1 = utils.word_count(["first test"])
    count2 = utils.word_count(["second test"])

    # Ожидаем, что словари независимы.
    assert count1 == {"first": 1, "test": 1}
    assert count2 == {"second": 1, "test": 1}

