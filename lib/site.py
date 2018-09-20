from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen


class Site:
    def __init__(self, path):
        self.path = path
        self.title = ""
        self.links = ""

        self.site = urlopen(str(self.path))q
        self.soup = BeautifulSoup(self.site, 'html.parser')

        self.sites = list()
        self.soups = list()

        self.titles = list()
        self.description = list()

        self.site_errors = list()

        self.title_errors = 0
        self.description_errors = 0

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

        # LINKS
        self.links_unsorted = list()
        for link in self.soup.find_all('a'):
            if link.get('href'):
                if link.get('href').startswith("/"):
                    self.links_unsorted.append(path + link.get('href'))
        self.links = sorted(set(self.links_unsorted), key=self.links_unsorted.index)

        # GET SITES
        for sites in self.links:
            try:
                self.sites.append(urlopen(sites))
                print("get data from: {0}".format(sites))
            except Exception as e:
                self.site_errors.append("{0} - {1}".format(sites, e))
                print(e)

        # GET SOUP FROM SITES
        for site in self.sites:
            self.soups.append(BeautifulSoup(site, 'html.parser'))

        # GET IMPORTANT DATA FROM SITE
        for tags in self.soups:
            try:
                self.titles.append(tags.title.string)
                self.description.append(tags.find(attrs={"name": "description"})['content'])
                self.author = tags.find(attrs={"name": "author"})['content']
                self.favicon = self.path + tags.find("link", rel="shortcut icon").get("href")
                self.apple_touch_icon = self.path + tags.find("link", rel="apple-touch-icon").get("href")
                self.apple_touch_title = tags.find(attrs={"name": "apple-mobile-web-app-title"})['content']
                self.keywords = tags.find(attrs={"name": "keywords"})['content']

            except Exception as e:
                print(e)
                pass

        # GET ERRORS
        for errors in self.soups:
            for img in errors.find_all('img', alt=False):
                self.image_alt_error_links_unsorted.append(self.path + img['src'])
            for comments in errors.find_all(string=lambda text: isinstance(text, Comment)):
                if "@todo" in str(comments):
                    self.todo.append(comments[6:])
                else:
                    self.comments_unsorted.append(comments)

        self.image_alt_error_links = sorted(set(self.image_alt_error_links_unsorted), key=self.image_alt_error_links_unsorted.index)
        self.comments = sorted(set(self.comments_unsorted), key=self.comments_unsorted.index)
        self.image_alt_error_counter = len(self.image_alt_error_links)
        self.comments_counter = len(self.comments)
        self.todo_counter = len(self.todo)

        # GET DESCRIPTION LENGTH
        for description in self.description:
            self.description_length.append(int(len(description)))
            if len(description) <= 1:
                self.description_errors += 1
            elif len(description) < 130:
                self.description_warnings += 1
            elif len(description) >= 160:
                self.description_warnings += 1

        # GET TITLE LENGTH
        for title in self.titles:
            self.title_length.append((int(len(title))))
            if len(title) < 1:
                self.title_errors += 1
            elif len(title) >= 60:
                self.title_warnings += 1
