import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
from datetime import datetime

def startChrome():
    # PowerShell script yolunu belirtin
    ps1_path = r".\StartChromeDebug.ps1"

    # PowerShell komutunu çalıştırın
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1_path])

def stopChrome():
    # Chrome'u kapat
    subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], shell=True)

def main():
    # Halihazırda debug modunda çalışan Chrome'a bağlanabilmek için debugger_address ayarı
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"  # Chrome'un debug portunu yazın

    # Mevcut Chrome oturumuna bağlan
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Yeni sekme aç
        driver.execute_script("window.open();")

        # Yeni sekmeye geç
        driver.switch_to.window(driver.window_handles[-1])

        # cimri.com'a git
        driver.get("https://www.cimri.com/indirimli-urunler?sort=new%2Cdesc")

        # Sayfanın yüklenmesi için zaman tanı
        time.sleep(5)

        # Tüm <article> elemanlarını bul
        wait = WebDriverWait(driver, 10)  # Maksimum 10 saniye bekle
        
        # "LoadingOrLink_link" ile başlayan class'a sahip <a> tag'ına tıklamak
        try:
            # Elemanın tıklanabilir olmasını bekle
            next_page_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class^='LoadingOrLink_link']"))
            )
            next_page_button.click()
        except:
            print("Normal click ile tiklanamadi, JS ile deneniyor...")
            # JavaScript kullanarak tıklama işlemi
            driver.execute_script("document.querySelector('a[class^=\"LoadingOrLink_link\"]').click();")

        # Yeni verilerin yüklenmesi için zaman tanı
        time.sleep(5)
        
        # Sayfanın %30 kadar altına kaydırma işlemi
        for i in range(50):  # 50 kez kaydırma işlemi yap
            # driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.30);")
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(3)  # 2 saniye bekle    
            print(f"{i+1}. kere scroll işlemi yapıldı. Sayfanın guncel URL'si: {driver.current_url}")


        # Dosya adını datetime ile oluştur
        filename = datetime.now().strftime("%Y%m%d%H%M") + ".txt"            
        
        articles = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

        # Dosyayı aç (yazma modu)
        with open(filename, 'w', encoding='utf-8') as file:
            # Her bir <article> içinde başlık ve fiyatı çek
            for article in articles:
                
                # <h3> başlığını bul
                try:
                    title = article.find_element(By.TAG_NAME, "h3").text
                except:
                    title = "Baslık bulunamadı"

                # Fiyat satırını bul
                try:
                    price_element = article.find_element(By.CSS_SELECTOR, "span[class^='Price_price__']")
                    price = price_element.text
                except:
                    price = "Fiyat bulunamadı"

                # Link satırını bul
                try:
                    link_element = article.find_element(By.CSS_SELECTOR, "a[class*='_linkArea_']")
                    href = link_element.get_attribute("href")
                except:
                    href = "Link bulunamadı" 

                # Sonuçları yazdır
                if title:
                    print(f"Link: {href}")
                    print(f"Title: {title}")
                    print(f"Price: {price}")
                    print("-" * 100)
                    
                    # Dosyaya yazdırma
                    file.write(f"Link: {href}\n")
                    file.write(f"Title: {title}\n")
                    file.write(f"Price: {price}\n")
                    file.write("-" * 100 + "\n")
            
    finally:
        driver.quit()
        stopChrome()

if __name__ == "__main__": 
    startChrome()
    main() 