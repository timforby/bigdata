export CLASSPATH=${HADOOP_HOME}/share/hadoop/common/hadoop-common-2.7.3.jar:${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-client-core-2.7.3.jar
javac $1.java
jar cvf $1.jar $1*.class 
