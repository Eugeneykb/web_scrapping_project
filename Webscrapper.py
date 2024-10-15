# Import the Necessary Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait, Select
import csv
import time
import uuid
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
s = Service('C:/Users/HP/Documents/DATA ENGINEERING BOOTCAMP/Web Scrapping/chromedriver-win64/chromedriver.exe')

options = Options()
# options.add_argument('--headless') 

options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")

class Extract:
    def __init__(self, url: str='https://www.rightmove.co.uk/house-prices.html'):
        '''
        Create an Extract class to extract data from the given URL.
        '''
               
        # Set the path to your chromedriver
        chromedriver_path = 'C:/Users/HP/Documents/DATA ENGINEERING BOOTCAMP/Web Scrapping/chromedriver-win64/chromedriver.exe'  # Ensure you have the correct path to your chromedriver
        options.add_argument("--window-size=1920x1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
        # Correct initialization of the service and driver
        service = Service(chromedriver_path)  # Service points to the chromedriver
        self.driver = webdriver.Chrome(service=service, options=options)  # Assign self.driver correctly
        
        self.driver.get(url)  # Open the URL
          
    #Define the accept cookies method
    def accept_cookies(self, xpath):
         '''
         We will Define a method that finds and clicks on accept cookies button. 
         If the cookies button is not found:
         Return:
            'No Cookies Found'

         We will also add a timer which will allow 5 seconds for the website to load the webpage, look for the accept cookies button and  click on it.
         '''
         time.sleep(2) #Wait for 2 seconds
         try:
             self.driver.find_element(By.XPATH, xpath).click()
         except TimeoutException:
             print('No Cookies Found')
             pass
         
        #  return accept_cookies
         
    #We will define the method that locate the search input fields
    def search_input(self, xpath: str='//*[@id="housePrices_soldPrices__bB7YV"]/div/div/div/div/div/input'):
        '''
        Locates and inputs text into the search input field.
        '''
        # Initialize WebDriverWait with self.driver
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds for elements to load
        try:
            # Locate the search input field
            input_glasgow = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            # Input the search term into the text box
            input_glasgow.send_keys("Glasgow City Centre")
        except TimeoutException:
            print("Search input box not found or took too long to load.")        

    #We will define the method that will cick on the search button
    def search_button(self, xpath: str= '//*[@id="housePrices_soldPrices__bB7YV"]/div/div/div/div/button'):
         '''
         We will define a method that click on the see search button,
         and to enable us input the our search location.
         
         If this button is not found:
        
         Return:
            'Not Found'
         '''
         try:
             self.driver.find_element(By.XPATH, xpath).click()
         except TimeoutException:
             print('Search xPath Not Found')
             pass
         
    def glasgow_city_search_result(self, xpath: str = '//*[@id="regions93616"]/a'):
        '''
        This method clicks the Glasgow City Centre search option from the result page.
        '''
        try:
            # Wait for the element to be visible and then click it
            wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
            glasgow_result = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))  # Wait until it's clickable
            glasgow_result.click()  # Perform the click action
        except TimeoutException:
            print('Search result took too long to load.')
        except NoSuchElementException:
            print('Search result element not found.')    
                    
    def click_glasgow_result(self, xpath: str= '//*[@id="regions93616"]/a'):
         '''
         We will define a method that click on the Sold price search button,
         and to display the result.
         
         If this button is not found:
        
         Return:
            'Not Found'
         '''
         try:
             self.driver.find_element(By.XPATH, xpath).click()
         except TimeoutException:
             print('Search xPath Not Found')
             pass
    def filter_result(self, xpath: str = '//*[@id="content"]/div[2]/div[2]/div[4]/div[1]/div[3]/div[1]/div[2]/select'): 
         ''' 
         This method wil filter the  result to a 10 mile distance
         '''
         try:
             dropdown = self.driver.find_element(By.XPATH, xpath)
             select =Select(dropdown)
             select.select_by_visible_text("Within 10 miles")
         except TimeoutException:
             print('Select Not found')
         
    # XPath for the container holding the property listings
    def find_container(self, xpath: str='/html/body/div[2]/div[2]/div[2]/div[4]'):
        #time.sleep(2)
        #return self.driver.find_element(By.XPATH, xpath)
        return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
                )
    
    # Empty list to store scraped data
    def Extract_link(self, container_xpath):
        property_data = []
        # Loop for pagination (adjust the range as needed)
        
        for i in range(40):  # Change to the actual number of pages you want to scrape
            try:
                # Wait for the container to load
                container = container_xpath
                # Find all property listings within the container by class name
                property_listings_2 = container.find_elements(By.CLASS_NAME, 'propertyCard')
                # Iterate through each listing and scrape data
                for listing in property_listings_2:
                    try:
                        title = listing.find_element(By.XPATH, './div/a').text
                        Date_1 = listing.find_element(By.XPATH, './div/div[2]/table/tbody/tr[1]/td[2]').text
                        Price_1 = listing.find_element(By.XPATH, './div/div[2]/table/tbody/tr[1]/td[1]').text
                        image = listing.find_element(By.XPATH, './a/img').get_attribute('src')
                        no_bed_rooms = listing.find_element(By.XPATH, './div/div[1]').text
                        Address = listing.find_element(By.XPATH, './div/a').text
                        # Append the scraped data to the list
                        property_data.append([title, Address, Date_1, Price_1, no_bed_rooms, image])

                    except Exception as e:
                        print(f"Error scraping listing: {e}")
                    # Pause briefly before looking for the "Next" button
            
               
                    next_button_xpath = '/html/body/div[2]/div[2]/div[2]/div[4]/div[28]/div[3]/div'  # Adjust as needed
                    # time.sleep(5)
                    # next_button = self.driver.find_element(By.XPATH, next_button_xpath)
                    next_button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                    )
                    next_button.click()
                    print(f'Next Button clicked for page {i + 1}')
            except Exception as e:
                print(f"No more pages or failed to find the Next button on page {i + 1}. Error: {e}")
                break
            
        return property_data
        
        
