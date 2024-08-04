import requests
import zipfile
import os
from datetime import datetime, timedelta
from urllib import error

# Specify the start date and end date for the range
start_date = datetime(2024, 5, 25)
end_date = datetime.today() #yyyymmdd

# Loop through the range of dates and download the corresponding CSV files
current_date = start_date
while current_date <= end_date:
    # Format the URL with the current date
    #       https://archives.nseindia.com/content/historical/DERIVATIVES/2023/JUN/fo21JUN2023bhav.csv.zip
    url = f"https://archives.nseindia.com/content/historical/DERIVATIVES/{current_date.strftime('%Y')}/{current_date.strftime('%b').upper()}/fo{current_date.strftime('%d%b%Y').upper()}bhav.csv.zip"
    #url = f"https://https://www.google.com/fo{current_date.strftime('%d%b%Y').upper()}bhav.csv.zip"
    print(current_date)
    try:
        # Download the zip file
        response = requests.get(url, timeout=1)
        response.status_code
        response.raise_for_status()

        with open(f"cm{current_date.strftime('%d%b%Y').upper()}bhav.csv.zip", "wb") as f:
            f.write(response.content)

        # Extract the CSV file from the zip file
        with zipfile.ZipFile(f"cm{current_date.strftime('%d%b%Y').upper()}bhav.csv.zip", "r") as zip_ref:
            zip_ref.extractall("D:/nse_download/fo_download/")

        # Rename the CSV file
        #old_file_name = f"cm{current_d2ate.strftime('%d%b%Y').upper()}bhav.csv"
        #new_file_name = "equity_data.csv"
        #os.rename(old_file_name, new_file_name)

        # Move the renamed file to the download folder
        #os.replace(new_file_name, f"C:/nse_download/{new_file_name}")

        # Delete the zip file
        os.remove(f"cm{current_date.strftime('%d%b%Y').upper()}bhav.csv.zip")

        print(f"Downloaded file for {current_date.strftime('%d-%b-%Y')}")
    
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