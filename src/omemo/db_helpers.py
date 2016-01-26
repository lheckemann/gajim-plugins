
def table_exists(db, name):
    """ Check if the specified table exists in the db. """

    q = """ SELECT name FROM sqlite_master
            WHERE type='table' AND name=?;
        """
    return db.execute(q, (name, )).fetchone() is not None


def user_version(db):
    """ Return the value of PRAGMA user_version. """
    return db.execute('PRAGMA user_version').fetchone()[0]
