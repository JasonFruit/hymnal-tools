class MarkdownEmitter(object):
    def initialize(self, filename, title, author, date):
        self.file = open(filename, "w")

        self.file.write(title)
        self.file.write("\n======================================================================\n\n")

        self.file.write("## %s (%s) ##" % (author, date))

    def emit_category(self, category):
        self.file.write("\n## %s\n\n" % category)

    def emit_header(self, num, meter, author):
        if author == "":
            self.file.write("**%s**. (%s)  \n" %
                            (num, meter))
        else:
            self.file.write("**%s**. (%s) _%s_  \n" %
                            (num, meter, author))

    def emit_footer(self):
        pass
    
    def emit_stanza(self, stanza):
        self.file.write("%s %s  \n" % (stanza.num, stanza[0]))
        for line in stanza[1:]:
            self.file.write("%s  \n" % line)
        self.file.write("\n")

    def finalize(self):
        self.file.close()
