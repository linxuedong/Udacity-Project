#!/usr/bin/env python3

import psycopg2


DBNAME = "news"


def popular_article():
    """
    List the most popular three articles
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT title, views
        FROM articles JOIN (
            SELECT path, count(path) AS views
            FROM log
            GROUP BY path
        ) AS log
        ON path = '/article/' || slug
        ORDER BY views DESC
        LIMIT 3;""")
    result = c.fetchall()
    db.close()
    return result


def popular_author():
    """
    list the most popular article authors
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT authors.name, views
        FROM authors JOIN (
            SELECT articles.author, sum(log.count) AS views
            FROM articles JOIN (
                SELECT log.path, count(log.path) FROM log GROUP BY log.path
            ) AS log
            ON log.path = '/article/' || articles.slug
            GROUP BY author
        ) AS author_views
        ON authors.id = author_views.author
        ORDER BY views DESC;""")
    result = c.fetchall()
    db.close()
    return result


def bad_request():
    """
    List which days did more than 1% of requests lead to errors
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT *
        FROM (
            SELECT bad.date,
            ROUND(bad.views::numeric/total.views::numeric*100.0, 2) AS percent
            FROM (
                SELECT date(time) as date, count(*) AS views
                FROM log
                WHERE status != '200 OK'
                GROUP BY date
            ) AS bad JOIN (
                SELECT date(time) as date, count(*) AS views
                FROM log
                GROUP BY date
            ) AS total
            ON bad.date = total.date
        ) AS result
        WHERE percent >1;""")
    result = c.fetchone()
    db.close()
    return result


if __name__ == '__main__':
    article_entry = "{} -- {} views \n"
    article_list = ''.join([article_entry.format(title, views)
                            for title, views in popular_article()])

    author_entry = "{} -- {} views \n"
    author_list = ''.join([author_entry.format(author, views)
                           for author, views in popular_author()])

    log_entyr = "{} -- {}% errors \n"
    log_info = log_entyr.format(bad_request()[0], str(bad_request()[1]))

    with open('output.txt', 'w') as output:
        q = '1. What are the most popular three articles of all time?'
        print(q, file=output)
        print(article_list, file=output)

        q = '2. Who are the most popular article authors of all time?'
        print(q, file=output)
        print(author_list, file=output)

        q = '3. On which days did more than 1% of requests lead to errors?'
        print(q, file=output)
        print(log_info, file=output)
