#!/bin/bash
#Start Zookeeper server:
bin/zookeeper-server-start.sh config/zookeeper.properties &

#Kafka server:
bin/kafka-server-start.sh config/server.properties &