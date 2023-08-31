import re
import json
from lxml import etree
incorrect_value = ('None', 'null', '0', '0.0', '.0', '-', '——', '—', '— ', '0.00', '---', '--', ' -')


def parse(raw_data: str):
    root = etree.XML(raw_data)
    ret = {}
    ele = root.find('.//Composite/SubItems')
    for e in ele.iter():
        if e.tag in ['MIDateTime', 'MIString', 'MINumber']:
            name = e.find('Code')
            if name is not None:
                value = e.find('Value')
                display_name = name.get('DisplayName')
                code = name.get('Code')
                ret[display_name or code] = value.text if value is not None else None
                if e.tag == 'MINumber':
                    ret[code] = value.text if value is not None else None

        if e.tag in ['MIDictionary', 'MIMonoChoice']:
            name = e.find('Code')
            if name is not None:
                value = e.find('Value/Choice')
                display_name = name.get('DisplayName')
                field_code = name.get('Code')
                ret[field_code] = value.get('Code') if value is not None else None
                if display_name:
                    ret[display_name] = value.get('DisplayName') if value is not None else None
                    ret[f"{display_name}_code"] = value.get('Code') if value is not None else None

        if e.tag == 'MIConcept':
            code = e.find('SubItems/MIImage/Code')
            value = e.find('SubItems/MIImage/Value')
            if code is not None:
                ret[code.get('Code')] = value.text
    return ret

# CMS_V_BA
with open('/Users/weibo/Code/test/python/xml/楚雄xml模板.xml') as f:
    all_xml_data = f.read()
s1 = re.compile(r'(.*)(?P<XML><ScatterData>.*</ScatterData>)', re.M | re.S)
m = s1.match(all_xml_data)
data_str = m.group('XML')
new_ba = parse(data_str) if data_str else {}
print(new_ba)
with open('./result.json', 'w') as f:
    f.write(json.dumps(new_ba, ensure_ascii=False, indent=4))
