from bs4 import BeautifulSoup
from urllib.request import urlopen


class Site:
    def __init__(self, path):
        self.path = path
        self.title = ""
        self.links = ""

        self.site = urlopen(str(self.path))
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
                pass

        # GET SOUP FROM SITES
        for site in self.sites:
            self.soups.append(BeautifulSoup(site, 'html.parser'))

        # GET IMPORTANT DATA FROM SITE
        for tags in self.soups:
            try:
                self.titles.append(tags.title.string)
                self.description.append(tags.find(attrs={"name": "description"})['content'])
            except Exception as e:
                pass

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
