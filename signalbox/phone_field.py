#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from six import with_metaclass
import phonenumbers
from django.db import models
from django import forms
from django.conf import settings
from phonenumbers import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException

DEFAULT_TELEPHONE_COUNTRY_CODE = settings.DEFAULT_TELEPHONE_COUNTRY_CODE

international_tuple = lambda x: (x.country_code, x.national_number)


def international_string(phone_number_obj):
    try:
        return phonenumbers.format_number(phone_number_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except:
        return ""


def as_phone_number(value):
    if not value or isinstance(value, PhoneNumber):
        return value
    try:
        return phonenumbers.parse(value, settings.DEFAULT_TELEPHONE_COUNTRY_CODE)
    except NumberParseException:
        return PhoneNumber()

# this all still here to keep migrations happy



#
# class PhoneNumberMultiWidget(forms.MultiWidget):
#
#     def __init__(self, attrs=None):
#         _widgets = (
#             forms.TextInput(attrs={'size': 3, 'class': 'countrycode'}),
#             forms.TextInput(attrs={'size': 8})
#         )
#         super(PhoneNumberMultiWidget, self).__init__(_widgets, attrs)
#
#     def decompress(self, value):
#         if value:
#             return international_tuple(as_phone_number(value))
#         else:
#             return ["", ""]
#
#
# class PhoneNumberMultiHiddenWidget(forms.MultipleHiddenInput):
#     pass
#
#
# class PhoneNumberFormField(forms.fields.MultiValueField):
#     def __init__(self, *args, **kwargs):
#         self.widget = PhoneNumberMultiWidget
#         self.hidden_widget = PhoneNumberMultiHiddenWidget
#
#         fields = (
#             forms.fields.CharField(),
#             forms.fields.CharField()
#         )
#         defaults = {
#             "help_text": "Enter a phone number (country code / number)",
#         }
#         defaults.update(kwargs)
#         super(PhoneNumberFormField, self).__init__(fields, *args, **defaults)
#
#     def compress(self, value):
#         if value and isinstance(value, list):
#             value[0] = "+" + value[0]
#         return "".join(value)
#
#
#
class PhoneNumberField(models.CharField):
    pass

# class PhoneNumberField(with_metaclass(models.SubfieldBase, models.Field)):
#
#     def get_internal_type(self):
#         return "CharField"
#
#     def formfield(self, **kwargs):
#         defaults = {
#             "form_class": PhoneNumberFormField
#         }
#         defaults.update(kwargs)
#         return super(PhoneNumberField, self).formfield(**defaults)
#
#     def to_python(self, value):
#         if value:
#             return as_phone_number(value)
#
#     def get_prep_value(self, value):
#         if value:
#             return self.value_to_string(value)
#
#     def __init__(self, *args, **kwargs):
#         kwargs['max_length'] = 16
#         super(PhoneNumberField, self).__init__(*args, **kwargs)
#
#     def value_to_string(self, obj):
#         if obj is not None:
#             return international_string(obj)
#         else:
#             return self.get_default()
#
