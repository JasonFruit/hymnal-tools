from __future__ import print_function

import os, sys, uuid
from hymn import hymn_from_string
from hymnary import Hymnary
from menu import ConsoleMenu
from hymn_data import HymnData

db = sys.argv[1]
hymn_data = HymnData(db)

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
    
    if len(texts) != 0:

        menu = ConsoleMenu(texts)
        hymn = menu.show()

        with open(fn, "w") as f:
            f.write(str(hymn))

    else:

        print("No full texts.")

        with open(fn, "w") as f:
            f.write("0. ([meter]) [author]\n[hymn text]")

    os.system('emacsclient -a "emacs" %s' % fn)
    hymn = hymn_from_string(open(fn, "r").read())

    print(hymn)

    if input("Save (Y/N)? ").lower() == "y":
        hymn_data.save_hymn(hymn)
        print("Saved as #%s." % hymn.num)
    else:
        print("Not saved.")
        
