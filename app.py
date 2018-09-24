from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from lib.site import Site
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
import tldextract
import csv
from urllib.request import urlopen
import random

app = Flask(__name__)


@app.route('/')
def get_header():
    return render_template('base.html', title="QS")


@app.route('/', methods=['POST'])
def get_data():
    try:
        path = validate_url(request.form['path'])
        site = Site(path)
        hash_value = random.getrandbits(16)
        file_string = str(request.form['path'])[11:-4] + str(hash_value)
        print(file_string)
        with open('static/{0}.csv'.format(file_string), 'w', newline='') as csvfile:
            seo_writer = csv.writer(csvfile,  delimiter=",")
            seo_writer.writerow(["Link"] + ["Title"] + ["Description"])
            for link, title, description in zip(site.links, site.title, site.description):
                seo_writer.writerow([link] + [title] + [description])

    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason)

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason)

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e))
    else:
        meta_data = zip(site.title,
                        site.title_length,
                        site.description,
                        site.description_length,
                        site.links)
        if not site.title_length == [] and not site.description_length == []:
            return render_template('result.html',
                                   path=path,
                                   meta=meta_data,
                                   site_errors=site.site_errors,
                                   site_errors_counter=site.site_errors_counter,
                                   t_warnings=site.title_warnings,
                                   t_error=site.title_errors,
                                   d_warnings=site.description_warnings,
                                   d_errors=site.description_errors,
                                   author=site.author,
                                   favicon=site.favicon,
                                   appletouchicon=site.apple_touch_icon,
                                   appleapptitle=site.apple_touch_title,
                                   keywords=site.keywords,
                                   alt_links=site.image_alt_error_links,
                                   alt_errors=site.image_alt_error_counter,
                                   comments=site.comments,
                                   comments_counter=site.comments_counter,
                                   todos=site.todo,
                                   todos_counter=site.todo_counter,
                                   hash=file_string
                                   )
        else:
            return render_template('noresults.html')

@app.route('/scan/<path>')
def get_url(path):
    try:
        url = validate_url(path)
        site = Site(url)
        hash_value = random.getrandbits(8)
        file = str(path[4:3]) + str(hash_value)
        print(file)
        with open('static/{0}.csv'.format(file), 'w', newline='') as csvfile:
            seo_writer = csv.writer(csvfile,  delimiter=",")
            seo_writer.writerow(["Link"] + ["Title"] + ["Description"])
            for link, title, description in zip(site.links, site.title, site.description):
                seo_writer.writerow([link] + [title] + [description])

    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason)

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason)

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e))
    else:
        meta_data = zip(site.title,
                        site.title_length,
                        site.description,
                        site.description_length,
                        site.links)
        if not site.title_length == [] and not site.description_length == []:
            return render_template('result.html',
                                   path=path,
                                   meta=meta_data,
                                   site_errors=site.site_errors,
                                   site_errors_counter=site.site_errors_counter,
                                   t_warnings=site.title_warnings,
                                   t_error=site.title_errors,
                                   d_warnings=site.description_warnings,
                                   d_errors=site.description_errors,
                                   author=site.author,
                                   favicon=site.favicon,
                                   appletouchicon=site.apple_touch_icon,
                                   appleapptitle=site.apple_touch_title,
                                   keywords=site.keywords,
                                   alt_links=site.image_alt_error_links,
                                   alt_errors=site.image_alt_error_counter,
                                   comments=site.comments,
                                   comments_counter=site.comments_counter,
                                   todos=site.todo,
                                   todos_counter=site.todo_counter,
                                   hash=str(hash_value)
                                   )
        else:
            return render_template('noresults.html')


@app.route('/api/<path>')
def api(path):
    try:
        url = validate_url(path)
        site = Site(url)

        data = jsonify(
            path=path,
            title=site.title,
            title_length=site.title_length,
            description=site.description,
            description_length=site.description_length,
            links=site.links,
            site_errors=site.site_errors,
            site_errors_counter=site.site_errors_counter,
            t_warnings=site.title_warnings,
            t_error=site.title_errors,
            d_warnings=site.description_warnings,
            d_errors=site.description_errors,
            author=site.author,
            favicon=site.favicon,
            appletouchicon=site.apple_touch_icon,
            appleapptitle=site.apple_touch_title,
            keywords=site.keywords,
            alt_links=site.image_alt_error_links,
            alt_errors=site.image_alt_error_counter,
            comments=site.comments,
            comments_counter=site.comments_counter,
            todos=site.todo,
            todos_counter=site.todo_counter
        )

        return data

    except Exception as e:
        return print("Es ist ein Fehler aufgetreten: {0}".format(e))

@app.route('/csv/<path>')
def export_csv(path):
    url = validate_url(path)
    site = Site(url)
    try:
        with open('seo.csv'.format(url), 'w', newline='') as csvfile:
            seo_writer = csv.writer(csvfile, delimiter=';')
            seo_writer.writerow(site.links)
            seo_writer.writerow(site.title)
            seo_writer.writerow(site.description)

        f = urlopen("seo.csv")
        with open("code2.zip", "wb") as code:
            code.write(f.read())

            return "OK!"

    except Exception as e:
        print(e)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")



def validate_url(path):
    url = path
    sub = tldextract.extract(url)

    if url.endswith("/"):
        url = url[:-1]

    p = urlparse(url, 'http')

    if p.netloc:
        netloc = p.netloc
        path = p.path
    else:
        netloc = p.path
        path = ''
    if not netloc.startswith('www.') and not sub.subdomain:
        netloc = 'www.' + netloc

    p = p._replace(netloc=netloc, path=path)
    print(p.geturl())
    return p.geturl()


if __name__ == '__main__':
    app.run()
