import sys
from hymn_data import HymnData

class MarkdownEmitter(object):
    def open(self, filename):
        self.file = open(filename, "w")

    def emit_category(self, category):
        self.file.write("\n## %s\n\n" % category)

    def emit_header(self, num, meter, author):
        if author == "":
            self.file.write("**%s**. (%s)  \n" %
                            (num, meter))
        else:
            self.file.write("**%s**. (%s) **%s**  \n" %
                            (num, meter, author))

    def emit_stanza(self, stanza):
        self.file.write("%s %s  \n" % (stanza.num, stanza[0]))
        for line in stanza[1:]:
            self.file.write("%s  \n" % line)
        self.file.write("\n")

    def finalize(self):
        self.file.close()

class HymnalFormatter(object):
    def __init__(self, db, emitter):
        self.hymns = HymnData(db).load_hymns()
        self.emitter = emitter
    def format(self, filename):
        self.emitter.open(filename)

        category = ""

        for hymn in self.hymns:
            if hymn.category != category:
                category = hymn.category
                self.emitter.emit_category(category)
            
            self.emitter.emit_header(hymn.num,
                                     hymn.meter,
                                     hymn.author)

            for stanza in hymn.stanzas:
                self.emitter.emit_stanza(stanza)

        self.emitter.finalize()

if __name__ == "__main__":
    db, out = sys.argv[1:]
    hf = HymnalFormatter(db,
                         MarkdownEmitter())
    hf.format(out)
