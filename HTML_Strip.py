import html.parser
import io
import re

path_in = r'C:\Users\Nate\Desktop\20240229_10-K_edgar_data_100517_0000100517-24-000027_1.txt'
path_out = r'C:\Users\Nate\Desktop\cleaned_text.txt'


class HTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return ''.join(self.result)


def html_to_text(html):
    """Converts HTML to plain text (stripping tags and converting entities)."""
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


html_text =  open(path_in, 'r', encoding='utf-8').read()



plain_text = html_to_text(cleaned_html)
print(repr(plain_text))

with open(path_out, 'w', encoding='utf-8') as output_file:
    output_file.write(plain_text)