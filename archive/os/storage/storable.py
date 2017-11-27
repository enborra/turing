import rethinkdb as r


class Storable(object):
    _database_name = None
    _connection = None


    def __init__(self, database_name):
        self._database_name = database_name
        self._connection = r.connect('localhost', 28015)

    def get(self, table_name, filter):
        return r.db(self._database_name).table(table_name).filter(filter).run(self._connection)

    def upsert(self, table_name, doc_obj):
        obj_count = r.db(self._database_name).table(table_name).filter({'key': doc_obj['key']}).count().run(self._connection)

        if obj_count == 0:
            r.db(self._database_name).table(table_name).insert(doc_obj).run(self._connection)
        else:
            r.db(self._database_name).table(table_name).filter({'key': doc_obj['key']}).update(doc_obj).run(self._connection)
