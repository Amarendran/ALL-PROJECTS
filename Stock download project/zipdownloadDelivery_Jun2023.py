import requests
import zipfile
import os
from datetime import datetime, timedelta
from urllib import error
import pandas as pd

# Specify the start date and end date for the range
start_date = datetime(2023, 7, 16) #yyyymmdd
end_date = datetime.today()

# Loop through the range of dates and download the corresponding CSV files
current_date = start_date
while current_date <= end_date:
    # Format the URL with the current date
    url = f"https://archives.nseindia.com/archives/equities/mto/MTO_{current_date.strftime('%d%m%Y')}.DAT"
    print(current_date)

    # Create the directory if it doesn't exist
    output_dir = "C:/nse_download/download_withdelivery/"
    output_dir_Temp = "C:/nse_download/"
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output file path based on the current date
    output_file_Temp = os.path.join(output_dir_Temp, f"tempfile.dat")
    output_file = os.path.join(output_dir, f"DQ{current_date.strftime('%Y%m%d')}.csv")


    try:
        # Download the file
        response = requests.get(url, timeout=1)
        response.status_code
        response.raise_for_status()
        content = response.content
        
        #To Save Temp DAT File as temp dat file
        with open(output_file_Temp, "wb") as file:
            file.write(content)
        
        print(f"File downloaded and saved as {output_file}")
        df = pd.read_table('C:/nse_download/'+'tempfile.DAT',delimiter=',',index_col=1,skiprows=4,skipfooter=0,names=['Record Type', 'Sr No', 'Name of Security','SERIES','Quantity Traded','Deliverable Quantity','% of Deliverable Quantity'])
        #df = pd.read_table('C:/nse_download/'+'tempfile.DAT',delimiter=',',index_col=0,skiprows=3,skipfooter=0)
        df['Date']=current_date
        df=df[df.SERIES=='EQ']
        df.to_csv(output_file)
        
        #To delete the temp Dat File
        os.remove(output_file_Temp)

        #print(f"Downloaded file for {current_date.strftime('%d-%b-%Y')}")
    
    except requests.ConnectionError as e:
        print(e)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {e.response.status_code} occurred while downloading file for {current_date.strftime('%d-%b-%Y')}")
    except requests.exceptions.InvalidURL as e:
        print(f"Invalid URL: {url}")
    except requests.exceptions.RequestException as e:
        print(e)
    except (zipfile.BadZipFile, OSError) as e:
        print(f"Error occurred while extracting file for {current_date.strftime('%d-%b-%Y')}: {e}")
    except Exception as e:
        print(f"Unknown error occurred for {current_date.strftime('%d-%b-%Y')}: {e}")

    # Increment the current date by one day
    current_date += timedelta(days=1)
    
    while current_date.weekday() >= 5:
        current_date += timedelta(days=1)