def deface_string_middle(string, visible=4, deface_string="..."):
    strlen = len(string)
    return string[:int(round(visible / 2))] + deface_string * 3 + string[int(round((strlen - visible / 2))):]


def deface_string_end(string, visible=4, deface_string="..."):
    strlen = len(string)
    return deface_string + string[int(strlen - visible):]
