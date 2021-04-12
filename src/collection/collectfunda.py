#!/usr/bin/env python
# coding: utf-8

# <h1>FUNDA SCRAPER TEAM 02<h1>

# In[1]:


#import libraries
import selenium.webdriver
from time import sleep
import pandas as pd
from tqdm import tqdm
import json
import time


# In[2]:


def connect(link):
    global driver
    #create driver, navigate to funda and accept cookies
    driver = selenium.webdriver.Chrome()
    driver.get(link)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()


# In[3]:


connect('https://www.funda.nl/koop/INSERT CITYNAME HERE/verkocht/sorteer-afmelddatum-af/') 

#if Funda detects Selenium, you might need to fill in the reCAPTCHA verification
sleep(2)
if driver.find_element_by_xpath('/html/body/div[3]/div/div/div/p').text == 'Fout bij het laden van de pagina. Probeer het opnieuw.':
    driver.refresh()
    print("PLEASE FILL IN reCAPTCHA")


# In[ ]:


#IMPORTANT NOTE: Make sure the inspector is closed and the Funda page is on full screen when running following codes!


# <h5> Create list of links <h5>

# In[4]:


#Scrape all links of all houses on Funda
def build_pages_urls():
    #create empty addresslist_links
    addresslist_links= []
    #setup condition for page navigation
    condition=True
    while condition: 
        address_list= driver.find_elements_by_class_name("search-result__header-title-col")
        for address in address_list:
            aaa1= address.find_element_by_tag_name('a')
            addresslist_links.append(aaa1.get_property('href')) #find all urls to click on
    #pagination
        try:
            kk=driver.find_element_by_class_name("pagination").find_elements_by_tag_name('a')[-1] 
            if kk.get_attribute('rel')== 'next':
                kk.click() #if there is a 'next' attribute: click, otherwise condition=False (breaks loop)
            else:
                condition=False
        except:
            condition=False
        sleep(4)
    
    #return list with links
    return(addresslist_links)


# In[5]:


#Store addresslist in variable 'my_urls'
my_urls= build_pages_urls()


# <h5> Check if len(my_urls) matches the total number of houses on the page <h5>

# In[ ]:


print('Total houses on page = ' + driver.find_element_by_xpath('//*[@id="content"]/form/div[2]/div[3]/div[1]/div[1]/h1/span').text)
print('# of links in my_url = ' + str(len(my_urls)))


# In[ ]:


#STORE ADDRESSLIST IN CSV
#my_urls_df = pd.DataFrame(my_urls0
#my_urls_df.to_csv (r"path where you want to save/nameofcsv.csv"), index= False, header=True)


# <h5> Define how to get all house data <h5>
#     

# In[125]:


#retrieve all info from housepage
def get_productdata(url):
    driver.get(url)
    sleep(2)
    
    #retrieve all values (€215.000, 10m2 etc.)
    values_list= []
    address= driver.find_elements_by_class_name("object-header__title")
    for adr in address:
        values_list.append(adr.text)
    values= driver.find_elements_by_tag_name("dd")
    #exclude values that cause misalignment
    exclude= driver.find_elements_by_class_name('object-kenmerken-group-list') 
    excludelist= []
    for i in exclude:
        excludelist.append(i.text)
    for val in values:
        if val.text not in excludelist:
                values_list.append(val.text)
    if 'Onbekend' in values_list: values_list.remove('Onbekend')
    if 'Kadastrale kaart' in values_list: values_list.remove('Kadastrale kaart')
    if "" in values_list: values_list.remove("")
    
    #retrieve all elements ('Price', 'Surface', etc.)
    elements_list= []
    elements_list.append('Adres')
    elements= driver.find_elements_by_tag_name("dt")
    #exclude elements that cause misalignment
    exclude_elements= driver.find_elements_by_class_name('kadaster-title') 
    exclude_elements_list= []
    for j in exclude_elements:
        exclude_elements_list.append(j.text)
    for el in elements:
        if el.text not in exclude_elements_list:
                elements_list.append(el.text)
    if 'Gebruiksoppervlakten' in elements_list: elements_list.remove( 'Gebruiksoppervlakten')
    
    jsondict= dict(zip(elements_list, values_list))
    
    #return json dictionary with elements and their associated values
    return(jsondict)
    
    


# <h5> Scraper <h5>

# In[121]:


def scrape_funda():
    for i in tqdm(my_urls):
        driver.get(i)
        my_json = get_productdata(i)
        f = open('CITYNAME.json', 'a', encoding= "utf-8")
        f.write(json.dumps(my_json)+'\n')
        f.close()


# In[ ]:


scrape_funda()


# In[124]:


#CONVERT YOUR .JSON TO CSV
df= pd.read_json('PATH TO JSON', lines= True)
df.to_csv('PATH TO CSV STORING LOCATION/CITYNAME.csv')

