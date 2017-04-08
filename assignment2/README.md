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

Spark v 2.1.0

Python 3.5.2 (Note this assignment will only work for python3+)

Not guaranteed but to make it work on python2 changes must be made to the following:
```
dict.items() => dict.iteritems()
print(*,end='') => print (*,end="")
```


## Assignment 2 - Log Analyzer

**HOSTS** are assumed to be in folder called data.

Tree structure would look like so:
```
assignment2

--data

----illiad

------part-000000

------part-000001

------part-000002

------part-000003

------part-000004

----odyseey

------part-000000

------part-000001

------part-000002

------part-000003

------part-000004

--out

----success

--log_analyzer.py
```

## Execution

```
python3 log_analyzer.py -q <qid> <host1> <host2>
```

Where <qid> is the question number, <host1> is the first host, and <host2> is the second one.
