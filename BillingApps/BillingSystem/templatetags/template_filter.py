# from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
# from django.shortcuts import render
# from django.template.loader import render_to_string

# class Formset(LayoutObject):
# 	template = "mycollections/formset.html"

# 	def __init__(self, formset_name_in_context, template=None):
# 		self.formset_name_in_context = formset_name_in_context
# 		self.fields = []
# 		if template:
# 			self.template = template

# 	def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
# 		formset = context[self.formset_name_in_context]
# 		return render_to_string(self.template, {'formset': formset})

from django import template
register = template.Library()


@register.filter(is_safe=True)
def get_label_with_cssclass(value, arg):
	return value.label_tag(attrs={'class': arg})


@register.filter(is_safe=True)
def get_field_with_cssclass(value, arg):
	return value.as_widget(attrs={'class': arg})

@register.filter(is_safe=True)
def get_field_with_cssid(value, arg):
	return value.as_widget(attrs={'id': arg})



@register.filter(is_safe=True)
def addprefix(arg1, arg2):
	"""concatenate arg1 & arg2"""
	return str(arg1) + '-__prefix__-' +str(arg2)

@register.filter(is_safe=True)
def addidprefix(arg1, arg2):
	"""concatenate arg1 & arg2"""
	return "id_" + str(arg1) + '-__prefix__-' +str(arg2)


@register.filter(is_safe=True)
def addCls(value, arg):
	'''
	Add provided classes to form field
	:param value: form field
	:param arg: string of classes seperated by ' '
	:return: edited field
	'''
	css_classes = value.field.widget.attrs.get('class', '')
	# check if class is set or empty and split its content to list (or init list)
	if css_classes:
		css_classes = css_classes.split(' ')
	else:
		css_classes = []
	# prepare new classes to list
	args = arg.split(' ')
	for a in args:
		if a not in css_classes:
			css_classes.append(a)
	# join back to single string
	return value.as_widget(attrs={'class': ' '.join(css_classes)})