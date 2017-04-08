# Big Data
Timothy Forbes

26856411
## Summary 

Spark assignment consisting in analyzing log files.

## Requirements
Python

Spark

Hadoop

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
.
├── data
│   ├── iliad
│   │   ├── part-00000
│   │   ├── part-00001
│   │   ├── part-00002
│   │   ├── part-00003
│   │   └── part-00004
│   ├── iliad_anonymized
│   │   ├── part-00000
│   │   ├── part-00001
│   │   ├── part-00002
│   │   ├── part-00003
│   │   ├── part-00004
│   │   └── _SUCCESS
│   ├── odyssey
│   │   ├── part-00000
│   │   ├── part-00001
│   │   ├── part-00002
│   │   ├── part-00003
│   │   └── part-00004
│   └── odyssey_anonymized
│       ├── part-00000
│       ├── part-00001
│       ├── part-00002
│       ├── part-00003
│       ├── part-00004
│       └── _SUCCESS
├── log_analyzer.py
├── out
│   ├── part-00000
│   └── _SUCCESS
└── README.md
```

## Execution

```
python3 log_analyzer.py -q <qid> <host1> <host2>
```

Where qid is the question number, host1 is the first host, and host2 is the second one.
