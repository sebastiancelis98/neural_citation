import os

os.chdir('ncn')
print(os.getcwd())
#Update the neccessary assets when the MAG Database has been updated

exec(open("mag_cited_allquery.py").read())
exec(open("mag_citing_allquery.py").read())

os.chdir('..')
print(os.getcwd())

#Create dictionaries once query results have been saved locally
exec(open("generate_dicts.py").read())