def snake2camel(string : str):
    words = string.split("_")
    if len(words)>1:
        return words[0]+"".join([word[0].upper()+word[1:] for word in words[1:]])
    return string

def snake2pascal(string: str):
    words = string.split("_")
    return "".join([word[0].upper()+word[1:] for word in words])


def syntax_error():
    print("Syntax error")
    exit(1)