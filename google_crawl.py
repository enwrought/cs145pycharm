import re
import urllib2


def query_google(keywords):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    return opener.open('http://www.google.com/search?q=%s%%20salary' % '%20'.join(keywords)).read()


def parse_html_file(text):
    """
        Gets the estimated salary from the HTML text

        Parameter:
        @:param{str}{text} - Estimate of the
        @:returns{int} - Estimated salary.
    """
    find_number = re.compile('(\$[0-9]{1,3},?[0-9]{3})|([0-9]{1,3},?[0-9]{3} +USD)')
    parse_number = re.compile("[\$, USD]+")

    number = find_number.search(text)
    print text
    if number:
        return float(''.join(parse_number.split(number.group())))
    else:
        return None


if __name__ == '__main__':
    print parse_html_file(query_google(['software', 'engineer']))
    pass
