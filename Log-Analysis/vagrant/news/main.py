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
        SELECT title, count(path) AS view
        FROM articles JOIN log
        ON path = CONCAT('/article/', slug)
        GROUP BY title
        ORDER BY view DESC
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
        SELECT name, view
        FROM authors JOIN (
            SELECT author,  count(author) AS view
                FROM articles JOIN log
                ON path = CONCAT('/article/', slug)
                GROUP BY author
                ORDER BY view DESC
            ) AS popular_author
        ON authors.id = popular_author.author;""")
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
            SELECT date(time),
            to_char(100.0*bad.b_view::numeric/count(*)::numeric, '999D99%')
             as percent
            FROM (SELECT date(time) AS b_date, count(*) AS b_view
            FROM log
            WHERE status NOT LIKE '200%'
            GROUP BY date(time)) AS bad JOIN log
            ON date(time) = bad.b_date
            GROUP BY date(time), bad.b_view
        ) AS result
        WHERE to_number(percent, '999D99%') > 1
        ;""")
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

    log_entyr = "{} -- {} errors \n"
    log_info = log_entyr.format(bad_request()[0], bad_request()[1].strip())

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
