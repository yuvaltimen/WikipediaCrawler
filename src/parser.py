from html.parser import HTMLParser
from utils import clean_data
from document import Document

# Class for parsing HTML content
# Subclasses from built-in Python HTMLParser
class Parser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.is_text = False  # If current iteration is text or not
        self.is_content_body = False  # If current iteration is the body we are looking for
        self.open_div_count = 1  # Represents number of open div tags since reaching the bodyContent
        self.BODY_CONTENT_ID = 'bodyContent'  # Represents the bodyContent tag
        self.prefix = "https://en.wikipedia.org"
        self.doc = Document()
    
    # Method called when start tag is encountered
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if self.is_content_body:
                self.open_div_count += 1
            elif attrs[0][1] == self.BODY_CONTENT_ID:
                self.is_content_body = True
        # If we are reading the content body, look for <p> and <a>
        elif self.is_content_body:
            if tag == 'p':
                # --- FOUND TEXT ---
                self.is_text = True
            elif tag == 'a':
                # --- FOUND LINK ---
                candidate = attrs[0][1]
                # If it's a wiki link, store the full URL
                if candidate[:6] == "/wiki/":
                    candidate = self.prefix + candidate
                    self.doc.append_link(candidate)
    
    # Method called on data in between two tags
    def handle_data(self, data):
        if self.is_text:
            self.doc.write(clean_data(data))
    
    # Method called when end tag is encountered
    def handle_endtag(self, tag):
        if tag == 'div' and self.is_content_body:
            self.open_div_count -= 1
            if self.open_div_count == 0:
                self.is_content_body = False
        elif tag == 'p':
            # --- FOUND TEXT ---
            self.is_text = False
    
    # Returns a Document object representing a
    def get_document(self):
        return self.doc
