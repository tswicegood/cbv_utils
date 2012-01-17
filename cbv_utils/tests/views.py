from ._utils import TestCase

from .. import views


class DummyObject(object):
    def __init__(self, *args, **kwargs):
        pass


class TestableForm(DummyObject):
    pass


class CustomForm(DummyObject):
    pass


class TestableInlineFormset(DummyObject):
    pass


class CustomFormset(DummyObject):
    pass


class FormMixinTestCase(TestCase):
    mixin_class = views.FormMixin

    def get_testable_mixin(self):
        mixin = self.mixin_class()
        mixin.form_class = TestableForm
        mixin.request = self.factory.get("/any/url/works")
        return mixin

    def test_get_context_data_adds_default_form(self):
        context_data = self.get_testable_mixin().get_context_data()
        self.assertTrue("form" in context_data)
        self.assertEqual(context_data["form"].__class__, TestableForm)

    def test_get_context_data_uses_provided_form_if_available(self):
        context_data = self.get_testable_mixin().get_context_data(
                form=CustomForm())
        self.assertEqual(context_data["form"].__class__, CustomForm)

    def test_get_form_class_returns_form_class_property(self):
        mixin = self.get_testable_mixin()
        self.assertFalse(mixin.get_form_class() is None, msg="Sanity check")
        self.assertEqual(mixin.form_class, mixin.get_form_class())

    def test_get_form_uses_form_class_by_default(self):
        form = self.get_testable_mixin().get_form()
        self.assertEqual(form.__class__, TestableForm)

    def test_get_form_uses_provided_form_class(self):
        form = self.get_testable_mixin().get_form(form_class=CustomForm)
        self.assertEqual(form.__class__, CustomForm)


class InlineFormsetMixinTestCase(FormMixinTestCase):
    mixin_class = views.InlineFormsetMixin

    def get_testable_mixin(self):
        mixin = super(InlineFormsetMixinTestCase, self).get_testable_mixin()
        mixin.inline_formset_class = TestableInlineFormset
        return mixin

    def test_get_inline_formset_uses_default_class(self):
        formset = self.get_testable_mixin().get_inline_formset()
        self.assertEqual(formset.__class__, TestableInlineFormset)

    def test_get_inline_formset_with_provided_formset_class(self):
        formset = self.get_testable_mixin().get_inline_formset(CustomFormset)
        self.assertEqual(formset.__class__, CustomFormset)

    def test_inline_formset_added_to_context(self):
        context_data = self.get_testable_mixin().get_context_data()
        self.assertTrue("inline_formset" in context_data)
        self.assertEqual(context_data["inline_formset"].__class__,
                TestableInlineFormset)

    def test_get_context_data_uses_provided_inline_formset_if_available(self):
        context_data = self.get_testable_mixin().get_context_data(
                inline_formset=CustomFormset())
        self.assertEqual(context_data["inline_formset"].__class__,
                CustomFormset)
