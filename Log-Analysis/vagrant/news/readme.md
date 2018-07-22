# Log Analysis

## Resources

### main.py
This is a project that output the answer of three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### output.py
This will be a plain text file that is a copy of what your program printed out.

## Requirement
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VitrualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

### How to use vagrant
```
cd Log-Analysis/vagrant
vagrant up
vagrant ssh
```

## Database
The project use PostgreSQL database. In this project we have a database named news.
In news we have three tables:

author:

name | bio | id
-----|------|----
Ursula La Multa | Ursula La Multa is an expert on bears, bear abundance, and bear accessories. |  1

article:

author |  title   |      slug       |lead |      body      | time  | id
------ | ------ | ------ | ------ | ------ | ------ | ------
3 | Bad things gone, say good people | bad-things-gone | All bad things have gone away... | Bad things are a thing of the bad, bad past... | 2016-08-15 18:55:10.814316+00 | 23


logs:

path |       ip       | method | status |          time          |   id
------ | ------ | ------ | ------ | ------ | --------
/article/balloon-goons-doomed | 198.51.100.195 | GET    | 200 OK | 2016-07-01 07:00:23+00 | 1678927


## Run
```
cd /vagrant/news
python main.py
```

## Third part resources
[Download the news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.

This project is homework of [Full-stack Web Developer](https://cn.udacity.com/course/full-stack-web-developer-nanodegree--nd004-cn) in Udacity.
