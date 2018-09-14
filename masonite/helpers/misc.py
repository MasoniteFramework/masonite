def dot(data, compile_to=None):
    notation_list = data.split('.')

    compiling = ""
    compiling += notation_list[0]
    beginning_string = compile_to.split('{1}')[0]
    compiling = beginning_string + compiling
    dot_split = compile_to.replace(beginning_string + '{1}', '').split('{.}')
    if any(len(x) > 1 for x in dot_split):
        raise ValueError("Cannot have multiple values between {1} and {.}")

    for notation in notation_list[1:]:
        compiling += dot_split[0]
        compiling += notation
        compiling += dot_split[1]
    return compiling
