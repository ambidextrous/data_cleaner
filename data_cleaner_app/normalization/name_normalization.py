from typing import List, Dict


def get_name(
    source_name: str, base_material_name: str, warnings: List[Dict[str, str]]
) -> str:
    if base_material_name.strip().lower() in source_name.lower():
        return base_material_name
    else:
        message = f"No match found between source material name `{source_name}` and base material name `{base_material_name}`. Preserving source name `{source_name}``"
        warnings.append(message)
        return source_name
