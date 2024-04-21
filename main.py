from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import re

firefox_options = webdriver.FirefoxOptions()

service = Service(
    GeckoDriverManager().install()
)

driver = webdriver.Firefox(
    service=service, options=firefox_options
)

try:
    keyword = "arthritis specialist"

    driver.get(f"https://www.google.com/maps/search/{keyword}")

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
    except Exception:
        pass

    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    driver.execute_script("""
    var scrollableDiv = arguments[0];
    function scrollAndClickWithinElement(scrollableDiv) {
        return new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 1000;
            var scrollDelay = 3000;

            var timer = setInterval(() => {
                var scrollHeightBefore = scrollableDiv.scrollHeight;
                scrollableDiv.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight > scrollHeightBefore) {
                    totalHeight = 0;
                    setTimeout(() => {
                        var scrollHeightAfter = scrollableDiv.scrollHeight;
                        if (scrollHeightAfter > scrollHeightBefore) {
                            return;
                        } else {
                            clearInterval(timer);
                            // Get all divs with the attribute 'div[role="feed"] > div > div[jsaction]'
                            var divsToClick = document.querySelectorAll('div[role="feed"] > div > div[jsaction] > a');
                            console.log('Number of divs found:', divsToClick.length);
                            // Click all divs with the attribute 'div[role="feed"] > div > div[jsaction]' one by one
                            clickDivsOneByOne(divsToClick, 0);
                        }
                    }, scrollDelay);
                }
            }, 200);
        });
    }

    function clickDivsOneByOne(divs, index) {
        if (index < divs.length) {
            divs[index].click();
            setTimeout(() => {
                clickDivsOneByOne(divs, index + 1);
            }, 500); // Delay between clicks (adjust as needed)
        } else {
            resolve(); // Resolve the promise after clicking all divs
        }
    }

    return scrollAndClickWithinElement(scrollableDiv);
""", scrollable_div)




    items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')
    cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] > a')
    
    print(cards.count())
    
    for card in cards:
        card.click()

    results = []

    for item in items:
        data = {}
        
        try:
            data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
        except Exception:
            pass
        
        try:
            data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        except Exception:
            pass
        
        try:
            data['website'] = item.find_element(By.CSS_SELECTOR, 'a[data-value="Website"]').get_attribute('href')
        except Exception:
            pass
        
        try:
            review_text_element = item.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span[role="img"]')
            review_text = review_text_element.get_attribute('aria-label')
            review_numbers = [float(piece.replace(",", ".")) for piece in review_text.split(" ") if piece.replace(",", ".").replace(".", "", 1).isdigit()]
            
            if review_numbers:
                data['stars'] = review_numbers[0]
                data['review_count'] = int(review_numbers[1]) if len(review_numbers) > 1 else 0
                data['review_text'] = review_text_element.text  # Add review text
        except Exception:
            pass
        
        try:
            text_content = item.text
            phone_pattern = r'((\+?\d{1,2}[ -]?)?(\(?\d{3}\)?[ -]?\d{3,4}[ -]?\d{4}|\(?\d{2,3}\)?[ -]?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}))'
            matches =  re.findall(phone_pattern, text_content)
            
            phone_numbers = [match[0] for match in matches]
            unique_phone_numbers = list(set(phone_numbers))
            
            data['phone'] = unique_phone_numbers[0] if unique_phone_numbers else None
            
        except Exception:
            pass
        
        if data.get('title') and data.get('stars') and data.get('review_count'):
            results.append(data)
            
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
            
finally:
    time.sleep(50)
    driver.close()


print("End test")