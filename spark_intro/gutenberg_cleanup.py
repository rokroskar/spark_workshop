import glob
import os
import re
import tempfile
import zipfile

from bs4 import BeautifulSoup

#
# `get_formatted_number` and `RdfParser` are from
# https://github.com/kiwix/gutenberg
#


def get_formatted_number(num):
    """
    Get a formatted string of a number from a not-predictable-string
    that may or may not actually contain a number.
    Append a BC notation to the number num with, if the
    number is negative.
    returns: a formatted string of the number, or num if
             num is not negative or None.
    """
    if not num:
        return None
    if all(['-' in num, num.replace('-', '').strip().isdigit()]):
        return ' '.join([num, 'BC'])
    return num


class RdfParser(dict):
    def __init__(self, rdf_data, gid):
        super().__init__()
        self['gid'] = gid
        for k in ['author_id', 'author_name', 'first_name', 'last_name']:
            self[k] = None
        self.rdf_data = rdf_data
        self.parse()

    def parse(self):
        soup = BeautifulSoup(self.rdf_data, 'xml')

        # The tile of the book: this may or may not be divided
        # into a new-line-seperated title and subtitle.
        # If it is, then we will just split the title.
        self['title'] = soup.find('dcterms:title')
        self['title'] = self['title'].text if self['title'] else '- No Title -'
        self['title'] = self['title'].split('\n')[0]
        self['subtitle'] = ' '.join(self['title'].split('\n')[1:])
        self['author_id'] = None

        # Parsing the name of the Author. Sometimes it's the name of
        # an organization or the name is not known and therefore
        # the <dcterms:creator> or <marcrel:com> node only return
        # "anonymous" or "unknown". For the case that it's only one word
        # `self['last_name']` will be null.
        # Because of a rare edge case that the field of the parsed author's name
        # has more than one comma we will join the first name in reverse, starting
        # with the second item.
        author = soup.find('dcterms:creator') or soup.find('marcrel:com')
        if author:
            self['author_id'] = author.find('pgterms:agent')
            self['author_id'] = self['author_id'].attrs[
                'rdf:about'].split('/')[-1] if 'rdf:about' in getattr(
                    self['author_id'], 'attrs', '') else None

            if author.find('pgterms:name'):
                self['author_name'] = author.find('pgterms:name')
                self['author_name'] = self['author_name'].text.split(',')

                if len(self['author_name']) > 1:
                    self['first_name'] = ' '.join(
                        self['author_name'][::-2]).strip()
                self['last_name'] = self['author_name'][0]

        # Parsing the birth and (death, if the case) year of the author.
        # These values are likely to be null.
        self['birth_year'] = soup.find('pgterms:birthdate')
        self['birth_year'] = self['birth_year'].text if self[
            'birth_year'] else None
        self['birth_year'] = get_formatted_number(self['birth_year'])

        self['death_year'] = soup.find('pgterms:deathdate')
        self['death_year'] = self['death_year'].text if self[
            'death_year'] else None
        self['death_year'] = get_formatted_number(self['death_year'])

        # ISO 639-3 language codes that consist of 2 or 3 letters
        try:
            self['language'] = soup.find('dcterms:language').find(
                'rdf:value').text
        except AttributeError:
            self['language'] = None

        # The download count of the books on www.gutenberg.org.
        # This will be used to determine the popularity of the book.
        self['downloads'] = soup.find('pgterms:downloads').text

        # The book might be licensed under GPL, public domain
        # or might be copyrighted
        self['license'] = soup.find('dcterms:rights').text

        # Finding out all the file types this book is available in
        file_types = soup.find_all('pgterms:file')
        self['file_types'] = {}
        for x in file_types:
            if not x.find('rdf:value').text.endswith('application/zip'):
                k = x.attrs['rdf:about'].split('/')[-1]
                v = x.find('rdf:value').text
                self['file_types'].update({k: v})


