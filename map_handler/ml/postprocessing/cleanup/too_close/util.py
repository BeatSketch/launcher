def has_stack(marked: list[list[bool]]):
    count = 0
    for layer in marked:
        for pos in layer:
            if pos:
                count += 1

    return count > 1
