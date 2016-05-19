import re
import urllib2
import itertools
import random
import time


def query_google(keywords, attempts=3):
    """
        Searches google or bing using all keywords.
        To prevent being blocked, we alternate between different headers,
        search engines, and delay a random amount of time before allowing
        another search.

        @param{list}{keywords} List of strings to search in google
        @param{int}{attempts} Number of total attempts to reach website in case of error.
                              Defaults to 3.
        @returns The HTML of the Google result page.
    """
    all_headers = ['Mozilla/5.0', 'Mozilla/5.0 (Windows NT 6.1) ', 'AppleWebKit/535.7 (KHTML, like Gecko)',
                   'Chrome/16.0.912.77', 'Safari/535.7']
    header = random.choice(all_headers)
    search_engines_texts = ['http://www.google.com/search?q=%s%%20salary',
                            'http://www.bing.com/search?q=%s%%20salary']
    search_url = random.choice(search_engines_texts)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', random.choice(header))]

    time.sleep(random.choice(xrange(5)) + random.random())
    for _ in xrange(attempts):
        try:
            return opener.open(search_url % '%20'.join(keywords)).read()
        except urllib2.URLError as e:
            print e
            if _ < attempts - 1:
                print 'Retrying query of keywords ', keywords
    print 'Could not query ', keywords
    return ''


def get_salary(text):
    """
        Gets the estimated salary from the HTML text

        Parameter:
        @:param{str}{text} - Estimate of the
        @:returns{int} - Estimated salary.
    """
    find_number = re.compile('(\$[0-9]{1,3},?[0-9]{3})|([0-9]{1,3},?[0-9]{3} +USD)')
    parse_number = re.compile("[\$, USD]+")

    number = find_number.search(text)
    # print text
    if number:
        return float(''.join(parse_number.split(number.group())))
    else:
        return None


def search_all_keywords(job_keywords, location_keywords):
    """
        Gets the estimated salary from using an average of all combinations of job keywords
        with the location
    """
    split_space = re.compile(' +')
    cleaned_job_keywords = list(set(filter(lambda x: len(x) > 1,
                                           map(lambda keyword: keyword.strip().strip(',/&:()'),
                                               job_keywords))))

    """
        If we get a result using all keywords, we stop.  Otherwise, we try removing i=1,2,3...
        keywords until we get a result.
    """
    nonzero_salaries = []
    for num_keywords in range(len(cleaned_job_keywords), 0, -1):
        for keyword_combo in itertools.combinations(cleaned_job_keywords, num_keywords):
            if len(location_keywords) > 0:
                for location in location_keywords:
                    split_locations = split_space.split(location)
                    salary = get_salary(query_google(list(keyword_combo) + split_locations))
                    if salary:
                        nonzero_salaries.append(salary)
                        print keyword_combo, location, salary
            else:
                salary = get_salary(query_google(keyword_combo))
                if salary:
                    nonzero_salaries.append(salary)
                    print keyword_combo, salary
        if len(nonzero_salaries) > 0:
            break
        # TODO: check in case salary information is available only when the location is omitted
    if len(nonzero_salaries) == 0:
        return -1.0
    else:
        return float(sum(nonzero_salaries)) / len(nonzero_salaries)


if __name__ == '__main__':
    print get_salary(query_google(['software', 'engineer']))
    print search_all_keywords(['head', 'software', 'engineer'], ['Boston, MA'])
    pass
