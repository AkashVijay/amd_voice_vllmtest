import xml.etree.ElementTree as ET
from datetime import datetime

def filter_by_date(xml_response: str, year_cutoff: int) -> dict:
    year_cutoff = int(year_cutoff)
    root = ET.fromstring(xml_response)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    filtered_papers = []

    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        published = entry.find('atom:published', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()

        try:
            pub_year = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ").year
            if pub_year > year_cutoff:
                filtered_papers.append({
                    "title": title,
                    "published": published,
                    "summary": summary
                })
        except Exception:
            continue

    return {"filtered": filtered_papers}



test_xml = """
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Paper A</title>
    <published>2023-05-01T00:00:00Z</published>
    <summary>This is a paper from 2023.</summary>
  </entry>
  <entry>
    <title>Paper B</title>
    <published>2015-06-01T00:00:00Z</published>
    <summary>This is a paper from 2015.</summary>
  </entry>
</feed>
"""

result = filter_by_date(test_xml, 2020)
print(result)