import tldextract
import logging
import sys

class Matcher:

    @staticmethod
    def extract_domain_name(url):
        extracted = tldextract.extract(url)
        if extracted.domain == "" or extracted.suffix =="":
            return None
        else:
            return "{}.{}".format(extracted.domain, extracted.suffix)

    @staticmethod
    def extract_subdomain(url):
        extracted = tldextract.extract(url)
        return extracted.subdomain

    @staticmethod
    def is_onion_tld(url):
        # Just to shut up tldextract from complaining about no logger
        logging.basicConfig(stream=sys.stdout, level=logging.FATAL)
        extracted = tldextract.extract(url)
        return extracted.suffix == "onion"
