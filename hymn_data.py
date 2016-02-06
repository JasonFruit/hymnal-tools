from sqlite3 import connect
from hymn import Stanza, Hymn, sortable

# SQL statements for various kinds of activity

get_meter = "select id from meter where description = ?"
add_meter = "insert into meter (description) values (?)"

get_author = "select id from author where name = ?"
add_author = "insert into author (name) values (?)"

get_category = "select id from category where name = ?"
add_category = "insert into category (name) values (?)"

get_max_hymn_num = "select max(num) from hymn"

get_hymn_id = "select id from hymn where num = ?"

delete_lines = "delete from line where hymn_id = ?"
delete_hymn = "delete from hymn where id = ?"

add_hymn = """
insert into hymn (
    num,
    meter_id,
    author_id,
    category_id
) values (
    ?, ?, ?, ?
)"""

add_line = """insert into line (hymn_id, stanza_num, ordinal, content, sortable)
values
(?, ?, ?, ?, ?)"""

get_hymn = """
select h.id,
num,
m.description as meter,
a.name as author,
c.name as category,
auth
from hymn h
inner join meter m
on h.meter_id = m.id
inner join author a
on h.author_id = a.id
inner join category c
on h.category_id = c.id
where num = ?
"""

get_lines = """
select stanza_num,
content
from line
where hymn_id in (select id from hymn where num = ?)
order by stanza_num, ordinal
"""


class HymnData(object):
    """Saves and loads hymns from the database.  Also cleans up unused
    values from lookup tables.
    """
    def __init__(self, db):
        self.conn = connect(db)
        self.cur = self.conn.cursor()

    def _id_maybe_add(self, get_sql, add_sql, params=list()):
        """Attempts to select the id for the given value in a lookup table.
        If no id is found, adds a new row and returns its id.
        """
        try:
            self.cur.execute(get_sql, params)
            return self.cur.fetchone()[0]
        except:
            self.cur.execute(add_sql, params)
            return self.cur.lastrowid
    def _meter_id_maybe_add(self, meter):
        return self._id_maybe_add(get_meter, add_meter, (meter,))
    def _author_id_maybe_add(self, name):
        return self._id_maybe_add(get_author, add_author, (name,))
    def _category_id_maybe_add(self, name):
        return self._id_maybe_add(get_category, add_category, (name,))
    def max_hymn_num(self):
        self.cur.execute(get_max_hymn_num)
        num = self.cur.fetchone()[0]
        if num:
            return num
        return 0
    def clean_up(self):
        """Removes unused values from lookup tables (called after deleting a
        hymn).

        """
        cleaning_sqls = ["delete from meter where id not in (select meter_id from hymn)",
                         "delete from author where id not in (select author_id from hymn)",
                         "delete from category where id not in (select category_id from hymn)"]
        for sql in cleaning_sqls:
            self.cur.execute(sql)
        self.conn.commit()
    def _delete_hymn(self, id):
        self.cur.execute(delete_lines, (id,))
        self.cur.execute(delete_hymn, (id,))
    def delete_hymn(self, id):
        self._delete_hymn(id)
        self.clean_up()
    def _update_hymn(self, hymn):
        self.cur.execute(get_hymn_id, (hymn.num,))
        id = self.cur.fetchone()[0]
        self._delete_hymn(id)
        self._add_hymn(hymn)
    def _add_hymn(self, hymn):
        self.cur.execute(add_hymn, (hymn.num,
                               self._meter_id_maybe_add(hymn.meter),
                               self._author_id_maybe_add(hymn.author),
                               self._category_id_maybe_add(hymn.category)))
        id = self.cur.lastrowid
        for stanza in hymn.stanzas:
            ord = 0
            for line in stanza:
                self.cur.execute(add_line,
                            (id, stanza.num, ord, line, sortable(line)))
                ord += 1
        self.conn.commit()
        return id
    def save_hymn(self, hymn):
        """Saves a hymn to the database.  If there is no hymn number (hymn.num
        == 0), adds a new record; otherwise deletes the old one and
        adds a new.  Returns hymn.id.
        """
        if hymn.num == 0:
            hymn.num = self.max_hymn_num() + 1
            return self._add_hymn(hymn)
        else:
            return self._update_hymn(hymn)

    def load_hymn(self, num):
        """Retrieves a hymn from the database.
        """
        self.cur.execute(get_hymn, (num,))
        row = self.cur.fetchone()

        out = Hymn(row[2], row[3], row[5], row[4], row[1])

        self.cur.execute(get_lines, (num,))
        line_rows = self.cur.fetchall()

        last_snum = 0
        stanza = None
        
        for row in line_rows:
            cur_snum, content = row
            if cur_snum != last_snum:
                if stanza:
                    out.stanzas.append(stanza)
                stanza = Stanza(cur_snum)
                last_snum = cur_snum
            stanza.append(content)

        out.stanzas.append(stanza)

        return out
