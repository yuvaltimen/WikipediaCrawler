# Document container


class Document():
    
    def __init__(self):
        self.url = None
        self.links = []
        self.content = ""
        
    def write(self, content):
        self.content += f"{content}\n"
        
    def set_url(self, url):
        self.url = url
    
    
    def append_link(self, link):
        self.links.append(link)
        
    # # Empty = False
    # def __bool__(self):
    #     return self.url or self.links or self.content
        
    