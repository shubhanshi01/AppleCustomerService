from src.config import INTENTS

INTENT_DESCRIPTIONS = {
    "account_and_security": "Apple ID, password, login, verification, account access, or suspicious activity.",
    "billing_and_purchase": "App Store, iTunes, subscription, charge, refund, payment, or purchase.",
    "device_hardware": "Physical device fault: battery, screen, camera, buttons, charging, or overheating.",
    "software_and_update": "iOS, macOS, app behaviour, update, crash, notification, or feature bug.",
    "service_and_connectivity": "iCloud, Apple Music, FaceTime, iMessage, Wi-Fi, cellular, or syncing.",
    "how_to_and_setup": "How to use, configure, enable, transfer, or set up an Apple product or feature.",
    "order_and_repair": "Delivery, order, appointment, warranty, repair, replacement, or store visit.",
    "other": "Message does not provide enough evidence for a more specific operational intent.",
}

KEYWORDS = {
    "account_and_security": ("apple id", "password", "sign in", "login", "locked", "verification", "hacked", "security"),
    "billing_and_purchase": ("charge", "charged", "refund", "payment", "billing", "purchase", "subscription", "itunes", "app store", "receipt"),
    "device_hardware": ("battery", "screen", "display", "camera", "charger", "charging", "overheat", "button", "speaker", "headphone"),
    "software_and_update": ("ios", "update", "upgrade", "crash", "bug", "notification", "keyboard", "app", "software"),
    "service_and_connectivity": ("icloud", "imessage", "facetime", "wifi", "wi-fi", "bluetooth", "sync", "apple music", "network"),
    "how_to_and_setup": ("how do", "how can", "setup", "set up", "enable", "transfer", "turn on", "where can"),
    "order_and_repair": ("order", "delivery", "shipped", "repair", "replace", "replacement", "warranty", "appointment", "store"),
}
