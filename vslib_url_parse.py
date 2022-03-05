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

def putUrlListToFile(section, val_list):
    import pandas as pd
    import os
    import datetime 
    from jinja2 import Template
    import gzip
    
    data_list = []
    xx = 0
    max = int(len(val_list))
    print(xx,max)
    while xx < max:
        if type(val_list[xx]) == list:
            if int(len(val_list[xx])) == 6:
                print('lista 1:',val_list[xx])
                for v in val_list[xx]:
                    data_list.append(v)
            else:
                print('\t',type(val_list[xx]),len(val_list[xx]))
                for v in val_list[xx]:
                    data_list.append(v)
        else:
            print('string 1:',type(val_list[xx]),len(val_list[xx]))
            data_list.append(val_list[xx])

        xx+= 1
    
    
    xml_data = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" "
    xml_data+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    xml_data+= "xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 "
    xml_data+= "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">"


    # Import List of URLs
    list_of_urls = '\n'.join(data_list)
    list_of_urls
 
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
