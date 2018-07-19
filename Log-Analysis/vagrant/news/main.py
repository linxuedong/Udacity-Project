import psycopg2
from flask import Flask

app = Flask(__name__)

DBNAME = "news"


def popular_article():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT title, count(path) AS view \
                FROM articles JOIN log \
                ON path LIKE CONCAT('%', slug, '%') \
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
                        ON path LIKE CONCAT('%', slug, '%')\
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


HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB Forum</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>1. What are the most popular three articles of all time? </h1>
    <ul>
        %s
    </ul>

    <h1>2. Who are the most popular article authors of all time? </h1>
    <ul>
        %s
    </ul>

    <h1>3. On which days did more than 1 percent of requests lead to errors?</h1>
    <ul>
        %s
    </ul>
  </body>
</html>
'''

ENTRY = """<li>%s ---- %s %s </li>"""


@app.route('/', methods=['GET'])
def index():
    article_list = "".join(ENTRY % (title, str(views), 'views')
                           for title, views in popular_article())
    author_list = "".join(ENTRY % (author, str(views), 'views')
                          for author, views in popular_author())
    error_date = "".join(ENTRY % (bad_request()[0], bad_request()[1], 'error'))

    html = HTML_WRAP % (article_list, author_list, error_date)
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
