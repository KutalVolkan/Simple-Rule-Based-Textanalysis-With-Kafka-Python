from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import time
import argparse
from pathlib import Path
from os import listdir



# finding txt files in path 
def find_txt_filenames(path_to_dir, suffix=".txt" ):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

# create and returns the ArgumentParser object
def create_arg_parser():
    parser = argparse.ArgumentParser(description = 'Rule-based text analysis of doctors letters')
    parser.add_argument("file_path", type = Path,  help = 'Path to the input directory where the files lay e.g. ../doctor_letters/')
    parser.add_argument("--host", type = str, default = 'localhost' ,help = ' pass your local ip address e.g. localhost')
    parser.add_argument("--port", type = int, default = 9092, help = 'kafka default port e.g. 9092')
    parser.add_argument("--topic", type = str, default = 'TestTopic', help = 'TopicName you created using the configuration option' )
    parser.add_argument("--partitions", type = int, default = 1, help = 'number of partitions for topic' )
    return parser

def create_topic(p):
	admin_client = KafkaAdminClient(bootstrap_servers = [f'{p.host}:{p.port}'], client_id = 'vk')
	topic_list = []
	topic_list.append(NewTopic(name=f"{p.topic}", num_partitions=p.partitions, replication_factor=1))
	admin_client.create_topics(new_topics=topic_list, validate_only=False)

def main(p):
    txt_files = find_txt_filenames(f'{p.file_path}')
    # Kafkaproducer connects to a server or a broker, providing that address via bootstrap_servers
    producer = KafkaProducer(bootstrap_servers = [f'{p.host}:{p.port}'])

    for doctor_letter in txt_files: 
        with open(f'{p.file_path}/{doctor_letter}', 'r') as f:
            for letter in f:
                producer.send(f'{p.topic}', letter.encode('ascii'))
                time.sleep(4)

if __name__ == "__main__":
		# building a commaned-line interface
        parser = create_arg_parser() 
        p = parser.parse_args()

        print("Starting the producer") 
        # handles the TopicAlreadyExistsError, TODO more generic way
        if p.topic != "TestTopic":
        	create_topic(p)
        # simulate continuous flow of doctor letters
        while 1==1:
        	main(p)
		
