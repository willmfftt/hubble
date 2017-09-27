import re
import urllib2
from BeautifulSoup import BeautifulSoup
from matcher import Matcher


class PageScraper:

    def __init__(self, url):
        request = urllib2.Request(url)
        opener = urllib2.build_opener()
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        page = opener.open(request)
        self.__html = page.read()
        self.__soup = BeautifulSoup(self.__html)
        self.__url = url

    def get_all_anchor_links(self, internal_only = False):
        anchors = self.__soup.findAll("a")
        links = []

        for anchor in anchors:
            links.append(anchor.get("href"))

        links = self.__strip_bad_links(links)

        if not internal_only:
            return links
        else:
            internal_links = []
            for link in links:
                if Matcher.extract_domain_name(link) == \
                        Matcher.extract_domain_name(self.__url) or \
                                Matcher.extract_domain_name(link) is None:
                    internal_links.append(link)
            return internal_links

    def __strip_bad_links(self, links):
        good_links = []
        for link in links:
            if link is not None and link.startswith("#") is False:
                good_links.append(link)
        return good_links

    def get_non_anchor_links(self, internal_only = False):
        urls = re.findall('^(?!href)http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.__html)
        if not internal_only:
            return urls
        else:
            internal_links = []
            for url in urls:
                if Matcher.extract_domain_name(url) == \
                        Matcher.extract_domain_name(self.__url) or \
                                Matcher.extract_domain_name(url) is None:
                    internal_links.append(url)
            return internal_links

    def get_all_links(self, internal_only = False):
        links = []
        links += self.get_all_anchor_links(internal_only)
        links += self.get_non_anchor_links(internal_only)
        return self.__remove_duplicates(links)

    def get_all_onion_links(self, internal_only = False):
        onion_links = []
        links = self.get_all_links(internal_only)
        for link in links:
            if Matcher.is_onion_tld(link):
                onion_links.append(link)
        return onion_links

    def get_title(self):
        if self.__soup.title is None:
            return None
        else:
            return self.__soup.title.string

    def __remove_duplicates(self, links):
        clean_links = []
        for link in links:
            if link not in clean_links:
                clean_links.append(link)
        return clean_links
