from django.views.generic.edit import FormMixin as DjangoFormMixin
from django.views.generic.edit import ProcessFormView as DjangoProcessFormView


class FormMixin(DjangoFormMixin):
    def get_form_class(self):
        return self.form_class

    def get_form(self, form_class=None):
        if not form_class:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return kwargs


class InlineFormsetMixin(FormMixin):
    inline_initial = {}
    inline_formset_class = None

    def get_inline_initial(self):
        """
        Returns the initial data to use for the inline forms on this view
        """
        return self.inline_initial

    def get_inline_formset_class(self):
        """
        Returns the inline form class to use in this view
        """
        return self.inline_formset_class

    def get_inline_formset(self, inline_formset_class=None):
        """
        Returns the inline form to use in this view
        """
        if not inline_formset_class:
            inline_formset_class = self.get_inline_formset_class()
        return inline_formset_class(**self.get_inline_formset_kwargs())

    def get_inline_formset_kwargs(self):
        kwargs = {"initial": self.get_inline_initial()}
        if self.request.method in ("POST", "PUT"):
            kwargs.update({
                "data": self.request.POST,
                "files": self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, inline_formset):
        """
        The response returned on a succesul POST/PUT
        """
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, inline_formset):
        """
        The response returned on an unsuccessful POST/PUT
        """
        context = self.get_context_data(form=form,
                                        inline_formset=inline_formset)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if "inline_formset" not in kwargs:
            kwargs["inline_formset"] = self.get_inline_formset()
        return super(InlineFormsetMixin, self).get_context_data(**kwargs)


class ProcessFormView(DjangoProcessFormView):
    """
    A mixin that processes a form on POST.

    Backported from #17557.
    """
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProcessInlineFormsetView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        inline_formset = None
        if form.is_valid():
            obj = form.save(commit=False)
            inline_formset = self.get_inline_formset()
            if inline_formset.is_valid():
                form.save()
                inline_formset.save()
                return self.form_valid(form, inline_formset)
        return self.form_invalid(form=form, inline_formset=inline_formset)
