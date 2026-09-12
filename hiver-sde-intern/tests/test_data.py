from src.intent.taxonomy import INTENT_DESCRIPTIONS
from src.config import INTENTS

def test_all_intents_are_documented():
    assert set(INTENTS) == set(INTENT_DESCRIPTIONS)
