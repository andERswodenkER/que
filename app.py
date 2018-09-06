from flask import Flask
from flask import render_template
from flask import request
from lib.site import Site
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse

app = Flask(__name__)


@app.route('/')
def get_header():
    return render_template('base.html', title="QS")


@app.route('/', methods=['POST'])
def get_data():
    try:
        path = validate_url(request.form['path'])
        site = Site(path)
    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason)

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason)

    except Exception as e:
        return render_template('error.html', code="", msg="Es ist ein Fehler aufgetreten: {0}".format(e))
    else:
        meta_data = zip(site.titles,
                        site.title_length,
                        site.description,
                        site.description_length,
                        site.links)

        return render_template('result.html',
                               path=path,
                               meta=meta_data,
                               t_warnings=site.title_warnings,
                               t_error=site.title_errors,
                               d_warnings=site.description_warnings,
                               d_errors=site.description_errors,
                               author=site.author,
                               favicon=site.favicon
                               )


def validate_url(path):
    url = path

    if url.endswith("/"):
        url = url[:-1]

    p = urlparse(url, 'http')

    if p.netloc:
        netloc = p.netloc
        path = p.path
    else:
        netloc = p.path
        path = ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    p = p._replace(netloc=netloc, path=path)
    print(p.geturl())

    return p.geturl()


if __name__ == '__main__':
    app.run()
