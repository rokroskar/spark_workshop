
import glob, re, os
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

class RdfParser():
    def __init__(self, rdf_data, gid):
        self.rdf_data = rdf_data
        self.gid = gid

        self.author_id = None
        self.author_name = None
        self.first_name = None
        self.last_name = None

    def parse(self):
        soup = BeautifulSoup(self.rdf_data, 'lxml', from_encoding='utf-8')

        # The tile of the book: this may or may not be divided
        # into a new-line-seperated title and subtitle.
        # If it is, then we will just split the title.
        self.title = soup.find('dcterms:title')
        self.title = self.title.text if self.title else '- No Title -'
        self.title = self.title.split('\n')[0]
        self.subtitle = ' '.join(self.title.split('\n')[1:])
        self.author_id = None

        # Parsing the name of the Author. Sometimes it's the name of
        # an organization or the name is not known and therefore
        # the <dcterms:creator> or <marcrel:com> node only return
        # "anonymous" or "unknown". For the case that it's only one word
        # `self.last_name` will be null.
        # Because of a rare edge case that the field of the parsed author's name
        # has more than one comma we will join the first name in reverse, starting
        # with the second item.
        self.author = soup.find('dcterms:creator') or soup.find('marcrel:com')
        if self.author:
            self.author_id = self.author.find('pgterms:agent')
            self.author_id = self.author_id.attrs['rdf:about'].split('/')[-1] if 'rdf:about' in getattr(self.author_id, 'attrs', '') else None

            if self.author.find('pgterms:name'):
                self.author_name = self.author.find('pgterms:name')
                self.author_name = self.author_name.text.split(',')

                if len(self.author_name) > 1:
                    self.first_name = ' '.join(self.author_name[::-2]).strip()
                self.last_name = self.author_name[0]

        # Parsing the birth and (death, if the case) year of the author.
        # These values are likely to be null.
        self.birth_year = soup.find('pgterms:birthdate')
        self.birth_year = self.birth_year.text if self.birth_year else None
        self.birth_year = get_formatted_number(self.birth_year)

        self.death_year = soup.find('pgterms:deathdate')
        self.death_year = self.death_year.text if self.death_year else None
        self.death_year = get_formatted_number(self.death_year)

        # ISO 639-3 language codes that consist of 2 or 3 letters
        try : 
            self.language = soup.find('dcterms:language').find('rdf:value').text
        except AttributeError : 
            self.language = None

        # The download count of the books on www.gutenberg.org.
        # This will be used to determine the popularity of the book.
        self.downloads = soup.find('pgterms:downloads').text

        # The book might be licensed under GPL, public domain
        # or might be copyrighted
        self.license = soup.find('dcterms:rights').text

        # Finding out all the file types this book is available in
        file_types = soup.find_all('pgterms:file')
        self.file_types = {}
        for x in file_types:
            if not x.find('rdf:value').text.endswith('application/zip'):
                k = x.attrs['rdf:about'].split('/')[-1]
                v = x.find('rdf:value').text
                self.file_types.update({k:v})

        return self



def get_text(html_path) :
    """Clean HTML tags, escape characters, special unicode, punctuation, and empty spaces from the raw html"""
    
    with open(html_path) as f : 
        source = f.read()
    
    # lower case
    source = source.lower()
    
    # define the regular expressions
    
    # remove tags and punctuation 
    no_tags = re.compile('<.*>')
    cleaned = no_tags.sub('',source)
    
    # remove escape characters
    no_escape = re.compile('\r?\n|\r')
    cleaned = no_escape.sub(' ', cleaned)
   
    # replace umlauts
    a_uml = re.compile('\\xc3\\xa4')
    cleaned = a_uml.sub('ae', cleaned)

    o_uml = re.compile('\\xc3\\xb6')
    cleaned = o_uml.sub('oe', cleaned)

    u_uml = re.compile('\\xc3\\xbc')
    cleaned = u_uml.sub('ue', cleaned)

    # remove all non-ascii
    no_non_ascii = re.compile('[^\x00-\x7F]+')
    cleaned = no_non_ascii.sub(' ', cleaned)
    
    # remove punctuation
    no_punctuation = re.compile('[^a-zA-Z0-9\s]')
    cleaned = no_punctuation.sub('', cleaned)
    
    # remove numbers
    no_numbers = re.compile('[0-9]+')
    cleaned = no_numbers.sub('', cleaned)
   
    # remove empty white space and numbers
    no_empty_space = re.compile('\s+')
    cleaned = no_empty_space.sub(' ', cleaned) 
     
    # when returning, remove also the left and right space padding
    return cleaned.strip()

def get_gid(html_path) : 
    digits = re.compile('[0-9]+')
    gid = digits.findall(os.path.splitext(os.path.basename(html_path))[0])[0]
    return int(gid)

def get_metadata(gid, rdf_path = '/cluster/home03/sdid/roskarr/work/gutenberg/rdf-files/') :
    """Extract the metadata from the appropriate RDF file"""

    gid = str(gid)

    rdf_file = glob.glob(rdf_path+gid+'/*')[0]

    with open(rdf_file) as f :
        rdf_data = f.read() 

    rp = RdfParser(rdf_data, gid).parse()

    return {'gid': int(rp.gid), 'title': rp.title, 
            'first_name': rp.first_name, 'last_name': rp.last_name, 
            'birth_year': rp.birth_year, 'death_year': rp.death_year, 
            'lang': rp.language, 'downloads': rp.downloads}

    #return "%d||%s||%s||%s||%s||%s"%(int(rp.        gid), rp.title,rp.first_name,rp.last_name,rp.birth_year,rp.death_year)


