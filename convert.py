import json
from mistune import create_markdown
from mistune.core import BaseRenderer
from lxml import etree

class OdtRenderer(BaseRenderer):
    @staticmethod
    def heading(text, level):
        return f"<text:h text:style-name='Heading {level}' text:outline-level='{level}'>{text}</text:h>"

    @staticmethod
    def paragraph(text):
        return f'<text:p text:style-name="Text Body">{text}</text:p>'

    @staticmethod
    def softbreak():
        return "<text:line-break/>"

    @staticmethod
    def blank_line():
        return ''

    @staticmethod
    def block_text(text):
        return f'<text:p text:style-name="TextkörperAufzählung">{text}</text:p>'

    # SPAN LEVEL
    @staticmethod
    def text(text):
        return text

    @staticmethod
    def emphasis(text):
        return f'<text:span text:style-name="Emphasis">{text}</text:span>'

    @staticmethod
    def strikethrough(text):
        return f'<text:span text:style-name="Strikethrough">{text}</text:span>'

    @staticmethod
    def strong(text):
        return f'<text:span text:style-name="Strong Emphasis">{text}</text:span>'

    # LISTS
    @staticmethod
    def list(body, ordered, **attrs):
        style="Numbering 123" if ordered else "List 1"
        return f'<text:list text:style-name="{style}">{body}</text:list>'

    @staticmethod
    def list_item(text, **attrs):
        return f'<text:list-item>{text}</text:list-item>'

    # TABLES
    @staticmethod
    def table(text, cols=3):
        return f'''<table:table table:style-name="AdfinisTable">
<table:table-column table:number-columns-repeated="{cols}"/>
{text}</table:table>'''

    def table_head(self, text):
        return self.table_row(text)

    @staticmethod
    def table_body(text, cols=3):
        return f'''
<table:table-row table:style-name="AdfinisTable.1">
 <table:table-cell table:style-name="AdfinisTable.A2" office:value-type="string" table:number-columns-repeated="{cols}">
 </table:table-cell>
</table:table-row>{text}'''

    @staticmethod
    def table_row(text):
        return f'<table:table-row table:style-name="AdfinisTable.1">{text}</table:table-row>'

    @staticmethod
    def table_cell(text, align=None, head=False):
        cell_style = "A1" if head else "A2"
        p_style = "Heading" if head else "Contents"
        return f'''<table:table-cell table:style-name="AdfinisTable.{cell_style}" office:value-type="string">
<text:p text:style-name="Table {p_style}">{text}</text:p>
</table:table-cell>'''


md = """
## Markdown import

### Text

Regular Text. **Bold**, _italic_, ~~strikethrough~~.

Linebreak.

### Tables

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| First Header  | Second Header | Third Header  |
| ------------- | ------------- | ------------- |
| Content Cell  | Content Cell  | Content Cell  |
| Content Cell  | Content Cell  | Content Cell  |

| First Header  | Second Header | Third Header  | Fourth Header |
| ------------- | ------------- | ------------- | ------------- |
| Content Cell  | Content Cell  | Content Cell  | Content Cell  |
| Content Cell  | Content Cell  | Content Cell  | Content Cell  |

| First Header  | Second Header | Third Header  | Fourth Header | Fifth Header |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Content Cell  | Content Cell  | Content Cell  | Content Cell  | Content Cell  |
| Content Cell  | Content Cell  | Content Cell  | Content Cell  | Content Cell  |
"""

# ### Lists
# 
# Ordered:
# 
# 1. first
# 2. second
#     1. Sub 1
#     2. Sub 2
# 
# Unordered:
# 
# - foo
# - bar
#     - sub a
#     - sub b
# 
# Mixed:
# 
# 1. First
#     - sub A
#     - sub B
# 2. Second
#     - foo
#     - bar
# 
# - Point A
#     1. Step one
#     2. Step two
# - Point B

xml = create_markdown(renderer=OdtRenderer(), plugins=['strikethrough', 'table'])(md)
header = '<office:document xmlns:officeooo="http://openoffice.org/2009/office" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rpt="http://openoffice.org/2005/report" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:xforms="http://www.w3.org/2002/xforms" office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.text">'


x = etree.fromstring(header + xml + "</office:document>")

tree = etree.parse("adfinis.fodt")
parent = tree.xpath('//text()[. = "{{CONTENT}}"]/ancestor::text:p', namespaces={"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"})[0]
print(f"PARENT: {parent}")
for child in reversed(x.getchildren()):
    parent.addnext(child)
parent.getparent().remove(parent)
with open('out.fodt', 'wb') as f:
    tree.write(f, encoding='utf-8', xml_declaration=True)


ast = create_markdown(renderer=None)(md)
# print(json.dumps(ast, indent=4))
