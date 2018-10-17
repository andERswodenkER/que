from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib.robotparser as urobot
import tldextract
import csv
import random
from tqdm import tqdm
from socket import timeout


class Site:
    def __init__(self, path):
        self.path = self.validate_url(path)
        self.rp = urobot.RobotFileParser()
        self.rp.set_url(self.path + "/robots.txt")
        try:
            self.rp.read()
        except Exception:
            self.rp = ""

        self.file_string = ""

        self.links = ""

        self.robot_exclude_list = list()

        self.site = urlopen(str(self.path))
        self.soup = BeautifulSoup(self.site, 'html.parser')

        self.sites = list()
        self.sites_counter = 0
        self.soups = list()

        self.title = list()
        self.description = list()

        self.site_errors = list()
        self.site_errors_counter = 0

        self.title_errors = 0
        self.description_errors = 0

        self.headline_h1 = dict()
        self.headline_h2 = dict()

        self.headline_h1_warning = 0
        self.headline_h1_warning_dict = dict()

        self.title_warnings = 0
        self.description_warnings = 0

        self.description_length = list()
        self.title_length = list()

        self.keywords = ""

        self.author = ""
        self.favicon = ""
        self.apple_touch_icon = ""
        self.apple_touch_title = ""

        self.image_alt_error_links_unsorted = list()
        self.image_alt_error_links = list()
        self.image_alt_error_counter = 0

        self.comments = list()
        self.comments_unsorted = list()
        self.comments_counter = 0

        self.todo = list()
        self.todo_counter = 0

        self.image_todo = list()
        self.image_todo_counter = 0

        self.links_unsorted = list()

        self.get_links()

        self.get_sites()

        self.get_meta_data()

        self.get_headlines()

        self.get_title_length()

        self.get_description_length()

        self.get_comment_errors()

        self.get_image_errors()

        self.write_csv()

    @staticmethod
    def sorting(unsorted_list):
        sorted_list = sorted(set(unsorted_list), key=unsorted_list.index)

        return sorted_list

    def get_sites(self):
        for sites in tqdm(self.links):
            try:
                if self.rp == "":
                    try:
                        self.sites.append(urlopen(sites))
                    except:
                        pass
                else:
                    if self.rp.can_fetch("*", sites):
                        try:
                            self.sites.append(urlopen(sites, timeout=0.5))
                        except timeout:
                            print("to long!")
                    else:
                        self.robot_exclude_list.append(sites)

            except Exception as e:
                self.site_errors.append("{0} - {1}".format(sites, e))

        for site in self.sites:
            self.soups.append(BeautifulSoup(site, 'html.parser'))

        self.site_errors_counter = len(self.site_errors)
        self.sites_counter = len(self.sites)

    def get_links(self):
        try:
            for link in self.soup.find_all('a'):
                if link.get('href'):
                    if link.get('href').startswith("/") and not link.get('href')[-3:] == "pdf":
                        self.links_unsorted.append(self.path + link.get('href'))
            self.links = self.sorting(self.links_unsorted)

        except Exception as e:
            pass

    def get_meta_data(self):
        for tags in self.soups:
            try:
                self.title.append(tags.title.string)
                self.description.append(tags.find(attrs={"name": "description"})['content'])
                self.author = tags.find(attrs={"name": "author"})['content']
                self.favicon = self.path + tags.find("link", rel="shortcut icon").get("href")
                self.apple_touch_icon = self.path + tags.find("link", rel="apple-touch-icon").get("href")
                self.apple_touch_title = tags.find(attrs={"name": "apple-mobile-web-app-title"})['content']
                self.keywords = tags.find(attrs={"name": "keywords"})['content']

            except Exception as e:
                pass

    def get_headlines(self):
        for tags in self.soups:
            for h1 in tags.find_all('h1'):
                if tags.title.string in self.headline_h1:
                    self.headline_h1[tags.title.string].append(h1.getText())
                else:
                    self.headline_h1[tags.title.string] = [h1.getText()]

            if not tags.find('h1'):
                self.headline_h1_warning += 1
                self.headline_h1_warning_dict[tags.title.string] = True
            else:
                self.headline_h1_warning_dict[tags.title.string] = False

            for h2 in tags.find_all('h2'):
                if tags.title.string in self.headline_h2:
                    self.headline_h2[tags.title.string].append(h2.getText())
                else:
                    self.headline_h2[tags.title.string] = [h2.getText()]

    def get_image_errors(self):
        for errors in self.soups:
            for img in errors.find_all('img', alt=False):
                self.image_alt_error_links_unsorted.append(self.path + img['src'])
            for img in errors.find_all("img", alt="@todo"):
                self.image_todo.append(self.path + img['src'])

        self.image_alt_error_links = self.sorting(self.image_alt_error_links_unsorted)
        self.image_alt_error_counter = len(self.image_alt_error_links)
        self.image_todo_counter = len(self.image_todo)

    def get_comment_errors(self):
        for errors in self.soups:
            for comments in errors.find_all(string=lambda text: isinstance(text, Comment)):
                if "@todo" in str(comments):
                    self.todo.append(comments[6:])
                else:
                    self.comments_unsorted.append(comments)
        self.comments = self.sorting(self.comments_unsorted)
        self.comments_counter = len(self.comments)
        self.todo_counter = len(self.todo)

    def get_description_length(self):
        for description in self.description:
            self.description_length.append(int(len(description)))
            if len(description) <= 1:
                self.description_errors += 1
            elif len(description) < 130:
                self.description_warnings += 1
            elif len(description) >= 160:
                self.description_warnings += 1

    def get_title_length(self):
        for title in self.title:
            self.title_length.append((int(len(title))))
            if len(title) < 1:
                self.title_errors += 1
            elif len(title) >= 60:
                self.title_warnings += 1

    @staticmethod
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

    def write_csv(self):
        hash_value = random.getrandbits(16)
        self.file_string = str(self.path)[11:-4] + str(hash_value)
        with open('static/{0}.csv'.format(self.file_string), 'w', newline='') as csvfile:
            seo_writer = csv.writer(csvfile,  delimiter=",")
            seo_writer.writerow(["Link"] + ["Title"] + ["Description"])
            for link, title, description in zip(self.links, self.title, self.description):
                seo_writer.writerow([link] + [title] + [description])