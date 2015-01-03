import re

# These transformations make it easy to type text with normal line returns
# And use tabs like a normal person.  I should really experiment with using
# <div>'s but that's a can of worms and this "just works" except for some
# minor clipping I don't really mind in the article samples.
transformations = {
	'\t':"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp",
	'\n\n':"<br>",
}

def Transform(text):
	'''
		Apply all transformations in order to text.

		:param text: the string to transform
	'''
	for pattern, replacement in transformations.items():
		text = re.sub(pattern, replacement, text)

	return text

