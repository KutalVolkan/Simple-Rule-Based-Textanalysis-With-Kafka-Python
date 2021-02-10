import re 


def regex_gender(letter):
	gender = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'(\bman|\bwoman|\bm |\bf |\bmale|\bfemale)', letter, flags = re.I | re.M)]
	if len(gender) == 0:
		gender = "Unknown"
	return gender


def regex_age(letter):
	age = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'\b[0-9]{1,3}-year-old', letter, flags = re.I | re.M)]
	if len(age) == 0:
		age = "Unknown"
	return age


def check_context_exception(weight):
	weights = []
	for letter_part in weight:
		context = re.search(r"\b(pounds|lbs|lb|kg|kgs|oz|kilograms|kilos|(pounds\s*\d{1,3}\s*ounces))\b", letter_part[2], flags = re.I | re.M)
		if context is not None:
			weights.append(letter_part[2])
			return weights


def regex_weight(letter):
	weight = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'\b(weighs:?|weighed:?|weight:?)\s*\b(\d{1,3}(\.\d)?\s*(((kg)|(#|lb)|(pound))s?)?\s*((1?oz)|[0-9]{0,3}\s*(ounces|kilos|kilograms))?((gain|g|gram|grams|mg|milligram|milligrams|BMI|gains|gained|gaining|lose|lost|loses|losing|temperature|pulse|height)?)|[0-2]\d{3})\b', letter, flags = re.M)]
	if len(weight) == 0:
		weight = "Unknown"
	else:
		weight = check_context_exception(weight)
	return weight


	