from lxml import etree
from lxml import html as lxml_html
from lxml.html import clean, fromstring, tostring, _transform_result, copy

remove_attrs = ['class', 'width', 'cellspacing', 'cellpadding', 'border']
remove_tags = ['a', 'p', 'span', 'div', 'strong']
nonempty_tags = []

class MyCleaner(clean.Cleaner):
    def clean_html(self, html, parser=None):
        result_type = type(html)
        if isinstance(html, basestring):
            doc = fromstring(html, parser=parser)
        else:
            doc = copy.deepcopy(html)
        self(doc)
        return _transform_result(result_type, doc)

cleaner = MyCleaner(remove_tags=remove_tags, page_structure=False)

def squeaky_clean(html):
    parser = lxml_html.HTMLParser(encoding='utf-8')

    clean_html = cleaner.clean_html(html, parser)
    root = fromstring(clean_html)
    context = etree.iterwalk(root)

    for action, elem in context:
        clean_text = elem.text and elem.text.strip(' \t\r\n')

        if elem.tag in nonempty_tags and \
        not (len(elem) or clean_text):
            elem.getparent().remove(elem)
            continue
        elem.text = clean_text

        for badattr in remove_attrs:
            if elem.attrib.has_key(badattr):
                del elem.attrib[badattr]

    return tostring(root, encoding='ISO-8859-1')

with open("test.html") as myfile:
    DATA="".join(line.rstrip() for line in myfile)
    #html = squeaky_clean(DATA)
    #print html
    my_file = open("cleanfile.html", 'w')
    my_file.write(squeaky_clean(DATA))
    my_file.close()

print "...Save clean html to file cleanfile.html"