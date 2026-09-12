def draft_reply(message, intent, evidence, escalate):
    """Conservative template; retrieved text is evidence, never blindly copied."""
    if escalate:
        return "Thanks for reaching out. To protect your account and make sure this is handled correctly, please continue with Apple Support directly at getsupport.apple.com."
    if intent == "how_to_and_setup":
        return "Thanks for reaching out. Please try the relevant steps in Apple Support's guide at getsupport.apple.com, and let us know what you see after trying them."
    if intent == "software_and_update":
        return "Thanks for the details. Please check that your device is updated, then try restarting it and testing again. If it continues, Apple Support can investigate at getsupport.apple.com."
    if intent == "service_and_connectivity":
        return "Thanks for letting us know. Please check your connection and try again; if the issue continues, Apple Support can look into the account or service details at getsupport.apple.com."
    if intent == "device_hardware":
        return "Thanks for the details. Apple Support can help diagnose the device and discuss service options at getsupport.apple.com."
    return "Thanks for reaching out. Apple Support can help with this at getsupport.apple.com."
