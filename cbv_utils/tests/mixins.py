import random
from ._utils import TestCase

from ..mixins import context_mixin_factory


class context_mixin_factoryTestCase(TestCase):
    def test_returns_a_class(self):
        foo = context_mixin_factory()
        self.assertEqual(type(foo), type)

    def test_class_adds_dict_to_get_context_data(self):
        r = random.randint(100, 200)
        foo = context_mixin_factory({"random": r})
        self.assertEqual(r, foo().get_context_data()["random"])

    def test_dispatches_to_other_classes(self):
        r = random.randint(100, 200)
        Mixin = context_mixin_factory({"random": r})

        class MyMixin(Mixin):
            def get_context_data(self):
                c = super(MyMixin, self).get_context_data()
                c.update({"double_random": r * 2})
                return c

        context = MyMixin().get_context_data()
        self.assertEqual(r * 2, context["double_random"])
        self.assertEqual(r, context["random"])

    def test_can_be_combined_with_other_mixins(self):
        r = random.randint(100, 200)
        MixinOne = context_mixin_factory({"one": r})
        MixinTwo = context_mixin_factory({"two": r * 2})

        class MyView(MixinOne, MixinTwo):
            pass

        context = MyView().get_context_data()
        self.assertEqual(r, context["one"])
        self.assertEqual(r * 2, context["two"])

    def test_can_take_a_callable(self):
        def counter_factory():
            class Counter(object):
                counter = 0

                def inner(self):
                    self.counter += 1
                    return {"counter": self.counter}
            return Counter().inner

        mixin = context_mixin_factory(callback=counter_factory())()
        self.assertEqual(1, mixin.get_context_data()["counter"])
        self.assertEqual(2, mixin.get_context_data()["counter"])

    def test_infers_context_variable_name_from_callback(self):
        from datetime import datetime
        mixin = context_mixin_factory(callback=datetime.now)()
        self.assertTrue("now" in mixin.get_context_data())

    def test_can_handle_lambdas_as_callbacks(self):
        from datetime import datetime
        callback = lambda: datetime.now()
        mixin = context_mixin_factory(callback=callback)()
        self.assertTrue("<lambda>" in mixin.get_context_data())

    def test_kwargs_are_passed_along(self):
        class MyMixin(object):
            def get_context_data(self, **kwargs):
                return kwargs

        GeneratedMixin = context_mixin_factory({"foo": "bar"})

        class MyView(GeneratedMixin, MyMixin):
            pass

        view = MyView()
        self.assertTrue("baz" in view.get_context_data(baz=123))