class Transform:
    def data_transform(self, df_pd):
        import pandas as pd
        import uuid
        from datetime import datetime
        #creating the pandas Dataframe from the property_data list
        Property_dataframe = pd.DataFrame(df_pd, columns=['title', 'Address', 'Date_1', 'Price_1', 'no_bed_rooms', 'image'])
        Property_dataframe['id'] = str(uuid.uuid4())
        return Property_dataframe
    
    def download_timeframe(self, property_dataframe):
        from datetime import datetime
        #add download data and download timestamp to this dataframe
        current_datetime = datetime.now()
        property_dataframe['Download_Date'] = current_datetime.date()  # Only Date
        property_dataframe['Download_Timestamp'] = current_datetime  # Full Timestamp (date + time)
        return property_dataframe
        
        
    def data_normalisation(self, property_dataframe):    
        #add the property Id to this dataframe
        property_dataframe = property_dataframe.reindex(columns=['id'] + [col for col in property_dataframe.columns if col != 'id'])
        #clean the data removing the unknown from the number of rooms
        property_dataframe['no_bed_rooms'] = property_dataframe['no_bed_rooms'].str.split(',').str[0].str.strip()

        #Get the unique values of the 'no_bed_rooms' column
        unique_bedrooms = property_dataframe['no_bed_rooms'].unique()

        #Generate a UUID for each unique number of bedrooms
        bedroom_uuid_map = {}
        for bedroom in unique_bedrooms:
            bedroom_uuid_map[bedroom] = str(uuid.uuid4())  # Assign a UUID to each unique bedroom count

        #Map the 'no_bed_rooms' column to the UUIDs generated
        property_dataframe['bedroom_uuid'] = property_dataframe['no_bed_rooms'].map(bedroom_uuid_map)
        
            #creating a dataframe for the bedrooms with bedroom id
        no_bedrooms_dataframe = property_dataframe[['bedroom_uuid', 'no_bed_rooms','Download_Date','Download_Timestamp']]
        #creating a dataframe for property_dataframe without no-bed_rooms
        f_property_dataframe = property_dataframe.drop(columns=['no_bed_rooms'])
        #converting pandas datafrmae to csv
        # f_property_dataframe.to_csv('properties.csv', index=False) #converting property dataframe to csv
        # no_bedrooms_dataframe.to_csv('no_bed_rooms.csv', index=False) #converty bedroom dataframe to csv
        bedrooms_dataframe = no_bedrooms_dataframe.drop_duplicates()
        return f_property_dataframe, bedrooms_dataframe
      
        
class Load:
    def  Load_Data(Self, dataframe1, dataframe2):
        import boto3
        import pandas as pd
        from io import StringIO
        # Convert DataFrame to CSV in memory
        csv_buffer1 = StringIO()
        dataframe1.to_csv(csv_buffer1, index=False)

        csv_buffer2 = StringIO()
        dataframe2.to_csv(csv_buffer2, index=False)

        # Initialize a session using boto3
        s3 = boto3.client('s3',
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name='eu-west-1'  # e.g., 'us-east-1'
        )
        # Define the S3 bucket name and object key (file path)
        bucket_name = 'propertydataframe'
        s3_file_key = 'f_property_dataframe.csv'
        s3_file_key2 = 'bedrooms_dataframe.csv'

        # Upload the CSV to S3
        s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=csv_buffer1.getvalue())
        print("property_dataframe.CSV uploaded successfully to S3!")
        s3.put_object(Bucket=bucket_name, Key=s3_file_key2, Body=csv_buffer2.getvalue())
        print("Bedrooms_dataframe.CSV uploaded successfully to S3!")

# This is Precious making a change
        
accept_cookiesxpath = '//*[@id="onetrust-accept-btn-handler"]'
bot = Extract()
bot.accept_cookies(accept_cookiesxpath)
bot.search_input()
bot.search_button()
bot.click_glasgow_result()
bot.filter_result()

container_xpath = bot.find_container()
df_pd = bot.Extract_link(container_xpath)

df = Transform().data_transform(df_pd)
_df = Transform().download_timeframe(df)
print(_df)
f_property_dataframe, bedrooms_dataframe =Transform().data_normalisation(_df)

Load().Load_Data(f_property_dataframe,bedrooms_dataframe)