

    # Parses the page's content:
    # 0) First check that we are exploring new content
    # 1) Add any new vocab words to the vocab mapping
    # 2) For this document, counts number of occurrences for each vocab word
    # 3) Update co-occurrence matrix
from html.parser import HTMLParser

class Parser(HTMLParser):

    def __init__(self) -> None:
        super().__init__()
        self.links = []
        self.is_text = False
        self.is_content_body = False
        self.open_div_count = 1
        self.BODY_CONTENT_ID = 'bodyContent'
        self.mega_string = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if self.is_content_body:
                self.open_div_count += 1
            elif attrs[0][1] == self.BODY_CONTENT_ID:
                self.is_content_body = True
        # If we are reading the content body, look for <p> and <a>
        elif self.is_content_body:
            if tag == 'p':
                # print('--- FOUND TEXT ---')
                self.is_text = True
            elif tag == 'a' and attrs[0][1][0:6] == '/wiki/':
                self.links.append(attrs[0][1])
                return
        
    def handle_data(self, data):
        if self.is_text:
            self.mega_string += f'\n{data}'
            return

    def handle_endtag(self, tag):
        if tag == 'div' and self.is_content_body:
            print(self.open_div_count)
            self.open_div_count -= 1
            if self.open_div_count == 0:
                self.is_content_body = False
        elif tag == 'p':
            # print('--- FOUND TEXT ---')
            self.is_text = False