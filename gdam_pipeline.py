from plyer import notification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from statistics import fmean
import logging
import config

logging.basicConfig(
    filename = config.LOG_DIR/"gdam.txt",
    level = logging.INFO,
    format = '%(asctime)s-%(levelname)s-%(message)s'
)

def to_float(x):
    try:
        return round(float(x),2)
    except:
        return None
        
try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    service = Service(config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service= service,options=chrome_options) 
    check_date = datetime.now().strftime("%d-%m-%Y")
    master_df = pd.DataFrame()
    
    driver.get("https://www.iexindia.com/market-data/green-day-ahead-market/market-snapshot")
    logging.info("website opened.")
    time.sleep(1)
    
    # Applying the filters
    try:
        logging.info("Locating INTERVAL dropdown...")  
        Interval_dropdown = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[4]/section/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div'))
        )
        time.sleep(1)
        Interval_dropdown.click()
        logging.info("INTERVAL dropdown found. Selecting 'HOURLY'...")
        option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//li[text()='Hourly']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", option)
        option.click() 
        logging.info("'Hourly' selected.")
    except NoSuchElementException as e:
        logging.exception(f"Error locating or interacting with INTERVAL dropdown: {e}")

    try:
        Delivery_period_dropdown = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[4]/section/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div')) )
        Delivery_period_dropdown.click()
        logging.info("DELIVERY PERIOD dropdown found. Selecting 'Today'...")
        option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[text()='Today']"))
        )
        logging.info("Today selected.")
        driver.execute_script("arguments[0].scrollIntoView(true);", option)
        option.click()
    except NoSuchElementException as e:
        logging.exception(f"Error locating or interacting with DELIVERY PERIOD dropdown: {e}")
    
    try:
        logging.info("Waiting for Update Report button...")
        time.sleep(1)  
        Update_Report_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/section/div[1]/div[1]/div[2]/button"))
        )
        logging.info("Clicking Update Report button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", Update_Report_button)
        time.sleep(1)
        try:
            Update_Report_button.click()
        except:
            driver.execute_script("arguments[0].click();", Update_Report_button)
        
        time.sleep(2)
        logging.info("Waiting for table to load...")
        expected_date = check_date
        xpath_to_check = "/html/body/div[1]/div[4]/section/div[1]/div[3]/div[1]/table/tbody/tr[1]/td[1]"
        try:
            WebDriverWait(driver, 30).until(
                lambda d: d.find_element(By.XPATH, xpath_to_check).text.strip() == expected_date
            )
            logging.info("Table loaded")

        except Exception as e:

            print(f'Error while waiting for table load:{e}')
        
        ##Data extraction from Table
        new_df = pd.DataFrame()
        table = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/section/div[1]/div[3]/div[1]")
        rows = table.find_elements(By.TAG_NAME, 'tr') 
        date = []
        hour = []
        pb = []
        total_sell = []
        solar_sell = []
        non_solar_sell = []
        hydro_sell = []
        total_mcv = []
        solar_mcv = []
        non_solar_mcv =[]
        hydro_mcv = []
        total_fsv = []
        solar_fsv = []
        non_solar_fsv = []
        hydro_fsv = []
        mcp=[]
        wmcp = []

        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME,"td")
            if len(cells)<16:
                continue
            if len(cells)==17:
                date.append(check_date)
                hour.append(to_float(cells[1].text.strip()))
                pb.append(to_float(cells[2].text.strip()))
                total_sell.append(to_float(cells[3].text.strip()))
                solar_sell.append(to_float(cells[4].text.strip()))
                non_solar_sell.append(to_float(cells[5].text.strip()))
                hydro_sell.append(to_float(cells[6].text.strip()))
                total_mcv.append(to_float(cells[7].text.strip()))
                solar_mcv.append(to_float(cells[8].text.strip()))
                non_solar_mcv.append(to_float(cells[9].text.strip()))
                hydro_mcv.append(to_float(cells[10].text.strip()))
                total_fsv.append(to_float(cells[11].text.strip()))
                solar_fsv.append(to_float(cells[12].text.strip()))
                non_solar_fsv.append(to_float(cells[13].text.strip()))
                hydro_fsv.append(to_float(cells[14].text.strip()))
                mcp.append(to_float(cells[15].text.strip()))
                wmcp.append(to_float(cells[16].text.strip()))
            if len(cells)==16:
                date.append(check_date)
                hour.append(to_float(cells[0].text.strip()))
                pb.append(to_float(cells[1].text.strip()))
                total_sell.append(to_float(cells[2].text.strip()))
                solar_sell.append(to_float(cells[3].text.strip()))
                non_solar_sell.append(to_float(cells[4].text.strip()))
                hydro_sell.append(to_float(cells[5].text.strip()))
                total_mcv.append(to_float(cells[6].text.strip()))
                solar_mcv.append(to_float(cells[7].text.strip()))
                non_solar_mcv.append(to_float(cells[8].text.strip()))
                hydro_mcv.append(to_float(cells[9].text.strip()))
                total_fsv.append(to_float(cells[10].text.strip()))
                solar_fsv.append(to_float(cells[11].text.strip()))
                non_solar_fsv.append(to_float(cells[12].text.strip()))
                hydro_fsv.append(to_float(cells[13].text.strip()))
                mcp.append(to_float(cells[14].text.strip()))
                wmcp.append(to_float(cells[15].text.strip()))
        
        new_df = pd.DataFrame({
                    'Date': date,
                    "Hour": hour,
                    "Purchase Bid (MWh)": pb,
                
                    # Sell Bid
                    "Sell Bid Total (MWh)": total_sell,
                    "Sell Bid Solar (MWh)": solar_sell,
                    "Sell Bid Non-Solar (MWh)": non_solar_sell,
                    "Sell Bid Hydro (MWh)": hydro_sell,
                
                    # MCV
                    "MCV Total (MWh)": total_mcv,
                    "MCV Solar (MWh)": solar_mcv,
                    "MCV Non-Solar (MWh)": non_solar_mcv,
                    "MCV Hydro (MWh)": hydro_mcv,
                
                    # Final Scheduled Volume
                    "FSV Total (MWh)": total_fsv,
                    "FSV Solar (MWh)": solar_fsv,
                    "FSV Non-Solar (MWh)": non_solar_fsv,
                    "FSV Hydro (MWh)": hydro_fsv,
                
                    # Prices
                    "MCP (Rs/MWh)": mcp,
                    "Weighted MCP (Rs/MWh)": wmcp
                })
               
        logging.info("Data extraction complete.")
        mean_row = pd.DataFrame({
                        'Date': ["Average"],
                        'Hour': [""],
                    
                        "Purchase Bid (MWh)": [round(new_df["Purchase Bid (MWh)"].mean(), 2)],
                    
                        "Sell Bid Total (MWh)": [round(new_df["Sell Bid Total (MWh)"].mean(), 2)],
                        "Sell Bid Solar (MWh)": [round(new_df["Sell Bid Solar (MWh)"].mean(), 2)],
                        "Sell Bid Non-Solar (MWh)": [round(new_df["Sell Bid Non-Solar (MWh)"].mean(), 2)],
                        "Sell Bid Hydro (MWh)": [round(new_df["Sell Bid Hydro (MWh)"].mean(), 2)],
                    
                        "MCV Total (MWh)": [round(new_df["MCV Total (MWh)"].mean(), 2)],
                        "MCV Solar (MWh)": [round(new_df["MCV Solar (MWh)"].mean(), 2)],
                        "MCV Non-Solar (MWh)": [round(new_df["MCV Non-Solar (MWh)"].mean(), 2)],
                        "MCV Hydro (MWh)": [round(new_df["MCV Hydro (MWh)"].mean(), 2)],
                    
                        "FSV Total (MWh)": [round(new_df["FSV Total (MWh)"].mean(), 2)],
                        "FSV Solar (MWh)": [round(new_df["FSV Solar (MWh)"].mean(), 2)],
                        "FSV Non-Solar (MWh)": [round(new_df["FSV Non-Solar (MWh)"].mean(), 2)],
                        "FSV Hydro (MWh)": [round(new_df["FSV Hydro (MWh)"].mean(), 2)],
                    
                        "MCP (Rs/MWh)": [round(new_df["MCP (Rs/MWh)"].mean(), 2)],
                        "Weighted MCP (Rs/MWh)" : [round(fmean(new_df["Weighted MCP (Rs/MWh)"],weights=new_df["FSV Total (MWh)"]),2)]
                    })

        sum_row = pd.DataFrame({
                    'Date': ["Sum"],
                    'Hour': [""],
                
                    "Purchase Bid (MWh)": [round(new_df["Purchase Bid (MWh)"].sum(), 2)],
                
                    "Sell Bid Total (MWh)": [round(new_df["Sell Bid Total (MWh)"].sum(), 2)],
                    "Sell Bid Solar (MWh)": [round(new_df["Sell Bid Solar (MWh)"].sum(), 2)],
                    "Sell Bid Non-Solar (MWh)": [round(new_df["Sell Bid Non-Solar (MWh)"].sum(), 2)],
                    "Sell Bid Hydro (MWh)": [round(new_df["Sell Bid Hydro (MWh)"].sum(), 2)],
                
                    "MCV Total (MWh)": [round(new_df["MCV Total (MWh)"].sum(), 2)],
                    "MCV Solar (MWh)": [round(new_df["MCV Solar (MWh)"].sum(), 2)],
                    "MCV Non-Solar (MWh)": [round(new_df["MCV Non-Solar (MWh)"].sum(), 2)],
                    "MCV Hydro (MWh)": [round(new_df["MCV Hydro (MWh)"].sum(), 2)],
                
                    "FSV Total (MWh)": [round(new_df["FSV Total (MWh)"].sum(), 2)],
                    "FSV Solar (MWh)": [round(new_df["FSV Solar (MWh)"].sum(), 2)],
                    "FSV Non-Solar (MWh)": [round(new_df["FSV Non-Solar (MWh)"].sum(), 2)],
                    "FSV Hydro (MWh)": [round(new_df["FSV Hydro (MWh)"].sum(), 2)],
                
                    "MCP (Rs/MWh)": [round(new_df["MCP (Rs/MWh)"].sum(), 2)],
                    "Weighted MCP (Rs/MWh)": [round(new_df["Weighted MCP (Rs/MWh)"].sum(), 2)]
                })


        new_df =  pd.concat([new_df,sum_row,mean_row],ignore_index = True)
        file_path = config.REPORT_DIR/f'{check_date}.csv'
        new_df.to_csv(file_path, index=False, encoding='utf-8')
        new_df_reset = new_df.reset_index(drop= True)
        master_df = pd.concat([master_df, new_df_reset], ignore_index=False)


        
    except Exception as e:
        logging.exception(f"Error during processing: {e}")
    master_df.to_html(config.REPORT_DIR/f"{check_date}.html",index = False)
    master_df.to_excel(config.REPORT_DIR/f"GDAM_summary.xlsx",index = False)
    logging.info("CSV saved.")


