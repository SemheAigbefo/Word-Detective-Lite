from app.core.daily_seed import target_index_for

def test_daily_seed_deterministic():
    a = target_index_for('2025-09-15', 'salt1', 1000)
    b = target_index_for('2025-09-15', 'salt1', 1000)
    assert a == b

def test_daily_seed_salt_changes():
    a = target_index_for('2025-09-15', 'salt1', 1000)
    c = target_index_for('2025-09-15', 'salt2', 1000)
    assert a != c

def test_daily_seed_modulo():
    idx = target_index_for('2025-09-15', 'salt1', 7)
    assert 0 <= idx < 7
