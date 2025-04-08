def replace_several_substrs(s: str, symbols_to_remove: list = [r"'", r'"', r'«', r'»'])-> str:
    """
    Функция очищает строку s от ненужных символов в symbols_to_remove - по дефолту - всевозможных кавычек. 
    """
    for symbol in symbols_to_remove:
        s =  s.replace(symbol, '')
    return s