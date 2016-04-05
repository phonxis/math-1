from django import forms

class FirstForm(forms.Form):
	my_choices = (
			('1', '1'),
			('2', '2'),
			('3', '3'),
			('4', '4'),
			('5', '5'),
			('6', '6'),
			('7', '7'),
			('8', '8'),
			('9', '9'),
		)
	number_of_companies = forms.ChoiceField(choices=my_choices, label='Кількість компаній')
	number_of_rows = forms.ChoiceField(choices=my_choices, label='Кількість можливих варіантів інвестування')

