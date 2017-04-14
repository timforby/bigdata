# Big Data
Timothy Forbes

26856411
## Summary 

Map reduce assignment that inputs a directed social network of x users with a non symetrical follow assignment. The output will recommend a list of users to each user based on the number of followers they have in common.

## Requirements
Hadoop

Java

Correct environment variables

## Tested with
Hadoop 2.7.3

openjdk version "1.8.0_121"

## Execution

Run in terminal 
```
git clone https://github.com/timforby/bigdata.git
```
Move into bigdata
```
cd bigdata
```
### Option 1
Compile and execute
```
sh comp_run.sh a1 input.txt
```
### Option 2
Compile the assignment (note, no ".java" in name arg)
```
sh compile.sh a1
```
Execute hadoop jar
```
hadoop jar a1.jar "INPUT_FILE" "OUTPUT_FILE"
```
example
```
hadoop jar a1.jar a1 input.txt output
```
View ouput
```
cat output/p*
```
