def merge(a: dict, b: dict) -> dict:
    """Merge two dictionaries. Dict b takes precedence

    Args:
        a: The base dictionary to merge into
        b: The dictionary to merge into a. Its values take precedence

    Returns:
        The merged dictionary
    """
    combined = {}
    for key in b:
        val = b[key]
        try:
            a[key]
            if isinstance(val, dict):
                combined[key] = merge(val, a[key])
            elif isinstance(val, list):
                combined[key] = val
                for v in a[key]:
                    combined[key].append(v)
            else:
                combined[key] = val
        except KeyError:
            combined[key] = val

    for key in a:
        try:
            b[key]
        except KeyError:
            combined[key] = a[key]

    return combined
