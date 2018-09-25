from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from lib.site import Site
from urllib.error import URLError, HTTPError

app = Flask(__name__)


@app.route('/')
def get_header():
    return render_template('start.html', title="robot", path="http://www.yoursite.com")


@app.route('/', methods=['POST'])
def get_data():
    try:
        site = Site(request.form['path'])
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
                                   title="scan",
                                   path=request.form['path'],
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
                                   csv_file=site.file_string
                                   )
        else:
            return render_template('noresults.html')


@app.route('/scan/<path>')
def get_url(path):
    try:
        site = Site(path)
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
                                   title="scan",
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
                                   csv_file=site.file_string
                                   )
        else:
            return render_template('noresults.html')


@app.route('/csv/<path>')
def export_csv(path):
    try:
        site = Site(path)
    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason)

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason)

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e))
    else:
        if not site.title_length == [] and not site.description_length == []:
            return render_template('csv.html',
                                   path=path,
                                   csv_file=site.file_string
                                   )
        else:
            return render_template('noresults.html')


@app.route('/about')
def about():
    return render_template("about.html", title="about", path="http://www.yoursite.com")


@app.route('/thanks')
def thanks():
    return render_template("thanks.html", title="yay!", path="http://www.you-are-awesome.com")


if __name__ == '__main__':
    app.run()
