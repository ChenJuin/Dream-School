from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import sys
import time

#将货币代码转换为中文
currency_mapping = {
    "GBP":"英镑",
    "HKD":"港币",
    "USD":"美元",
    "CHF":"瑞士法郎",
    "DEM":"德国马克",
    "FRF":"法国法郎",
    "SGD":"新加坡元",
    "SEK":"瑞典克朗",
    "DKK":"丹麦克朗",
    "NOK":"挪威克朗",
    "JPY":"日元",
    "CAD":"加拿大元",
    "AUD":"澳大利亚元",
    "EUR":"欧元",
    "MOP":"澳门元",
    "PHP":"菲律宾比索",
    "THP":"泰国铢",
    "NZD":"新西兰元",
    "KRW":"韩国元",
    "RUB":"卢布",
    "MYR":"林吉特",
    "TWD":"新台币",
    "ESP":"西班牙比塞塔",
    "ITL":"意大利里拉",
    "NLG":"荷兰盾",
    "BEF":"比利时法郎",
    "FIM":"芬兰马克",
    "INR":"印度卢比",
    "IDR":"印尼卢比",
    "BRC":"巴西里亚尔",
    "AED":"阿联酋迪拉姆",
    "ZAR":"南非兰特",
    "SAR":"沙特里亚尔",
    "TRL":"土耳其里拉",
}

def format_date(date_str):
    
    #将输入的日期字符串转换为 datetime 对象
    input_date = datetime.strptime(date_str, "%Y%m%d")
    
    #获取今天的日期
    today = datetime.today()
    
    #检测输入的日期是否超过今天的日期
    if input_date > today:
        print(f"Error: The date {date_str} is beyond today's date.")
        return None
    
    #将datetime对象转换回字符串
    return input_date.strftime("%Y-%m-%d")

def get_exchange_rate(date, currency_code):
    
    currency_name = currency_mapping.get(currency_code.upper())
    if not currency_name:
        print(f"Currency code {currency_code} is not supported.")
        return

    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service)

    #访问中国银行外汇牌价页面
    url = 'https://www.boc.cn/sourcedb/whpj/'
    driver.get(url)

    #格式化日期
    formatted_date = format_date(date)
    if formatted_date is None:
        return
    

    #填写开始日期和结束日期
    date_start = driver.find_element(By.NAME, "erectDate")
    date_start.clear()
    date_start.send_keys(formatted_date)
    date_end = driver.find_element(By.NAME, "nothing")  
    date_end.clear()
    date_end.send_keys(formatted_date)

    #等待货币下拉列表可见
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "pjname")))

    #选择货币
    currency_select = Select(driver.find_element(By.ID, "pjname"))
    currency_select.select_by_visible_text(currency_name)

    #点击搜索按钮
    search_button = driver.find_element(By.XPATH, "//input[@class='search_btn' and @style='float:right;margin-righth:26px;']")
    search_button.send_keys(Keys.ENTER)

    #等待页面加载
    time.sleep(3)

    #获取现汇卖出价
    currency_rows = driver.find_elements(By.XPATH, f"//tr[td[contains(text(), '{currency_name}')]]")
    if currency_rows:
        sell_price = currency_rows[0].find_element(By.XPATH, ".//td[4]").text
        result = f"{currency_name} {currency_code} {formatted_date} {sell_price}"
        with open("result.txt", "w") as file:
            file.write(result)
    else:
        print("No data found for the specified currency and date.")

    driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]
    get_exchange_rate(date, currency_code)