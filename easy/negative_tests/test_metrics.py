import metrics


def test_non_int_clicks():
    """Test non-int-clicks"""
    try:
        metrics.ctr(1.5, 2)
    except TypeError:
        pass
    else:
        raise AssertionError("Non int clicks not handled")


def test_non_int_views():
    """Test non-int-views"""
    try:
        metrics.ctr(2, 2.5)
    except TypeError:
        pass
    else:
        raise AssertionError("Non int views not handled")


def test_non_positive_clicks():
    """Test non-positive-clicks"""
    try:
        metrics.ctr(-1, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Non positive clicks not handled")


def test_non_positive_views():
    """Test non-positive_views"""
    try:
        metrics.ctr(1, -1)
    except ValueError:
        pass
    else:
        raise AssertionError("Non positive views not handled")


def test_clicks_greater_than_views():
    """test-clicks-greater-than-views"""
    try:
        metrics.ctr(2, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("less clicks not handled")


def test_zero_views():
    """test_zero_views"""
    try:
        metrics.ctr(2, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero views not handled")

