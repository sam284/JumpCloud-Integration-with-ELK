Integrating JumpCloud the ELK stack.

With the current script and configurations the logs are being forwarded to kafka after reaching logstash, this behavior can be changed by modifying the input plugin file to output directly to elastic.

The scripts pull logs as Json objects which eliminates the use of parsing if using elastic search.