except Exception as e:
     logging.exception(f"Script failed with error: {e}")


finally:
    if 'driver' in locals():
        driver.quit()

#plotting bar+line graph
import matplotlib.pyplot as plt

df_plot = new_df[~new_df["Date"].isin(["Average", "Sum"])]

fig, ax1 = plt.subplots(figsize=(10,5))

ax1.bar(df_plot["Hour"], df_plot["FSV Total (MWh)"], 
        color='lightblue', label="Final Scheduled Volume")

ax1.set_xlabel("Hour")
ax1.set_ylabel("Volume (MWh)", color='blue')
ax2 = ax1.twinx()

# ax2.plot(df_plot["Hour"], df_plot["MCP (Rs/MWh)"],
#          color='red', marker='o', label="MCP")

ax2.plot(df_plot["Hour"], df_plot["Weighted MCP (Rs/MWh)"], 
         color='green', marker='o', label="Weighted MCP")

ax2.set_ylabel("Price (Rs/MWh)", color='red')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title("IEX GDAM: Price vs Volume (Hourly)")
plt.grid(True)
plt.savefig(config.PLOT_DIR/"gdam_plot.png")
plt.close()
logging.info('gdam plot saved')


##outlook mail trigger
import win32com.client as win32

html_file_path = config.REPORT_DIR/"GDAM_summary.html"
image_path = config.PLOT_DIR/"gdam_plot.png"

try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    mail.To = ";".join(config.EMAIL_RECIPIENTS)
    
    mail.Subject = f"Green Day Ahead Market Report:{check_date}"
    attachment = mail.Attachments.Add(image_path)

    attachment.PropertyAccessor.SetProperty(
        "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
        "MyImage"
    )
    
    mail.HTMLBody = f"""
    <html>
    <body>
    
    Dear Team,<br><br>
    
    Please find the <b>Green Day Ahead Market Summary</b> below:<br><br>
    
    {html_content}
    
    <br><br>
    
    <b>Price vs Volume Trend:</b><br><br>
    
    <img src="cid:MyImage" width="800"><br><br>
    
    Regards,<br>
    Vinay
    
    </body>
    </html>
    """
    
    mail.Send()
    logging.info("Mail sent")

except Exception as e:
    logging.exception(f"Exception during mail trigger{e}")

