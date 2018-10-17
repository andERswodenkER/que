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
    return crawl_data(request.form['path'], "result", "post")


@app.route('/scan/<path>')
def get_url(path):
    return crawl_data(path, "scan", "scan")


@app.route('/csv/<path>')
def export_csv(path):
    return crawl_data(path, "csv", "csv")


@app.route('/about')
def about():
    return render_template("about.html", title="about", path="http://www.yoursite.com")


@app.route('/thanks')
def thanks():
    return render_template("thanks.html", title="yay!", path="http://www.you-are-awesome.com")


def crawl_data(path, title, option):
    if path == "":
        return render_template("start.html", path="http://www.yoursite.com")
    else:
        try:
            if not request.cookies.get('scanning'):
                scanned = ""
                seconds = ""
            else:
                scanned = request.cookies.get('scanning')
                now_time = datetime.datetime.now()
                past_time = datetime.datetime.strptime(scanned, "%Y-%m-%d %H:%M:%S.%f")
                seconds = (now_time - past_time).total_seconds()

            if not scanned or seconds > 30:
                site = Site(path)
            else:
                return render_template("wait.html", seconds=str(seconds)[:-5], path=path)

        except HTTPError as e:
            return render_template('error.html', code=e.code, msg=e.reason, path=path)

        except URLError as e:
            return render_template('error.html', code="", msg=e.reason, path=path)

        except Exception as e:
            return render_template('error.html', code="", msg="sorry!: {0}".format(e), path=path)
        else:
            meta_data = zip(site.title,
                            site.title_length,
                            site.description,
                            site.description_length,
                            site.links,
                            )
            if not site.title_length == [] and not site.description_length == []:
                if not option == "csv":
                    resp = make_response(render_template('result.html',
                                                         title=title,
                                                         path=path,
                                                         meta=meta_data,
                                                         site_errors=site.site_errors,
                                                         site_errors_counter=site.site_errors_counter,
                                                         site_counter=site.sites_counter,
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
                                                         image_todo=site.image_todo,
                                                         image_todo_counter=site.image_todo_counter,
                                                         csv_file=site.file_string,
                                                         robot=site.robot_exclude_list,
                                                         h1_dict=site.headline_h1,
                                                         h2_dict=site.headline_h2,
                                                         headline_warnings=site.headline_h1_warning,
                                                         headline_warning_dict=site.headline_h1_warning_dict
                                                         )
                                         )
                    scan = datetime.datetime.now()
                    resp.set_cookie('scanning', str(scan))
                    return resp
                else:
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


if __name__ == '__main__':
    app.run()
