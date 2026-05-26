import pandas as pd
import numpy as np
import math

bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')

# print(bios)

# print(bios.info())

'''print(bios.loc[
    bios[
        'height_cm']>215,
        ['name','height_cm','NOC']
    ].sort_values([
        'NOC',
        'height_cm'
]))'''

'''coffee = pd.read_csv('complete-pandas-tutorial/warmup-data/coffee.csv')
coffee['price'] = 3.99
coffee['new_price'] = np.where(coffee['Coffee Type'] == 'Espresso',3.99,5.99)
print(coffee)
print('Edited:')
coffee.drop(columns = ['price'], inplace = True)
print(coffee)
coffee.rename(columns = {
    'new_price':'price'
},inplace=True)
print('Edited:')
print(coffee)
print("latte: ")
latte = coffee.query('`Coffee Type` == "Latte"')
print(latte)'''


'''bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')

bios["Birth Year"] = pd.to_datetime(bios["born_date"]).dt.year
print(bios[['name','born_date',"Birth Year"]])'''

'''bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')
bios['height_catagory'] = bios['height_cm'].apply(lambda x: 'Short' if x <165 else ('Average' if x<185 else ('Tall' if not np.nan else math.nan)))
print(bios)'''

'''bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')

nocs = pd.read_csv('complete-pandas-tutorial/data/noc_regions.csv')

bios = pd.merge(bios,nocs,left_on='born_country',right_on='NOC',how='left',suffixes=['bios','noc'])
bios.rename(columns = {'region' : 'born_country_full'},inplace=True)

usa = bios[bios['born_country'] == 'USA'].copy()
gbr = bios[bios['born_country'] == 'GBR'].copy()
result = pd.concat([usa,gbr])

new_bios = pd.merge(bios,result,on='athlete_id',how='right')
print(new_bios)'''

'''coffee = pd.read_csv('complete-pandas-tutorial/warmup-data/coffee.csv')
coffee.loc[[0,1],'Units Sold'] = np.nan
print(coffee.fillna(1000))'''

'''bios =pd.read_csv('complete-pandas-tutorial/data/bios.csv')
print(bios[bios['born_country'] == 'USA']['born_region'].value_counts())'''

'''bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')
born_date = pd.to_datetime(bios['born_date']) 
bios['year_born'] = born_date.dt.year
bios['months_born'] = born_date.dt.month
db = bios.groupby([
    bios['year_born'],
    bios['months_born']
    ])['name'].count().reset_index().sort_values('name').reset_index()
print(db)'''

bios = pd.read_csv('complete-pandas-tutorial/data/bios.csv')