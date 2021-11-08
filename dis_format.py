def get_italic(string: str) -> str:
    return "*{0}*".format(string)


def get_bold(string: str) -> str:
    return "**{0}**".format(string)


def get_underline(string: str) -> str:
    return "__{0}__".format(string)


def get_strikethrough(string: str) -> str:
    return "~~{0}~~".format(string)


def get_code_block(string: str) -> str:
    return "`{0}`".format(string)
