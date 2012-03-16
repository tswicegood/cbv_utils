def context_mixin_factory(context=None, callback=None):
    """
    Returns a class that can be used as mixin to add context data.

    You can use this to create simple class-based-view mixins that
    add context data to a given view.  You can provide a ``context``
    dict, a ``callback`` function, or both.

    For example, here's how you would create a simple mixin that
    adds a ``foo`` variable to the context data:

    >>> from cbv_utils.mixins import context_mixin_factory
    >>> Mixin = context_mixin_factory({"foo": "bar"})
    >>> Mixin().get_context_data()
    {'foo': 'bar'}

    You can defer calculation until the time ``get_context_data``
    is called with a ``callback`` like this:

    >>> from datetime import datetime
    >>> def current_time():
    ...     return {"now": datetime.now()}
    ...
    >>> CurrentTimeMixin = context_mixin_factory(callback=current_time)
    >>> CurrentTimeMixin().get_context_data()
    {'now': datetime.datetime(2012, 3, 16, 15, 32, 4, 953354)}
    >>> CurrentTimeMixin().get_context_data()
    {'now': datetime.datetime(2012, 3, 16, 15, 32, 7, 441365)}

    You don't *have* to return a dict data type.  This code attempts
    to infer the name of the context variable based on name of the
    function (``callback.__name__`` to be exact).  The above code can
    be written out like this:

    >>> CurrentTimeMixin = context_mixin_factory(callback=datetime.now)
    >>> CurrentTimeMixin().get_context_data()
    {'now': datetime.datetime(2012, 3, 16, 15, 39, 39, 3415)}
    >>> CurrentTimeMixin().get_context_data()
    {'now': datetime.datetime(2012, 3, 16, 15, 39, 40, 427489)}
    """
    if not context:
        context = {}
    if not callback:
        callback = lambda: {}

    class Mixin(object):
        def get_context_data(self, **kwargs):
            try:
                c = super(Mixin, self).get_context_data(**kwargs)
            except AttributeError:
                c = {}
            c.update(context)
            try:
                callback_result = callback()
                c.update(callback_result)
            except TypeError:
                c.update({callback.__name__: callback_result})
            return c

    return Mixin
