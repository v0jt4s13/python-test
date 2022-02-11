# importing the module
import json

{'ListaDomen':[{'domena': 'http://etyczne-dziennikarstwo.pl', 'data': [{'id': 1, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://telusmikolaj.com', 'data': [{'id': 2, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://adrianeight.tech', 'data': [{'id': 3, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://pythonistaxd.pl', 'data': [{'id': 4, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://aws.programista.warszawa.pl', 'data': [{'id': 5, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://animuscreations.pl', 'data': [{'id': 6, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://t-mike.pl', 'data': [{'id': 7, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://wurcu.pl', 'data': [{'id': 8, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://karolina-jedrzejak.com.pl', 'data': [{'id': 9, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}, {'domena': 'http://brownmilleryt.pl', 'data': [{'id': 10, 'status_code': 200, 'description': 'Status code dla domeny', 'extra': 200}]}]},{'IloscDomen':10},{'Status200':10},{'Statusy':[200]},{'BledneDomeny':[]} 
json_str = {
    'ListaDomen':[
        {
            'domena': 'http://etyczne-dziennikarstwo.pl', 
            'data':{
                    'id': 1, 
                    'status_code': 200, 
                    'description': 'Status code dla domeny', 
                    'extra': 200
                }
        }, {
            'domena': 'http://telusmikolaj.com', 
            'data':{
                    'id': 2, 
                    'status_code': 200, 
                    'description': 'Status code dla domeny', 
                    'extra': 200
                }
        }, {
            'domena': 'http://adrianeight.tech', 
            'data':{
                    'id': 3, 
                    'status_code': 200, 
                    'description': 'Status code dla domeny', 
                    'extra': 200
                }
        }
    ],
    'IloscDomen':759,
    'Status200':728,
    'Statusy':[200, 502, 404, 500],
    'BledneDomeny':[
            {"502": 'http://obiekt-626.pl'},
            {"404": 'http://mi-st.pl'},
            {"502": 'http://mkrzem.pl'},
            {"502": 'http://andzejem.pl'},
            {"500": 'http://aleksandra-zochowska.pl'}
    ]
}

# Opening JSON file
with open('test_test_file.json') as json_file:
    data = json.load(json_file)
 
    # for reading nested data [0] represents
    # the index value of the list
    print(data['people1'][0])
     
    # for printing the key-value pair of
    # nested dictionary for loop can be used
    print("\nPrinting nested dictionary as a key-value pair\n")
    for i in data['people1']:
        print("Name:", i['name'])
        print("Website:", i['website'])
        print("From:", i['from'])
        print()