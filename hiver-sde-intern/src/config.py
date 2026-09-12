from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW_TWEETS = DATA / "raw" / "twcs.csv"
PROCESSED = DATA / "processed"
ARTIFACTS = DATA / "artifacts"
GOLDEN = DATA / "golden" / "apple_golden.csv"
BRAND = "AppleSupport"

INTENTS = (
    "account_and_security", "billing_and_purchase", "device_hardware",
    "software_and_update", "service_and_connectivity", "how_to_and_setup",
    "order_and_repair", "other",
)
