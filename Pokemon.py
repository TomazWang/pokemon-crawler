class Pokemon:
    def __init__(self, id, name_zh, name_en):
        self.id = id
        self.name_zh = name_zh
        self.name_en = name_en
        self.link = ''
        self.pic_link = ''
        self.pic_name = ''
        self.generation = 0

    def __str__(self):
        return '#{} {}'.format(self.id, self.name_zh)
