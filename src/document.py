
# Container for a document
class Document(object):
    
    def __init__(self):
        self.url = None
        self.links = []
        self.content = ""
        
    # Append plaintext to document content
    def write(self, content):
        self.content += f" {content}"
    
    # Set the unique identifying URL for this document
    def set_url(self, url):
        self.url = url
    
    # Add links found in this document's references
    def append_link(self, link):
        self.links.append(link)
        
    
        
    