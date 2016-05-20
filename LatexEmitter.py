class LatexEmitter(object):
    def emit(self, s):
        self.file.write(s)
        
    def initialize(self, filename, title, author, date):
        self.file = open(filename, "w")

        self.emit(r"""\documentclass{book}

\usepackage{verse}
\title{%s}
\author{%s}
\date{%s}

\begin{document}

\maketitle
\tableofcontents

""" % (title, author, date))

    def emit_category(self, category):
        self.emit("\\chapter{%s}\n\n" % category)

    def emit_header(self, num, meter, author):
        self.current_meter = meter
        self.emit(r"""\vspace{1em}\textbf{%s}. (%s) \textit{%s}

""" % (num, meter, author))
        self.emit("\\begin{verse}\n")

    def emit_stanza(self, stanza):
        self.emit("\\begin{altverse}\n")
        self.emit("\\flagverse{%s} " % stanza.num)
        for line in stanza:
            self.emit("%s\\\\\n" % line)
        self.emit("\\end{altverse}\n\\vspace{0.4em}\n\n")

    def emit_footer(self):
        self.emit("\\end{verse}\n\n")
        
    def finalize(self):
        self.emit("\\end{document}\n")
