class ShanghaimetroDatabaseRouter(object):
    """
    Database router for the mobike database in mobike application
    """
    app_label = "shanghaimetro"
    db_label = "shanghaimetro_db"

    def db_for_read(self, model, **hints):
        """Send all read operations on mobike app models to "mobike_db"."""
        if model._meta.app_label == self.app_label:
            return self.db_label
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on mobike app models to `mobike_db`."""
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            # Allow any relation between two models that are both in the mobike app.
            return True
        elif self.app_label not in [obj1._meta.app_label, obj2._meta.app_label]:
            # No opinion if neither object is in the mobike app (defer to default or other routers).
            return None
        # Block relationship if one object is in the mobike app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            # The current app should be migrated only on the current database.
            return db == self.db_label
        if db == self.db_label:
            # Ensure that all other apps don't get migrated on the current database.
            return False
        # No opinion for all other scenarios
        return None
