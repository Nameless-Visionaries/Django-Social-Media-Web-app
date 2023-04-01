from django.core.exceptions import ValidationError

def file_size(value):
	filesize = value.size
	if filesize > 400000000:
		raise ValidationError('maximum upload size is 400MB')