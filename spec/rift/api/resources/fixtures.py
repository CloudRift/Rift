from specter import Spec, fixture
from webtest import TestApp

import rift.data.handler
import rift.data.adapters.mongodb

@fixture
class MockedDatabase(Spec):

    def before_each(self):
        # reset the mocked DB to clear out any data it has
        rift.data.handler._db_handler = rift.data.adapters.mongodb.MongoDB()
        rift.data.handler._db_handler.connect()
        self.app = TestApp(rift.app.application)
