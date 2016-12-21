import os
import unittest
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class TestDatabaseFunctionality(unittest.TestCase):
    '''
    This Class is simply used to test that a database
    created and removed using the os function does
    not persist in the file system. It also enables us test
    the action of first removing a database before creating
    it. Pretty COOL!
    '''

    def test_database_is_removed_if_exists(self):
        '''
        This test first creates a test_amity_exists.db file
        and proceeds to remove it. After removing,
        assert that the file does not exist using the os.path.exits
        file command that ties to the os.path.aA

        '''
        db_name = "test_amity_exists.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///' + db_name)
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)
        if os.path.exists(db_name):
            os.remove(db_name)
        self.assertFalse(os.path.exists(db_name))