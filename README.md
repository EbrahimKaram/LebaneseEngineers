# How to get Every Engineer in Lebanon
There is a website that allows to search the directory for engineers

https://www.oea.org.lb/Arabic/MembersSearch.aspx?pageid=112


now if just search we will get ability to download the excel but it doesn't have the latin names.

We want to have a database of Latin names to Arabic names. It would be useful to train a model for later for Arabic to English

## Let's see what the actual request is
We open Developer tools and monitor the network and see what requests are being done

We can see that the network is sending the following request
```
https://www.oea.org.lb/Arabic/GetMembers.aspx?PageID=112&CurrPage=1&fstname=&lstname=&fatname=&numb=&spec=-1&spec1=-1&searchoption=And&rand=0.9449476735976416

PageID: 112
CurrPage: 1
fstname:
lstname:
fatname:
numb:
spec: -1
spec1: -1
searchoption: And
rand: 0.9449476735976416

```
If we plug that link into Google Chrome we can get the list of the names to the first 20 names and it looks like this
```
رقم المهندس: 14
الاسم: يحيى أحمد مزبودي
Latin Name: Yehia Ahmad Mazboudi
التفاصيل (link to more details)
```
What happens when you press the next

```
https://www.oea.org.lb/Arabic/GetMembers.aspx?PageID=112&CurrPage=3&fstname=&lstname=&fatname=&numb=&spec=-1&spec1=-1&searchoption=And&rand=0.055286690143709905

PageID: 112
CurrPage: 3
fstname:
lstname:
fatname:
numb:
spec: -1
spec1: -1
searchoption: And
rand: 0.055286690143709905
```
Rand value changes but the curr page also changes which indicates the pagination. We can't change that to -1
rand doesn't seem to be doing much could be a security issue.
currPage starts at 1

What happens when we over increment currPage?
We get the following response
<div id="hiddenNoMore" class="noResDiv">لا يوجد أي نتيجة</div>

These are Get Requests so we can do them from the browser

# Missing info
Now it seems that the database has fields that are requested but never shown
like we other than the search field we can't seem to find the major field and subfield
They call them here the following `نوع الاختصاص ` and 'حقل الاختصاص'

Those would go into the spec and spec1 field

We are gonna call them accordingly
field and subfield
`نوع الاختصاص ` and 'حقل الاختصاص'
We should probably start in getting the and number for the fields and their respective subfields

Requests  |  Arabic |  Ours
--|---|--
  spec | نوع الاختصاص  |  fields
spec1  | حقل الاختصاص  |  subfields


https://techcommunity.microsoft.com/t5/excel/open-and-edit-a-csv-file-in-utf8/m-p/1035542

It seems that the subfields are not divided according to fields
The subfields are the same for all fields. Seems to be a time issue with implementation or just lazy implementation

## What can we do
Let's see what happens when try unrelated field with a subfield
We will get the following response

```
<div id="hiddenNoMore" class="noResDiv">لا يوجد أي نتيجة</div>
```

So maybe we should try all possible combinations and see what happens
we have 63 subfields and 10 fields. We have a total of 630 permutations to try

### What we ended up with
We got 62 subfields and we now know which subfields are under which fields.
You can look into how that was done by checking
`GetTheFieldsAndSubfields.py`

The data is in the folder mentioned `Categories`

# Building a database
The ideal scenario is having a database with the following
* Field
* Subfield
* Arabic Name
* Latin Name
* Engineer ID
* Link to extra info for that individual on the order of engineers sites

You can look at the `pullingTheDBv0.8.py` code to see how that was done.

We know need to merge all that data into one CSV so it's easier to analyze. You can can look at `mergeAllFiles.py` for the details on how that was done.

## Quick answers
***How many engineers are registered as of February 6,2021?***

65,949
Please note that the excel only mentions that we have 50,725 engineers. There might be duplicates in our file. We will check this now.
So apparently we have engineers that specialize in more than one field. There are 15002 engineers that specialize in more than one subfield.

***What are the 3 most popular subfields***

Field  |  Subfield |  Number
--|---|--
  الهندسة الكهربائية| الهندسة الكهربائية  |  10566
 الهندسة المدنية  |   الهندسة المدنية |   7055
 الهندسة المدنية|مدني-عام |    6844    

_**What are the most popular fields?**_

Field | Number
--|--
 الهندسة الكهربائية                     |    22035
 الهندسة المدنية                            |   17616
 الهندسة المعمارية                          |   12028
 الهندسة الميكانيكية                        |    9618
 الهندسة الزراعية                           |    3102
 الهندسة الصناعية والكيميائية والبترولية    |    1302
 اختصاصات متفرقة                            |     225
 هندسة المناجم والتعدين والهندسة الجيولوجية |      23


# Future Prospects for this project

This allows for multiple projects in Machine learning and Data analysis.
Some ideas for Machine learning:
* Machine learning to write any Latin name in Arabic
* From your name what is likelihood you will become an engineer
* Arabic to Latin training
* etc...

Some ideas for Data analysis
* What is the most dominant last name in every engineering Discipline
* How many people are in each Discipline
* Which discipline is the least active (not a lot of new IDs)
* etc...


# Support
If you liked this project and found it useful, I would really appreciate your support by buying me a drink via the link below

https://www.buymeacoffee.com/bobKaram
