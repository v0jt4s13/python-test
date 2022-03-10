import xml.etree.cElementTree as ET
import datetime

def registerSiteMaps():
	root = ET.Element('urlset')
	root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
	root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
	root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

	f = open('sitemap-urls.txt', 'r')
	urls_list = f.readlines()
 
	for doc in urls_list:
		#print(doc)
		site_root = doc
		dt = datetime.datetime.now().strftime ("%Y-%m-%d")
		doc = ET.SubElement(root, "url")
  	#for doc in q.results:
		#	uid = doc['uid']
		# site_root = uid.replace('__', '/').replace('_', '-')
		if "http" in site_root:
			ET.SubElement(doc, "loc").text = site_root
		else:
			ET.SubElement(doc, "loc").text = site_root
		ET.SubElement(doc, "lastmod").text = dt
		ET.SubElement(doc, "changefreq").text = "daily"
		ET.SubElement(doc, "priority").text = "1.0"

	tree = ET.ElementTree(root)
	tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)

def main(args):
	registerSiteMaps()

if __name__ == '__main__':
	main(sys.argv)