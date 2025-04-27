from vdf import VDFDict

def vdf_dict_to_dict_recursive(vdf_dict: VDFDict | list | dict) -> dict | list:
    """
    Recursively convert a VDFDict to a standard Python dictionary.
    """
    if isinstance(vdf_dict, VDFDict):
        return {key: vdf_dict_to_dict_recursive(value) for key, value in vdf_dict.items()}
    elif isinstance(vdf_dict, list):
        return [vdf_dict_to_dict_recursive(item) for item in vdf_dict]
    elif isinstance(vdf_dict, dict):
        return {key: vdf_dict_to_dict_recursive(value) for key, value in vdf_dict.items()}
    else:
        return vdf_dict

def vdf_copy_inner_values(vdf_dict: VDFDict, key: str) -> VDFDict:
    """
    Copy inner values of a VDFDict for a specific key.
    """
    if key not in vdf_dict:
        return VDFDict({})

    result = VDFDict({})
    vdf_dict_list = vdf_dict.get_all_for(key)

    for value in vdf_dict_list:
        if not isinstance(value, VDFDict):
            continue

        for inner_key, inner_value in value.items():
            result[inner_key] = inner_value

    return result