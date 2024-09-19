"""# Model ID base for SQLAlchemy models"""

from sqlalchemy.inspection import inspect


class ModelIdBase():
    """
    A base for SQLAlchemy models with a `model_id` property. The `model_id` is
    similar to a primary key, but prefixed by the model type. This 
    distinguishes it from other objects with the same primary key value 
    belonging to other tables.

    Attributes
    ----------
    model_id : str
    """
    @property
    def model_id(self):
        """ID for distinguishing models"""
        id = inspect(self).identity
        id = '-'.join([str(key) for key in id]) if id is not None else ''
        return type(self).__tablename__+'-'+str(id)