class CSVParser(object):
    """docstring for CSVParser"""
    def __init__(self, filename):
        super(CSVParser, self).__init__()
        self.filename = filename

    def parse(self):
        with open(self.filename, 'r') as f:
            self.columnnames = f.readline().strip().split(';')
            self.itemsList = f.read().splitlines()
            for i in range(len(self.itemsList)):
                self.itemsList[i] = map(lambda s: "NULL" if s == "None" else s, self.itemsList[i].split(";"))
        return self.columnnames, self.itemsList

    def __str__(self):
        string = ""
        for element in self.columnnames:
            string += element
            string += " | "
        string += "\n"
        for item in self.itemsList:
            for subelement in item:
                string += subelement
                string += " | "
            string += "\n"
        return string


def main():
    parser = CSVParser("../data/stations.csv")
    parser.parse()
    print(parser)

if __name__ == '__main__':
    main()
