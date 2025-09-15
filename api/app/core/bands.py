from typing import Literal

Band = Literal["Cold","Cool","Warm","Hot","Very Hot"]

def band_for(sim: float) -> Band:
    if sim < 0.25:
        return "Cold"
    if sim < 0.45:
        return "Cool"
    if sim < 0.65:
        return "Warm"
    if sim < 0.80:
        return "Hot"
    return "Very Hot"
