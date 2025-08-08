import pandas

data = {'Name': ['Jack','Tony','Sophia','Aaron','Sonya'], 'Spiderman': ['4/10',"5/10","3/10", "10/10", "9/10"], 'Mario Movie': ['3/10', "10/10", "3/10", "9/10", "8/10"], 'Minecraft Movie': ['3/10', "1/10", "3/10", "10/10", "8/10"], 'Pokemon': ['10/10', "10/10", "10/10", "2/10", "4/10"], "Ninjago": ['10/10', "10/10", "10/10", "10/10", "2/10"]}

print(data)

dataframe1 = pandas.DataFrame(data)
print(dataframe1)