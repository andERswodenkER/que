from flask import Flask
from flask import render_template
from flask import request
from lib.site import Site
from urllib.error import URLError, HTTPError
from flask import make_response
import datetime

app = Flask(__name__)


@app.route('/')
def get_header():
    return render_template('start.html', title="robot", path="http://www.yoursite.com")


@app.route('/', methods=['POST'])
def get_data():
    try:
        scanned = request.cookies.get('scanning')
        if not scanned:
            site = Site(request.form['path'])
        else:
            now_time = datetime.datetime.now()
            past_time = datetime.datetime.strptime(scanned, "%Y-%m-%d %H:%M:%S.%f")
            seconds = (now_time-past_time).total_seconds()
            if seconds > 30:
                site = Site(request.form['path'])
            else:
                return render_template("wait.html", seconds=str(seconds)[:-5], path=request.form['path'])

    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason, path=request.form['path'])

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason, path=request.form['path'])

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e), path=request.form['path'])
    else:
        meta_data = zip(site.title,
                        site.title_length,
                        site.description,
                        site.description_length,
                        site.links)
        if not site.title_length == [] and not site.description_length == []:
            resp = make_response(render_template('result.html',
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
                                                 csv_file=site.file_string,
                                                 robot=site.robot_exclude_list
                                                 )
                                 )
            scan = datetime.datetime.now()
            resp.set_cookie('scanning', str(scan))
            return resp
        else:
            return render_template('noresults.html', path=request.form['path'])


@app.route('/scan/<path>')
def get_url(path):
    try:
        scanned = request.cookies.get('scanning')
        if not scanned:
            site = Site(path)
        else:
            now_time = datetime.datetime.now()
            past_time = datetime.datetime.strptime(scanned, "%Y-%m-%d %H:%M:%S.%f")
            seconds = (now_time-past_time).total_seconds()
            if seconds > 30:
                site = Site(path)
            else:
                return render_template("wait.html", seconds=str(seconds)[:-5], path=path)

    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason, path=request.form['path'])

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason, path=request.form['path'])

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e), path=request.form['path'])
    else:
        meta_data = zip(site.title,
                        site.title_length,
                        site.description,
                        site.description_length,
                        site.links)
        if not site.title_length == [] and not site.description_length == []:
            resp = make_response(render_template('result.html',
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
                                                 csv_file=site.file_string,
                                                 robot=site.robot_exclude_list
                                                 )
                                 )
            scan = datetime.datetime.now()
            resp.set_cookie('scanning', str(scan))
            return resp
        else:
            return render_template('noresults.html', path=path)


@app.route('/csv/<path>')
def export_csv(path):
    try:
        scanned = request.cookies.get('scanning')
        if not scanned:
            site = Site(path)
        else:
            now_time = datetime.datetime.now()
            past_time = datetime.datetime.strptime(scanned, "%Y-%m-%d %H:%M:%S.%f")
            seconds = (now_time-past_time).total_seconds()
            if seconds > 30:
                site = Site(path)
            else:
                return render_template("wait.html", seconds=str(seconds)[:-5], path=path)
    except HTTPError as e:
        return render_template('error.html', code=e.code, msg=e.reason, path=request.form['path'])

    except URLError as e:
        return render_template('error.html', code="", msg=e.reason, path=request.form['path'])

    except Exception as e:
        return render_template('error.html', code="", msg="sorry!: {0}".format(e), path=request.form['path'])
    else:
        if not site.title_length == [] and not site.description_length == []:
            resp = make_response(render_template('csv.html',
                                                 title="csv",
                                                 path=path,
                                                 csv_file=site.file_string
                                                 )
                                 )
            scan = datetime.datetime.now()
            resp.set_cookie('scanning', str(scan))
            return resp
        else:
            return render_template('noresults.html', path=path)


@app.route('/about')
def about():
    return render_template("about.html", title="about", path="http://www.yoursite.com")


@app.route('/thanks')
def thanks():
    return render_template("thanks.html", title="yay!", path="http://www.you-are-awesome.com")


if __name__ == '__main__':
    app.run()
