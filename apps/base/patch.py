# coding=utf-8

from django.forms.forms import BoundField
from xadmin.widgets import SelectRelation


def as_widget(self, widget=None, attrs=None, only_initial=False):
    """
    Renders the field by rendering the passed widget, adding any HTML
    attributes passed as attrs.  If no widget is specified, then the
    field's default widget will be used.
    """
    if not widget:
        widget = self.field.widget

    attrs = attrs or {}
    auto_id = self.auto_id
    if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
        if not only_initial:
            attrs['id'] = auto_id
        else:
            attrs['id'] = self.html_initial_id

    if not only_initial:
        name = self.html_name
    else:
        name = self.html_initial_name
    if isinstance(widget,SelectRelation):
        return widget.render(name,self.value(),attrs=attrs,form=self.form)
    return widget.render(name, self.value(), attrs=attrs)

BoundField.as_widget = as_widget
