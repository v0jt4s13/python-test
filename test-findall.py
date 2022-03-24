from re import findall
text = "Python is great for data visualization! Matplotlib is very fast and robust but lacks the aesthetic appeal. Seaborn library built over matplotlib has greatly improved the aesthetics and provides very sophisticated plots. However when it comes to scatter plots, these python libraries do not have any straight forward option to display labels of data points. This feature is available in other data visualization tools like Tableau and Power BI, with just a few clicks or hovering the pointer over the datapoints."
list_of_words = findall(r'[^\d\W]+',text)
list_of_words.sort(key=lambda x: x[0], reverse=True)  # czwarty element listy to długość listy słow
print(list_of_words)
print(list_of_words)
