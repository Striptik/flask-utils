import json


def translate(key, lang="fr"):
    try:
        with open(f"i18n/{lang}.json", "r") as f:
            data = json.load(f)
            translation = data.get(key, None)
            return key if translation is None else translation
    except Exception:
        return key
