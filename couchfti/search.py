"""
Index/search facility for CouchDB.
"""

import logging
import os.path
import xapian
import xappy

from query import tokenize


log = logging.getLogger()


class Searcher(object):
    """
    Search a set of indexes for matching documents.
    """

    def __init__(self, db, path, indexes):
        self.__db = db
        self.__path = path
        self.__indexes = indexes

    def search_docs(self, index, query, skip, max):
        rows = self.db.view('_all_docs', include_docs=True,
                            keys=self.search_docids(index, query, skip, max))
        return [row.doc for row in rows]

    def search_docids(self, index, query, skip, max):
        return [r.id for r in self.search(index, query, skip, max)]

    def search(self, index, query, skip, max):
        config = self.__indexes[index]
        try:
            conn = xappy.SearchConnection(os.path.join(self.__path, config['path']))
        except xapian.DatabaseOpeningError, e:
            log.error(e)
            return None
        try:
            # Tokenize the query
            q = list(tokenize(query))
            # Build a phrase and a list of attrs
            terms = [i[1].encode('utf-8') for i in q if i[0] == 'term']
            attrs = [i[1] for i in q if i[0] == 'field']
            order = ([i[1] for i in q if i[0] == 'order'] or [None])[0]
            # Build a xapian query.
            query = conn.query_all()
            for term in terms:
                query = xapian.Query(xapian.Query.OP_AND, query, xapian.Query(term.lower()))
            for field, op, value in attrs:
                func = QUERY_FACTORIES[op]
                query = xapian.Query(xapian.Query.OP_AND, query, func(conn, field, value))
            if not order:
                sortby = None
            else:
                sortby = '-+'[order[1]] + order[0]
            # Run and return the query.
            return conn.search(query, skip, skip+max, sortby=sortby)
        finally:
            conn.close()


def query_eq(conn, field, value):
    return conn.query_field(field, value)


def query_prefix(conn, field, value):
    return _query_range(conn, field, value, value+u'\u9999')


def query_gteq(conn, field, value):
    return _query_range(conn, field, value, None)


def query_lteq(conn, field, value):
    return _query_range(conn, field, None, value)


def _query_range(conn, field, begin, end):
    return conn.query_range(field, begin, end)


QUERY_FACTORIES = {'=': query_eq,
                   '=*': query_prefix,
                   '>=': query_gteq,
                   '<=': query_lteq}

