import re

class Stanza(list):
    def __init__(self, num, lines=list()):
        list.__init__(self, lines)
        self.num = num
    def __repr__(self):
        return "%s %s" % (self.num,
                          "\n".join(self))

class Hymn(object):
    def __init__(self,
                 meter,
                 author,
                 auth="",
                 category="",
                 num=0):
        self.meter = meter
        self.author = author
        self.auth = auth
        self.category = category
        self.num = num
        self.stanzas = []
    def __repr__(self):
        header = "%s. (%s) %s" % (self.num,
                                  self.meter,
                                  self.author)
        text = "\n\n".join(
            [str(stanza)
             for stanza in self.stanzas])
        return header + "\n" + text

def sortable(line):
    return "".join(
        [c for c in line.lower()
         if c in "abcdefghijklmnopqrstuvwxyz "])

def hymn_from_string(s):
    s = s.strip()
    header_rgx = re.compile("([0-9]+)\. \(([^(]+)\) (.*)")
    lines = s.split("\n")
    header = lines[0].strip()
    try:
        num, meter, author = header_rgx.findall(header)[0]
    except (IndexError, ValueError):
        num, meter = re.compile("([0-9]+)\. \(([^(]+)\)").findall(header)[0]
        author = ""
    num = int(num)

    hymn = Hymn(meter, author, num=num)
    lines = map(lambda s: s.lstrip("\r\n\t0123456789. ").rstrip(),
                lines[1:])

    text = "\n".join(lines)
    
    stanza_texts = text.split("\n\n")
    snum = 1
    for st in stanza_texts:
        slines = st.split("\n")
        hymn.stanzas.append(Stanza(snum, slines))
        snum += 1

    return hymn
