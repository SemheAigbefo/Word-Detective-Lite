from app.core.normalize import normalize_word

def test_normalize_basic():
    assert normalize_word('  Apple  ') == 'apple'
    assert normalize_word('BANANA') == 'banana'
    assert normalize_word('pear123') == ''
    assert normalize_word('kiwi-juice') == ''
