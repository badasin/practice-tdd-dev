from django import forms
from lists.models import Item, List
from django.core.exceptions import ValidationError

EMPTY_LIST_ERROR = "You can't have an empty list item."
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):
	
	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
				'text': forms.fields.TextInput(attrs={
					'placeholder': 'Enter a to-do item',
					'class': 'form-control input-lg',
					}),
			}
		error_messages = {
			'text': {'required': EMPTY_LIST_ERROR}
		}

class NewListForm(ItemForm):
	
	def save(self, owner):
		list_ = List()
		if owner.is_authenticated():
			list_.owner = owner
		list_.save()
		item = Item()
		item.list = list_
		item.text = self.cleaned_data['text']
		item.save()
		return list_



class ExistingListItemForm(ItemForm):
	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list
	
	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)

