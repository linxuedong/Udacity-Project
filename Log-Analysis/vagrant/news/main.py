import psycopg2


DBNAME = "news"


def popular_article():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT title, count(path) AS view \
                FROM articles JOIN log \
                ON path LIKE CONCAT('/article/', slug) \
                GROUP BY title \
                ORDER BY view DESC \
                LIMIT 3;")
    result = c.fetchall()
    db.close()
    return result


def popular_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT name, view \
                FROM authors JOIN ( \
                    SELECT author,  count(author) AS view \
                        FROM articles JOIN log \
                        ON path LIKE CONCAT('/article/', slug)\
                        GROUP BY author \
                        ORDER BY view DESC \
                    ) AS popular_author \
                ON authors.id = popular_author.author;")
    result = c.fetchall()
    db.close()
    return result


def bad_request():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * \
            FROM ( \
                SELECT date(time), to_char(100.0*bad.b_view::numeric/count(*)::numeric, '999D99%') as percent \
                FROM (SELECT date(time) AS b_date, count(*) AS b_view \
                FROM log \
                WHERE status NOT LIKE '200%' \
                GROUP BY date(time)) AS bad JOIN log \
                ON date(time) = bad.b_date \
                GROUP BY date(time), bad.b_view \
            ) AS result \
            WHERE to_number(percent, '999D99%') > 1 \
            ;")
    result = c.fetchone()
    db.close()
    return result
