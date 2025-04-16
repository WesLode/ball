# PySpark SetUp
Note for setting up PySpark + Hadoop environment

## Requirement

Python 3.11

## Download Link

* Hadoop (winutils): https://github.com/steveloughran/winutils
* Spark: https://spark.apache.org/downloads.html


## Enviornmental Variable

Add the following to System Variables

* HADOOP_HOME -> pointing to your folder winutils
* JAVA_HOME -> pointing to your JDK folder
* PYSPARK_DRIVER_PYTHON -> pointing to your python.exe
* PYSPARK_HOME -> pointing to your python.exe
* PYSPARK_PYTHON -> pointing to your python.exe

### Update Path

Add the following to the path


```
%HADOOP_HOME%\bin;
%JAVA_HOME%\bin;
%SPARK_HOME%\bin;
```