def clean_text(text):
    """Clean HTML tags, escape characters, special unicode, punctuation, and empty spaces from the raw html

    Inputs:
        `html_path`: path to the raw html Gutenberg project book file

    Outputs:
        a string of cleaned, lower-case text

    """

    # lower case
    text = text.lower()

    # define the regular expressions

    # remove escape characters
    text = re.sub('\r?\n|\r', ' ', text)

    # remove punctuation
    text = re.sub("[^a-zA-Z0-9\s'-]", '', text)

    # when returning, remove also the left and right space padding
    return text.strip()


def get_metadata(gid, rdf_lookup):
    """Extract the metadata from the Gutenberg book represented by the gid.

    Inputs:
        `gid`: the Gutenberg project book ID

        `rdf_lookup`: a dictionary mapping a gid to an rdf file path

    Outputs:
        dictionary containing the book metadata

    """
    gid = str(gid)

    with open(rdf_lookup[gid], encoding='utf-8') as f:
        rp = RdfParser(f.read(), gid)

    return rp


def get_rdf_lookup(rdf_path):
    """Generate a dictionary of (gid, path) mapping for the rdf files to make lookup faster"""

    rdf_lookup = {}
    find_gid = re.compile('(\d+)')
    for root, dirs, files in os.walk(rdf_path):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext == '.rdf':
                rdf_lookup[find_gid.findall(name)[0]] = os.path.join(root, f)
    return rdf_lookup


def extract_data(data_path, extract_path):
    """Extract .zip files from Gutenberg DVD archive located at `data_path` to `extract_path`"""
    i = 0
    for root, dirs, files in os.walk(data_path):
        target_dir = os.path.join(extract_path, '/'.join(root.split('/')[3:]))
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            if os.path.splitext(f)[1].lower() == '.zip':
                if not os.path.exists(
                        os.path.join(target_dir,
                                     os.path.splitext(f)[0] + '.txt')):
                    try:
                        with zipfile.ZipFile(os.path.join(root, f),
                                             "r") as zip_ref:
                            zip_ref.extractall(target_dir)
                            i += 1
                    except NotImplementedError:
                        pass

    print('Extracted %d files' % i)


def get_filelist(basepath, extension='.txt'):
    """Recursively generate a list of files of a given extension starting at `basepath`"""

    filter_filenames = re.compile('[\d-]+%s' % extension)
    find_8 = re.compile('.+(?=-\d\%s)' % extension)

    filelist = []
    for root, dirs, files in os.walk(basepath):
        for f in files:
            if filter_filenames.search(f) is not None:
                filelist.append(os.path.join(root, f))

    # remove the plain-text files when an 8-bit encoded file exists
    for f in filelist:
        f8 = find_8.findall(f)
        if len(f8) > 0:
            try:
                filelist.remove(f8[0] + extension)
            except ValueError:
                pass
    return filelist


def get_gid(filename):
    """
    Return the Gutenberg book ID (`gid`) give the path to the raw html file.

    Input:
        `html_path`: path to the html Gutenberg book file

    Output:
        `gid`: the ID of the Gutenberg book

    """
    return re.findall('(\d+)', os.path.basename(filename))[0]


def get_encoding(charset_string):
    """Return the string encoding."""
    encoding = re.findall('charset=(.+)', charset_string)
    if len(encoding) == 0:
        return 'utf-8'
    else:
        return encoding[0]


def read_file(filename, rdf_lookup):
    """Read the file with associated RDF metadata."""
    basename = os.path.basename(filename)

    try:  # if we don't find the metadata, drop the file
        rp = get_metadata(get_gid(filename), rdf_lookup)
        rp['filename'] = filename
    except Exception as e:
        print('Error loading metadata for ', basename)
        print(e)
        return None, None

    if basename in rp['file_types']:  # if no encoding is given, drop the file
        encoding = get_encoding(rp['file_types'][basename])
        try:
            with open(filename, encoding=encoding, errors='ignore') as f:
                text = f.read()
        except Exception as e:
            if isinstance(e, UnicodeError):
                print('UnicodeError while reading ', basename)
                return None, None
            else:
                raise RuntimeError(
                    "problems with decoding %s with encoding %s" % (filename,
                                                                    encoding))
        return rp, text
    else:
        print('metadata not found for ', basename)
        return None, None
