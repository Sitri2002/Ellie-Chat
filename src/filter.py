import emoji

def filter(input):
    input = encoder(input)
    input = emoji_filter(input)
    return input

def encoder(input):
    return input

def emoji_filter(input):
    input = emoji.replace_emoji(input, replace= "")
    return input

def xml_filter(input):
    input = input.replace("&", "&amp;")
    input = input.replace("<", "&lt;")
    input = input.replace(">", "&gt;")
    input = input.replace("\"", "&quot")