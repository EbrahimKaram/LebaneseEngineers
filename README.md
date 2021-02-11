# TL; DR (too long didn't read)

The CSV with every engineer registered in Lebanon
<https://github.com/EbrahimKaram/LebaneseEngineers/blob/master/Data/all_engineers.csv>

If you are using excel to open the csv, you need to know that you need to change the encoding to UTF-8. Follow the steps [here](https://techcommunity.microsoft.com/t5/excel/open-and-edit-a-csv-file-in-utf8/m-p/1035542)

Early Data Analytics can be found here
<https://github.com/EbrahimKaram/LebaneseEngineers#quick-answers>


Please check the website to see the data displayed
https://ebrahimkaram.github.io/LebaneseEngineers/

Read on if you want to know about process and how it was done

# How to get Every Engineer in Lebanon

There is a website that allows to search the directory for engineers

<https://www.oea.org.lb/Arabic/MembersSearch.aspx?pageid=112>

now if you just search we will get ability to download the excel but it doesn't have the Latin names. You can check the excel they provide `OEA-All-Members.xlsx`. This is not what I like and is incomplete in my opinion. We can scrap the directory website and get what we need

We want to have a database of Latin names to Arabic names. It would be useful to train a model for later for Arabic to English or the other way around.

## Let's see what the actual request is

We open Developer tools and monitor the network and see what requests are being done when we click on search.

We can see that the page is sending the following request

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

If we plug that link into Google Chrome we can get the list of the first 20 names and it looks like this

    رقم المهندس: 14
    الاسم: يحيى أحمد مزبودي
    Latin Name: Yehia Ahmad Mazboudi
    التفاصيل (link to more details)

What happens when you press the next

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

Rand value changes but the curr page also changes which indicates the pagination. We can't change that to -1 then we have an invalid request.
Rand doesn't seem to be doing much could be a security issue.
We notice that currPage starts at 1 instead of zero

_What happens when we over increment currPage?_

We get the following response

<div id="hiddenNoMore" class="noResDiv">لا يوجد أي نتيجة</div>

These are Get Requests so we can do them from the browser and we don't need to use something like PostMan to test.

# Missing info

Now it seems that the database has fields that are requested but never shown. We can search by subfield and field but those are not reiterated in the results and are not provided in the excel that is easily downloadable.

They call them here the following `نوع الاختصاص` and 'حقل الاختصاص'

Those would go into the spec and spec1 field of the get requests

We are gonna call them accordingly
field and subfield
`نوع الاختصاص` and  `حقل الاختصاص`
We should probably start in getting IDs for the fields, their respective subfields, and the subfield IDs. (IDs are what the requests use)

| Requests | Arabic       | Ours      |
| -------- | ------------ | --------- |
| spec     | نوع الاختصاص | fields    |
| spec1    | حقل الاختصاص | subfields |

**Tech Tip**
Please note that UTF-8 is not the default for excel. You need to change it following the link below
<https://techcommunity.microsoft.com/t5/excel/open-and-edit-a-csv-file-in-utf8/m-p/1035542>

What we notice is that when we pick a field we don't get a list of subfields to choose from. They stay the same.

The subfields are the same for all fields. This might be due to a  time issue with implementation or just lazy implementation. This is just odd because the screen does load when you pick a field.

## What can we do

Let's see what happens when try an unrelated field with a subfield.
We will get the following response

    <div id="hiddenNoMore" class="noResDiv">لا يوجد أي نتيجة</div>

So maybe we should try all possible combinations and see what happens
we have 63 subfields and 10 fields. We have a total of 630 permutations to try.

### What we ended up with

We got 62 subfields and we now know which subfields are under which fields.
You can look into how that was done by checking
`GetTheFieldsAndSubfields.py`

The data is in the folder mentioned `Categories`

# Building a database

The ideal scenario is having a database with the following

-   Field
-   Subfield
-   Arabic Name
-   Latin Name
-   Engineer ID
-   Link to extra info for that individual on the order of engineers site

You can look at the `pullingTheDBv0.8.py` code to see how that was done. We put them into separate CSVs simply not to repeat the entire process if something broke midway. Small steps towards the bigger goal is preferred over a giant leap.

We know need to merge all that data into one CSV so it's easier to analyze. You can look at `mergeAllFiles.py` for the details on how that was done.

## Quick answers

**_How many engineers are registered as of February 6,2021?_**

65,949
Please note that the excel only mentions that we have 50,725 engineers. There might be duplicates in our file. We will check this now.
So apparently we have engineers that specialize in more than one field. There are 15002 engineers that specialize in more than one subfield.

**_What are the 3 most popular subfields_**

| Field              | Subfield           | Number |
| ------------------ | ------------------ | ------ |
| الهندسة الكهربائية | الهندسة الكهربائية | 10566  |
| الهندسة المدنية    | الهندسة المدنية    | 7055   |
| الهندسة المدنية    | مدني-عام           | 6844   |

_**What are the most popular fields?**_

| Field                                      | Number |
| ------------------------------------------ | ------ |
| الهندسة الكهربائية                         | 22035  |
| الهندسة المدنية                            | 17616  |
| الهندسة المعمارية                          | 12028  |
| الهندسة الميكانيكية                        | 9618   |
| الهندسة الزراعية                           | 3102   |
| الهندسة الصناعية والكيميائية والبترولية    | 1302   |
| اختصاصات متفرقة                            | 225    |
| هندسة المناجم والتعدين والهندسة الجيولوجية | 23     |

_**Which Field has the younger engineers?**_

ID's are given incrementally. New members have bigger ID numbers than old members

| Field                                      | Average ID   |
| ------------------------------------------ | ------------ |
| الهندسة الصناعية والكيميائية والبترولية    | 42830.877880 |
| اختصاصات متفرقة                            | 39955.746667 |
| الهندسة الميكانيكية                        | 38171.511957 |
| الهندسة الكهربائية                         | 36900.069027 |
| الهندسة المعمارية                          | 33925.649734 |
| الهندسة الزراعية                           | 32928.924242 |
| الهندسة المدنية                            | 32895.640327 |
| هندسة المناجم والتعدين والهندسة الجيولوجية | 23856.130435 |

Chemical engineering seems to have more recent members than old members. Civil engineering has more experienced engineers.

Now looking at the median ID. We know where that 50% mark is exactly. It could be a better indicator than average.

| Field                                      | Median ID |
| ------------------------------------------ | --------- |
| الهندسة الصناعية والكيميائية والبترولية    | 47467.0   |
| اختصاصات متفرقة                            | 44171.0   |
| الهندسة الميكانيكية                        | 38971.0   |
| الهندسة الكهربائية                         | 37240.0   |
| الهندسة المدنية                            | 34937.5   |
| الهندسة المعمارية                          | 34088.5   |
| الهندسة الزراعية                           | 30970.0   |
| هندسة المناجم والتعدين والهندسة الجيولوجية | 21851.0   |

It would seem that agriculture would need some fresh blood.

_**Which field has the earliest and latest members?**_

In a way I'm asking what the max and min ID are in each field. This would indicate in a sense the earliest and latest members

|                                            | Engineer_ID |         |       |
| ------------------------------------------ | ----------- | ------- | ----- |
| Field                                      | min         | median  | max   |
| الهندسة الصناعية والكيميائية والبترولية    | 2189        | 47467   | 60152 |
| اختصاصات متفرقة                            | 7596        | 44171   | 60035 |
| الهندسة الميكانيكية                        | 1177        | 38971   | 60163 |
| الهندسة الكهربائية                         | 844         | 37240   | 60162 |
| الهندسة المدنية                            | 14          | 34937.5 | 60164 |
| الهندسة المعمارية                          | 444         | 34088.5 | 60161 |
| الهندسة الزراعية                           | 1850        | 30970   | 60113 |
| هندسة المناجم والتعدين والهندسة الجيولوجية | 3752        | 21851   | 54811 |

# Future Prospects for this project

This allows for multiple projects in Machine learning and Data analysis.
Some ideas for Machine learning:

-   Machine learning to write any Latin name in Arabic
-   From your name what is likelihood you will become an engineer
-   Arabic to Latin training
-   etc...

Some ideas for Data analysis

-   What is the most dominant last name in every engineering Discipline
-   How many people are in each Discipline
    -   Answered Above
-   Which discipline is the least active (not a lot of new IDs)
    -   This can be done by checking the average ID. IDs are given sequentially. New members get bigger IDs
    -   Answered Above
-   A range of Age
    -   What is the smallest ID and largest ID. A indicator of membership age. who is an old member. WHo is a new member
    - Answered Above
-   etc...

Please download the complete CSV from [here](https://github.com/EbrahimKaram/LebaneseEngineers/blob/master/Data/all_engineers.csv)

# Support

If you liked this project and found it useful, I would really appreciate your support by buying me a drink via the link below

<https://www.buymeacoffee.com/bobKaram>

Also submit any issues you find in the link below. It could be a space for discussion and extra features that might be added. Also if you have any questions you would like to answer
https://github.com/EbrahimKaram/LebaneseEngineers/issues


# PostMortem
I just got feedback that I could have used an RPA for this. Some of them cost money but there's a free one from UIPath.
People are surprised that this info is readily available and are worried. Hopefully this project becomes more of an awareness campaign  
