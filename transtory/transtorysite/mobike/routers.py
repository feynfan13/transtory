class MobikeDatabaseRouter(object):
    """
    Database router for the mobike database in mobike application
    """
    def db_for_read(self, model, **hints):
        """Send all read operations on mobike app models to "mobike_db"."""
        if model._meta.app_label == 'mobike':
            return 'mobike_db'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on mobike app models to `mobike_db`."""
        if model._meta.app_label == 'mobike':
            return 'mobike_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""
        if obj1._meta.app_label == "mobike" or obj2._meta.app_label == "mobike":
            # Allow any relation between two models that are both in the mobike app.
            return True
        elif 'mobike' not in [obj1._meta.app_label, obj2._meta.app_label]:
            # No opinion if neither object is in the mobike app (defer to default or other routers).
            return None
        # Block relationship if one object is in the mobike app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "mobike":
            # The Example app should be migrated only on the example_db database.
            return db == "mobike_db"
        if db == "mobike_db":
            # Ensure that all other apps don't get migrated on the example_db database.
            return False
        # No opinion for all other scenarios
        return None
