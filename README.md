#Kensho

## Setup
You should first download stanford posttagger at https://nlp.stanford.edu/software/stanford-postagger-full-2016-10-31.zip

Then, you should unzip stanford-postagger-full-2016-10-31.zip, and then modify the classpath line of setup.sh file as:

export CLASSPATH="%your unzip directory%/stanford-postagger-full-2016-10-31" 

then run setup.py:

`python setup.py`

## usage: 

First, please run main.py:

`python main.py`

Then it will output a line:

`请输入问题：`

So you can input what you would like to ask:

`当苹果公司发布iPad4时，哪家苹果公司的供应商股价上涨幅度会最大？`

`当三级飓风袭击福罗里达州时，哪支水泥股的涨幅会最大？`

`当朝鲜试射导弹时，哪支国防股将涨得最多？`


The program will output the Actionlist and the result:


`omni 675`