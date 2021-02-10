from sudachipy import tokenizer
from sudachipy import dictionary
import markovify
import re
from glob import iglob


def load_from_file():

    # read text
    text = ""
    files_pattern = './src/hoge.txt'
    for path in iglob(files_pattern):
        with open(path, 'r', encoding='utf-8') as f:
            text += f.read().strip()

    # delete some symbols
    unwanted_chars = ['\r', '\u3000', '-', '｜']
    for uc in unwanted_chars:
        text = text.replace(uc, '')

    # delete aozora bunko notations
    unwanted_patterns = [re.compile(r'《.*》'), re.compile(r'［＃.*］')]
    for up in unwanted_patterns:
        text = re.sub(up, '', text)

    return text


def split_for_markovify(text):

    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.A

    _splitted_text = ""

    breaking_chars = [
        '(',
        ')',
        '[',
        ']',
        '"',
        "'",
        '（',
        '）',
        '「',
        '」',
    ]

    _words = [m.surface() for m in tokenizer_obj.tokenize(text, mode)]

    # split whole text to sentences by newline, and split sentence to words by space.
    for word in _words:

        try:
            if word not in breaking_chars:
                _splitted_text += ' ' + word    # skip if node is markovify breaking char

            if word == '、':
                _splitted_text += ' '    # split words by space

            if word == '。':
                _splitted_text += '\n'    # reresent sentence by newline
        except UnicodeDecodeError as e:
            # sometimes error occurs
            print(word)
            print(e)
        finally:
            pass

    return _splitted_text


input_text = load_from_file()

splitted_text = split_for_markovify(input_text)

text_model = markovify.Text(splitted_text)

for i in range(5):
    print(text_model.make_sentence())
