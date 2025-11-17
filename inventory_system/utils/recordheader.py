class RecordHeader:
    def __init__(self, title, fields=None, link=None):
        self.title = title
        self.fields = fields or {}
        self.link = link

    def items(self):
        return self.fields.items()
