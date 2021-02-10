# Bakdata_Demo
Rule-based text analysis of doctors letters using kafka-python

## Setting Up And Running
The easiest way to install Kafka is to download binaries and run it. You must make sure that you 
are using Java 7 or greater. Since it's based on JVM languages.

## Starting Zookepper For Windows
Kafka relies on Zookeeper, in order to make it run we will have to run Zookeeper first.

```.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties```

## Starting Kafka Server For Windows
Next, we have to start Kafka broker server:

```.\bin\windows\kafka-server-start.bat .\config\server.properties```

## Create Topics For Windows
Messages are published in topics. Use this command to create a new topic.

```.\bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic```

## Run The Consumer And Producer From Python Folder
First run the producer (gitbash) command:
```winpty python producer.py ./```

Second run the consumer:
```winpty python consumer.py consumer_group_a```

## Some Scalabiltity Examples Which We Provide
- It is mandatory for a consumer to register itself to a consumer group
- Consumer instances are separate process, to create two consumer run ```winpty python consumer.py``` twice each on different terminal

### Example: 1 Topic, 2 Partition, 1 Consumer
+ Message will be published to partition randomly
+ Message will be consumed by C1 
+ One consumer can consume from more than one partition

### Example: 1 Topic, 1 Partition, 2 Consumer
+ Here both consumer are registered to same consumer group
+ One consumer will be sitting idle (not good) 
+ Same partition can't be assigned to multiple consumer in same group (use different consumer-group to handle the problem)

### Example: 1 Topic, 2 Partition, 2 Consumer
+ Here both consumer can be registered to same consumer group
+ Each consumer consumes from one partition

