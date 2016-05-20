import sys
from hymn_data import HymnData

from MarkdownEmitter import MarkdownEmitter
from LatexEmitter import LatexEmitter
from HtmlEmitter import HtmlEmitter

emitters = {"latex": LatexEmitter,
            "markdown": MarkdownEmitter,
            "html": HtmlEmitter}
        
class HymnalFormatter(object):
    def __init__(self, db, emitter):
        hd = HymnData(db)
        self.title, self.author, self.date = hd.hymnal_info()
        self.hymns = hd.load_hymns()
        self.emitter = emitter
    def format(self, filename):
        
        self.emitter.initialize(filename,
                                self.title,
                                self.author,
                                self.date)

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

            self.emitter.emit_footer()
            
        self.emitter.finalize()

if __name__ == "__main__":
    fmt, db, out = sys.argv[1:]
    hf = HymnalFormatter(db,
                         emitters[fmt]())
    hf.format(out)
