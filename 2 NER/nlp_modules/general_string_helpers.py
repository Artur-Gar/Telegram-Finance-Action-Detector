def replace_several_substrs(s: str, symbols_to_remove: list = [r"'", r'"', r'«', r'»'])-> str:
    """
    The function cleans the string s by removing unnecessary characters listed in symbols_to_remove — by default, various types of quotation marks
    """
    for symbol in symbols_to_remove:
        s =  s.replace(symbol, '')
    return s