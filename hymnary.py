from __future__ import print_function

import urllib.request
import urllib.parse
import json
import codecs
from hymn import Stanza, Hymn

class Hymnary(object):

    def __init__(self):
        pass
    
    def __get_search_url(self, query):
        escaped = urllib.parse.quote(query, "")
        return "http://www.hymnary.org/all?qu=%s&export=json" % escaped

    def search(self, query):
        url = self.__get_search_url(query)
        response = urllib.request.urlopen(url)
        json_text = response.read().decode("utf-8")
        data = json.loads(json_text)
        return [{"first_line": text["firstLine"],
                 "auth": text["textAuthNumber"],
                 "meter": text["meter"],
                 "authors": text["authors"]}
                for text in data["text"]["matches"]]

    def _text_to_hymn(self, author, meter, auth, res):
        text = res["text"].strip()
        
        stanzas_texts = [stanza.strip()
                         for stanza
                         in text.split("\n\r\n\n")]
        out = Hymn(meter,
                   author,
                   auth,
                   "")

        st_num = 1
        
        for st in stanzas_texts:
            stanza = Stanza(st_num,
                            [line.strip().lstrip("1234567890. ")
                             for line in st.split("\n\r\n")])
            out.stanzas.append(stanza)
            st_num += 1

        return out
                      
    def get_full_texts(self, search_result):
        auth = search_result["auth"]
        url = 'http://www.hymnary.org/api/fulltext/' + urllib.parse.quote(auth, "")
        response = urllib.request.urlopen(url)
        json_text = response.read().decode("utf-8")
        texts = json.loads(json_text)

        if len(texts) == 0:
            return [("Add new",
                     Hymn(search_result["meter"],
                          search_result["authors"],
                          auth,
                          "")),
                    ("Abandon", None)]
        
        return [(text["title"],
                 self._text_to_hymn(search_result["authors"],
                                    search_result["meter"],
                                    auth,
                                    text))
                for text in texts]

if __name__ == "__main__":
    fl = input("First line: ")
    hymnary = Hymnary()
    results =  hymnary.search(fl)
    auth = results[0]["auth"]
    print(hymnary.get_full_texts(auth)[0]["text"])
