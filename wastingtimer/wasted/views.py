from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import Wasted
from forms import UserWastedForm


class UserEditView(DetailView, SingleObjectMixin, FormMixin):
    form_class = UserWastedForm
    model = Wasted
    template_name = 'wasted/wasted_form.html'

    def get_success_url(self):
        return reverse('wasted:edit', kwargs={'pk': self.object.pk})

    def get_form(self, form_class):
        data = self.get_form_kwargs()

        # inject initial if we have it
        if hasattr(self, 'object'):
            data['initial'].update({
                'tweet': self.object.text,
            })

        # inject these values into the form, so we can access
        # the request and user objects
        data.update({
            'request': self.request,
            'object': getattr(self, 'object', None),
        })

        return form_class(**data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # this is the key element here
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.save() # manually call save as its not a model form
            messages.success(request, _('Successfully, updated this wasted message.'))
            return self.form_valid(form)
        else:
            messages.warning(request, _('Oh dear, it looks like there was a problem.'))
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context.update({
            'form': form,
        })
        context.update(kwargs)
        return context