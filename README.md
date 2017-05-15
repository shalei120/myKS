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

`���������⣺`

So you can input what you would like to ask:

`��ƻ����˾����iPad4ʱ���ļ�ƻ����˾�Ĺ�Ӧ�̹ɼ����Ƿ��Ȼ����`

`������쫷�Ϯ�����������ʱ����֧ˮ��ɵ��Ƿ������`

`���������䵼��ʱ����֧�����ɽ��ǵ���ࣿ`


The program will output the Actionlist and the result:


`omni 675`