import xml.etree.ElementTree as ET


doc1 = ET.XML('''
    <root>
      <element1>
      </element1>
    </root>
    ''')

request = ET.XML('''
    <request>
      <dummyValue>5</dummyValue>
    </request>
    ''')

for element1 in doc1.findall('element1'):
    element1.append(request)

ET.dump(doc1)
