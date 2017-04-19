from flask.ext.wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired



"""Edits Form Class"""
class MyBaseForm(Form):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(my_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)
""" Remote White spaces"""
def my_strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value


class LoginForm(MyBaseForm):
    """Input Valdidators for Html Forms"""
    Client_id = StringField('Client_id', validators=[InputRequired()],render_kw={"placeholder": "Client ID"})
    Password = PasswordField('Password', validators=[InputRequired()],render_kw={"placeholder": "Password"})


"""JSON Vaildations Schema"""
client_view_schema = {'case_name': {'required': True, 'type': 'string'}, 'priority': {'required': True, 'type': 'integer', 'max': 10},
          'target_date': {'required': True, 'type': 'string', 'regex': '(1[0-2]|0[1-9]|[1-9])\/(3[0-1]|[1-2][0-9]|[0-9])\/2\d{3}'},
          'product_area': {'required': True, 'type': 'string'},'description': {'required': True, 'type': 'string'}}
