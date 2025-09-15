from app.core.bands import band_for

def test_bands_boundaries():
    assert band_for(0.0) == 'Cold'
    assert band_for(0.2499) == 'Cold'
    assert band_for(0.25) == 'Cool'
    assert band_for(0.4499) == 'Cool'
    assert band_for(0.45) == 'Warm'
    assert band_for(0.6499) == 'Warm'
    assert band_for(0.65) == 'Hot'
    assert band_for(0.7999) == 'Hot'
    assert band_for(0.8) == 'Very Hot'
    assert band_for(0.9999) == 'Very Hot'
    assert band_for(1.0) == 'Very Hot'
