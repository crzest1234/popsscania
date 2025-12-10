# Stub ML pipeline: à remplacer par YOLO/Detectron réels.
from typing import List, Dict
import random

def analyze_images_stub(image_paths: List[str]) -> Dict:
    """
    Retourne un JSON simulé avec défauts détectés et global_state_score.
    """
    defects = {
        "humidity": random.choice([True, False, False]),
        "cracks": random.choice([True, False, False]),
        "old_kitchen": random.choice([True, False]),
        "old_bathroom": random.choice([True, False]),
        "window_quality": random.choice(["old","ok","new"]),
        "floor_damage": random.choice(["none","minor","medium","major"]),
    }
    score = round(1 - sum([1 if v in (True,"major","old") else 0 for v in defects.values()]) / 6, 2)
    return {"defects": defects, "global_state_score": score, "confidence": 0.7}
