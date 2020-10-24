import string
import re
from typing import List, Set

from data_cleaner_app.material_reference import TestMaterialRetriever, Material


def get_base_material_from_name(given_name: str) -> str:
    """
    get_base_material_from_name('Zirconia, (ZrO2)')
    ->
    'Zirconium Oxide'
    """

    if not given_name:

        raise ValueError(f"Expected required name value, got {given_name}")

    material_retriever = TestMaterialRetriever()

    name_tokens = _tokenize_name(given_name)

    matching_materials = set()

    for token in name_tokens:

        if material_retriever.contains_synonym(token):

            matching_materials.add(material_retriever.get_by_synonym(token))

    if not matching_materials:

        raise ValueError(f"Failed to identify material matching name `{given_name}`")

    elif len(matching_materials) == 1:

        single_material = matching_materials.pop()
        return single_material.name

    else:

        meta_materials = _get_meta_materials(matching_materials)

        if len(meta_materials) == 1:
            return meta_materials[0].name

        else:
            raise ValueError(
                f"Identified multiple materials matching name `{given_name}`: {matching_materials}"
            )


def _get_meta_materials(matching_materials: Set[Material]) -> List[Material]:
    """
    _get_meta_materials([zirconium_oxide,zirconium])
    ->
    [zirconium_oxide]

    _get_meta_materials([zirconium_oxide,copper])
    ->
    [zirconium_oxide,copper]
    """
    material_list = list(matching_materials)
    meta_materials = []
    for i in range(len(material_list)):
        current_material = material_list[i]
        is_submaterial = False
        for j in range(len(material_list)):
            if i != j:
                other_material = material_list[j]
                for current_synonym in current_material.synonyms:
                    for other_synonym in other_material.synonyms:
                        if current_synonym in other_synonym:
                            is_submaterial = True
        if not is_submaterial:
            meta_materials.append(current_material)

    return meta_materials


def _tokenize_name(given_name: str) -> List[str]:
    """
    _tokenize_name('Zirconium Oxide, Zirconia, (ZrO2)')

    -> 
    [   
        '(zro2)', 
        'oxide', 
        'oxide,', 
        'zirconia', 
        'zirconia,', 
        'zirconium', 
        'zirconium oxide', 
        'zirconiumoxide', 
        'zro2'
    ]
    """

    name_tokens = []

    name_split_on_whitespace = given_name.split()
    name_split_on_commas = given_name.split(",")
    name_split_on_parentheses = re.findall(r"\([^\)]*\)", given_name)
    split_name = (
        name_split_on_whitespace + name_split_on_commas + name_split_on_parentheses
    )

    for material_name in split_name:

        lowercase_material_name = material_name.lower().strip()
        no_white_space_material_name = lowercase_material_name.translate(
            str.maketrans("", "", string.whitespace)
        )
        no_punctuation_material_name = no_white_space_material_name.translate(
            str.maketrans("", "", string.punctuation)
        )

        if not no_punctuation_material_name:
            continue

        cleaned_material_names = [
            lowercase_material_name,
            no_white_space_material_name,
            no_punctuation_material_name,
        ]

        name_tokens += cleaned_material_names

    return sorted(list(set(name_tokens)))
