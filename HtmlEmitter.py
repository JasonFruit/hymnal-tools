class HtmlEmitter(object):
    def emit(self, s):
        self.file.write(s)
        
    def emit_line(self, s=""):
        self.emit(s)
        self.emit("\n")
        
    def initialize(self, filename, title, author, date):
        self.file = open(filename, "w")
        self.emit_line("""<html>
<head>
    <link rel="stylesheet" type="text/css" href="hymnal.css" />
    <meta charset="utf-8" />
    <title>%s, %s</title>
</head>
<body>""" % (title, author))
        self.emit_line("""<h1 class="hymnal_title">%s</h1>""" % title)
        self.emit_line("""<h2 class="hymnal_subtitle">%s (%s)</h2>""" % (author, date))

    def emit_category(self, category):
        self.emit_line("""<h3 class="category">%s</h3>""" % category)

    def emit_header(self, num, meter, author):
        self.emit_line("""<div class="hymn">""")
        if author == "":
            self.emit_line(
                """<span class="hymn_num">%s</span>. (<span class="meter">%s</span>)<br />""" %
                (num, meter))
        else:
            self.emit_line(
                """<span class="hymn_num">%s</span>. (<span class="meter">%s</span>) <span class="author">%s</span><br />""" %
                            (num, meter, author))

    def emit_footer(self):
        self.emit_line("</div>")
    
    def emit_stanza(self, stanza):
        self.emit_line("""<div class="stanza">""")
        self.emit("""<span class="stanza_num">%s</span>""" % stanza.num)
        for line in stanza:
            self.emit_line("%s<br />" % line)
        self.emit_line("</div>")

    def finalize(self):
        self.emit_line("""</body>
</html>""")
        self.file.close()
