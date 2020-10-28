def get_name(given_name: str, identified_name: str) -> str:
    if identified_name.strip().lower() in given_name.lower():
        return identified_name
    else:
        return given_name
