# multi-label learning dataset and data-loader

This code repository aims to help you

1. unify the arff-format dataset downloaded from [Multi-Label Classification Dataset Repository](https://www.uco.es/kdis/mllresources/)
2. transform the format of dataset between `.arff` and `.mat` (for matlab)

## how to use it

Install the required python packages

```
$ pip install -r requirements.txt
```

Scan the dataset in under the current directory, 
and show basic information. 

```bash
$ python dataset.py
```

Transform them from `.arff` format into `.mat` format by a simple script

```bash
$ python arff2mat.py
```

## read before use

Since `.arff` format do not distinguish features and labels, 
we need to manually split the 
$n \times (m+q)$ matrix into the data (X) and targets (y). 
However, Mulan-source files prefer to put labels put before features 
($n \times (q+m)$), 
while Meka-source files prefer the other way ($n \times (m+q)$). 
The difference of preference cannot be distinguish unless we add some meta information. 

Therefore, you need to **manually** add these meta information in each `.arff` file,
so that the script can load the features and targets automatically. 
 
## how to add meta information

Given a `.arff` file (`ENRON.arff`) like this

```
@relation Enron

@attribute A.A8 {0,1}
@attribute C.C9 {0,1}
@attribute B.B12 {0,1}
@attribute C.C11 {0,1}
@attribute C.C5 {0,1}
@attribute C.C7 {0,1}
...
@attribute 0 numeric
@attribute 00 numeric
@attribute 000 numeric

@data

{14 1,40 1,46 1,49 1,193 1,441 1,841 1}
{12 1,14 1,37 1,39 1,49 1,56 1,69 1,71 1,76 1,117 1,118 1,133 1,136 1,141 1,209 1,239 1,240 1,242 1,245 1,252 1,255 1,302 1,304 1,316 1,331 1,344 1,364 1,411 1,451 1,458 1,473 1,479 1,528 1,535 1,551 1,556 1,581 1,608 1,613 1,662 1,683 1,705 1,741 1,758 1,763 1,764 1,796 1,835 1,857 1,869 1,872 1,901 1,928 1,939 1,964 1,982 1,1000 1,1012 1,1043 1}
{11 1,242 1,247 1,442 1,561 1,862 1}
{11 1,199 1,386 1,558 1,583 1,590 1}
{11 1,199 1,237 1,265 1,312 1,381 1,394 1,398 1,412 1,458 1,483 1,490 1,494 1,532 1,560 1,626 1,655 1,708 1,729 1,734 1,855 1,968 1,979 1,993 1,1008 1,1050 1}
...
```

Please edit the **`@relation` line** at the begin of each arff file as follow 

```
@relation 'Enron: -n 1702 -m 1001 -q 53 -label_location start -is_sparse true'

@attribute A.A8 {0,1}
@attribute C.C9 {0,1}
@attribute B.B12 {0,1}
@attribute C.C11 {0,1}
@attribute C.C5 {0,1}
@attribute C.C7 {0,1}
...
@attribute 0 numeric
@attribute 00 numeric
@attribute 000 numeric

@data

{14 1,40 1,46 1,49 1,193 1,441 1,841 1}
{12 1,14 1,37 1,39 1,49 1,56 1,69 1,71 1,76 1,117 1,118 1,133 1,136 1,141 1,209 1,239 1,240 1,242 1,245 1,252 1,255 1,302 1,304 1,316 1,331 1,344 1,364 1,411 1,451 1,458 1,473 1,479 1,528 1,535 1,551 1,556 1,581 1,608 1,613 1,662 1,683 1,705 1,741 1,758 1,763 1,764 1,796 1,835 1,857 1,869 1,872 1,901 1,928 1,939 1,964 1,982 1,1000 1,1012 1,1043 1}
{11 1,242 1,247 1,442 1,561 1,862 1}
{11 1,199 1,386 1,558 1,583 1,590 1}
{11 1,199 1,237 1,265 1,312 1,381 1,394 1,398 1,412 1,458 1,483 1,490 1,494 1,532 1,560 1,626 1,655 1,708 1,729 1,734 1,855 1,968 1,979 1,993 1,1008 1,1050 1}
``` 

the detailed explaination of attributes are given below: 

1. `-n`: the number of instances (not actually used)
2. `-m`: dimensions of features (not actually used)
3. `-q`: dimensions of labels
4. `-label_location`: if `@attribute` list the attribute of labels firstly, then the attribute of features, input `start`; otherwise, `end`
5. `-is_sparse`: if `@data` is stored in sparse format, input `true`; otherwise `false` (not actually used)

If you do that, you can load this dataset automatically! 
Wish you have a good time :) 