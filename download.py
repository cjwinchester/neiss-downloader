import urllib.request
import datetime
import os
import csv
from io import StringIO


# best I can tell, NEISS database starts with 1997
FIRST_YEAR = 1997

# assuming we're operating on a year lag -- might need to adjust
# depending on ~when~ you're running this script
LAST_YEAR = datetime.date.today().year - 1


def get_lookup_files():
    ''' grab the lookup TSV and parse it into separate lookup files '''

    # a TSV with all of the lookup codes lives here
    lookups_url = 'https://www.cpsc.gov/cgibin/NEISSQuery/Data/Info%20Docs/neiss_fmt.txt'  # noqa

    # grab that TSV and read it into memory
    response = urllib.request.urlopen(lookups_url)
    data = response.read()

    # decode bytes to utf-8 and wrap in a StringIO object
    text = StringIO(data.decode('utf-8'))
    print('got the lookups file')

    # feed that to a CSV reader object
    reader = csv.reader(text, delimiter='\t')

    # skip the headers
    next(reader)

    # an empty dictionary to hold the data before writing to file
    # goal: {'category': [['key', 'value'], ['key', value]] ...}
    d = {}

    # loop over the rows in the lookup file
    for row in reader:

        # the category -- what will eventually be the filename --
        # is in position 0
        category = row[0].lower()

        # the numeric code is in position 1
        code = int(row[1])

        # the value is in position 3, but it's almost always preceded
        # by the numeric code and a dash -- just want the value dawg
        value = row[3].split('-', 1)[-1].strip()

        # if we don't already have this key in the dict, add it
        # and set the value as an empty list
        if not d.get(category):
            d[category] = []

        # append a list with the code and value to that list
        d[category].append([code, value])

    # time to write the files!
    # loop over the dict
    for key in d:

        # build the filepath
        filepath = os.path.join('lookups', f'{key}.csv')

        # skip to the next one if we already have this file
        if os.path.isfile(filepath):
            continue

        # open file to write to
        with open(filepath, 'w') as outfile:

            # make a writer object
            writer = csv.writer(outfile)

            # write the headers
            writer.writerow(['code', 'value'])

            # iterate over the list for this category
            for item in d[key]:

                # and write out the row
                writer.writerow(item)

            # let us know what's up
            print(f'Wrote {filepath} lookup file')


def download_data_files(start_year=FIRST_YEAR, end_year=LAST_YEAR):
    ''' given a start and end year, download the NEISS files
        for that year
    '''

    # the data file URLs have a consistent template
    url_template = 'https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{}/neiss{}.tsv'  # noqa

    # loop over the year range
    for year in range(start_year, end_year+1):

        # build the file path
        local_file = os.path.join('data', f'neiss{year}.tsv')

        # check to see if we have this one already
        # if so, skip to the next year
        if os.path.isfile(local_file):
            continue

        # build the URL from the template
        url = url_template.format(year, year)

        # let us know what's up
        print(f'Downloading data file for {year} ...')

        # and download the file
        urllib.request.urlretrieve(url, local_file)

        # let us know what's up
        print(f'   Done!')


if __name__ == '__main__':
    get_lookup_files()
    download_data_files()
