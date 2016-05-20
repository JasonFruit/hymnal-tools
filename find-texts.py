from __future__ import print_function

import os, sys, uuid
from hymn import hymn_from_string
from hymnary import Hymnary
from menu import ConsoleMenu
from hymn_data import HymnData

db = sys.argv[1]
hymn_data = HymnData(db)

try:
    title, author, date = hymn_data.hymnal_info()
    print(title)
    print("%s (%s)" % (author, date))
except (IndexError, TypeError):
    title, author, date = (input("Title: "),
                           input("Author: "),
                           input("Year: "))
    hymn_data.cur.execute("insert into info (title, author, year) values (?, ?, ?)",
                          (title, author, date))
    hymn_data.cur.connection.commit()

print("Last hymn entered: #%s." % hymn_data.max_hymn_num())

hymnary = Hymnary()

while True:
    first_line = input("First line: ")
    
    auths = hymnary.search(first_line)

    if len(auths) == 0:
        print("No matches.")
        continue
    else:
        menu = ConsoleMenu([[auth["first_line"], auth]
                            for auth in auths])

    hymn = menu.show()

    texts = hymnary.get_full_texts(hymn)

    fn = "tmp/%s.txt" % uuid.uuid4()
    
    menu = ConsoleMenu(texts)
    hymn = menu.show()

    if not hymn:
        continue
    
    with open(fn, "w") as f:
        f.write(str(hymn))

    os.system('emacsclient -a "emacs" %s' % fn)
    hymn = hymn_from_string(open(fn, "r").read())

    print(hymn)

    if input("Save (Y/N)? ").lower() == "y":
        hymn_data.save_hymn(hymn)
        print("Saved as #%s." % hymn.num)
    else:
        print("Not saved.")
        
