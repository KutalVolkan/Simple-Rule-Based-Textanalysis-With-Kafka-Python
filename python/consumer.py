from kafka import KafkaConsumer
import re 
import os
import argparse
import json
from pathlib import Path


# create and returns the ArgumentParser object
def create_arg_parser():
    parser = argparse.ArgumentParser(description = 'Rule-based text analysis of doctors letters')
    parser.add_argument("--host", type = str, default = 'localhost' ,help = ' pass your local ip address e.g. localhost')
    parser.add_argument("--port", type = int, default = 9092, help = 'kafka default port e.g. 9092')
    parser.add_argument("--topic", type = str, default = 'TestTopic', help = 'TopicName you created using the configuration option' )
    parser.add_argument("--file_path", type = Path, default = '../kafka_output', help = 'Path where the kafka-output should be stored e.g. ../kafka_output')
    parser.add_argument("consumer_group", type = str, help = "mandatory for a consumer to register itself to a consumer group e.g. consumer_group_a")
    return parser


def store_kafka_output(target_path, target_file, data):
	if not os.path.exists(target_path):
		try:
			os.makedirs(target_path)
		except Exception as e:
			print(e)
			raise

	with open(os.path.join(target_path, target_file), 'w') as outfile:
		json.dump(data, outfile)


def regex_gender(letter):
	gender = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'(\bman|\bwoman|\bm |\bf |\bmale|\bfemale)', letter, flags = re.I | re.M)]
	if len(gender) == 0:
		gender = "Unknown"
	return gender


def regex_age(letter):
	age = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'\b[0-9]{1,3}-year(s)?-old', letter, flags = re.I | re.M)]
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
	weight = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'\b(weighs:?|weighed:?|weight:?)\s*\b(\d{1,3}(\.\d)?\s*(((kg)|(#|lb)|(pound))s?)?\s*((1?oz)|[0-9]{0,3}\s*(ounces|kilos|kilograms))?((gain|g|gram|grams|mg|milligram|milligrams|BMI|gains|gained|gaining|lose|lost|loses|losing|temperature|pulse|height)?)|[0-2]\d{3})\b', letter, flags = re.I | re.M)]
	if len(weight) == 0:
		weight = "Unknown"
	else:
		weight = check_context_exception(weight)
	return weight


def prepare_output(gender, age ,weight):
	doctor_letter_label = {
        						"Docletter:" : "{}".format(letter),
        						"Gender: ": "{}".format(gender),
        						"Age: " : "{}".format(age),
        						"Weight: " : "{}".format(weight)}
	return doctor_letter_label

    
if __name__ == "__main__":
	
	parser = create_arg_parser()
	p = parser.parse_args()
	consumer = KafkaConsumer(f"{p.topic}", bootstrap_servers  = f"{p.host}:{p.port}", auto_offset_reset  = "earliest", group_id = f"{p.consumer_group}")
	print("Starting the consumer")

	letter_id = 0
	for msg in consumer:
		letter = msg.value.decode()

		# starting to extract information via regex, and printing output into terminal
		gender = regex_gender(letter)
		age = regex_age(letter)
		weight = regex_weight(letter)
		doctor_letter_label = prepare_output(gender, age, weight)

		# store extractetd information into file
		store_kafka_output(f'{p.file_path}', f'doctor_letter_id{letter_id}', doctor_letter_label)
		letter_id +=1

		# printing letter into terminal
		for k, v in doctor_letter_label.items():
			print(k, v)
		print("--------")
