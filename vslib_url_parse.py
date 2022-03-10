import urllib.parse as urlparse

def parseUrlChangeParamValue(link,query_para,query_para_new_value):
    new_link = link
    #print(type(link),link)
    link_list = link.split('?')
    if len(link_list) == 2:
        parsed = urlparse.urlparse(link)
        querys = parsed.query.split("&")
        new_querys_list = []
        for val in querys:
            para = val.split('=')[0]
            if para == query_para:
                new_querys_list.append(para+"="+str(query_para_new_value))
            else:
                new_querys_list.append(val)
        new_query = '&'.join(new_querys_list)
        new_link = link_list[0]+"?"+new_query

    #print('***przed******>>>',link)
    #print('*****po****>>>',new_link)
    return new_link

#link = "http://website.url" #?cat=1&start=1"
#parseUrlChangeParamValue(link,'start',5)

def putUrlListToFile(section, data_list):
    import pandas as pd
    import os
    import datetime 
    from jinja2 import Template
    import gzip
    from moje_biblioteki import removeDuplicatesFromList
    
    #<?xml version="1.0" encoding="utf-8"?>
    #<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    #<url><loc>https://www.haikson.com</loc></url>
    #<url><loc>https://www.haikson.com/static/css/bootstrap.min.css</loc></url>
    #</urlset>

    xml_data = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" "
    xml_data+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    xml_data+= "xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 "
    xml_data+= "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">"

    new_url_list = []
    # Import List of URLs
    #print(len(data_list),type(data_list))
    xx = 0
    while xx < len(data_list):
        #print(xx,type(data_list[xx]),len(data_list[xx]))
        if len(data_list[xx]) > 0 and type(data_list[xx]) == list:
            for tmp_url in data_list[xx]:
                if type(tmp_url) == str:
                    new_url_list.append(tmp_url)
                else:
                    print('Wartosc nie jest stringiem. => ',type(tmp_url))
                    print(str(tmp_url))
        elif len(data_list[xx]) > 0:
            #print('=====>',data_list[xx])
            new_url_list.append(data_list[xx])
        else:
            print('Wartosc jest pusta.')
        
        xx+= 1
    
    #print(len(new_url_list))
    #removeDuplicatesFromList(new_url_list)
 
    deduplicated_list = list(set(new_url_list))
    print('Reduce duplicates from:',len(new_url_list),' to:',len(deduplicated_list))
    #list_of_urls = '\n'.join(new_url_list)
    list_of_urls = deduplicated_list
    list_to_remove = []
    for url in list_of_urls:
        if "https" not in url:
            list_to_remove.append(url)
    if len(list_to_remove) > 0:
        for url in list_to_remove:
            list_of_urls.remove(url)
        
    if len(list_of_urls) < 150:
        for url in list_of_urls:
            print(url)

    with open('sitemap-urls.txt', 'w') as f:
        for item in list_of_urls:
            f.write("%s\n" % item)
    
    raise SystemExit

    list_of_urls = pd.DataFrame(["https://londynek.net/", "https://londynek.net/link1", "https://londynek.net/link2"],
     columns=['name'])
    
    # Set-Up Maximum Number of URLs (recommended max 50,000)
    n = 50000
 
    # Create New Empty Row to Store the Splitted File Number
    list_of_urls.loc[:,'name'] = ''
        
    # Split the file with the maximum number of rows specified
    new_df = [list_of_urls[i:i+n] for i in range(0,list_of_urls.shape[0],n)]
 
    # For Each File Created, add a file number to a new column of the dataframe
    for i,v in enumerate(new_df):
        v.loc[:,'name'] = str(v.iloc[0,1])+'_'+str(i)
        print(v)
             
    # Create a Sitemap Template to Populate
 
    sitemap_template='''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {% for page in pages %}
        <url>
            <loc>{{page[1]|safe}}</loc>
            <lastmod>{{page[3]}}</lastmod>
            <changefreq>{{page[4]}}</changefreq>
            <priority>{{page[5]}}</priority>        
        </url>
        {% endfor %}
    </urlset>'''
 
    template = Template(sitemap_template)
 
    # Get Today's Date to add as Lastmod
    lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')
 
    # Fill the Sitemap Template and Write File
    for i in new_df:                           # For each URL in the list of URLs ...                                                          
        i.loc[:,'lastmod'] = lastmod_date      # ... add Lastmod date
        i.loc[:,'changefreq'] = 'daily'        # ... add changefreq
        i.loc[:,'priority'] = '1.0'            # ... add priority 
    
        # Render each row / column in the sitemap
        sitemap_output = template.render(pages = i.itertuples()) 
        
        # Create a filename for each sitemap like: sitemap_0.xml.gz, sitemap_1.xml.gz, etc.
        filename = 'sitemap' + str(i.iloc[0,1]) + '.xml.gz'
 
        # Write the File to Your Working Folder
        with gzip.open(filename, 'wt') as f:   
            f.write(sitemap_output)
        

def qq():

    data_list = []
    
    data_style = "<style>.domena{margin-right:20px;}.status-code{margin-right:20px;}.status-code2{margin-right:20px;}</style>"
    data_head = "<head><html>%s</html><body>" %data_style
    data_footer = "</body></html>"
    #print(type(data_list))
    #print(len(data_list))
    data_str = ''.join(data_list)

    with open('londynek-url-finder.html','w') as file:
        file.write(data_head)
        file.write(data_str)
        file.write(data_footer)
