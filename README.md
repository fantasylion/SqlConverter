# SqlConverter
It can convert spring-schedule-task.xml into an SQL statement. 

### Require
python version 3.5.2

### How to use

```Python
py readX.py --xmlFile=../dev/spring-schedule-task-dev.xml --propFile=../dev/schedule-dev.properties
```

`--xmlFile=spring-schedule-task.xml` and `--propFile=schedule.properties` is default so you can do like that

```Python
py readX.py
```

### Options

* `xmlFile`     schedule.xml
* `propFile`    cronExpression.properties
* `tableName`   table name

It will create a file name `result.sql` at project dirctory

