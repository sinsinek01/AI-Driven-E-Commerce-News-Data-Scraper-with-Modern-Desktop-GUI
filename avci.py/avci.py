import customtkinter as ctk
import threading
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# UI Theme Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ProScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pro-Market Scraper v1.1")
        self.geometry("500x520")

        # Main Title
        self.label = ctk.CTkLabel(self, text="AI Data Miner Pro", font=("Roboto", 26, "bold"))
        self.label.pack(pady=25)

        # Status Indicator
        self.status_label = ctk.CTkLabel(self, text="Status: Ready to Scan", text_color="cyan")
        self.status_label.pack(pady=5)

        # --- ACTION BUTTONS ---
        self.button = ctk.CTkButton(self, text="START DATA EXTRACTION", 
                                     command=self.start_scraping, 
                                     fg_color="#1f538d", hover_color="#14375e", height=40, font=("Roboto", 14, "bold"))
        self.button.pack(pady=15)

        self.open_button = ctk.CTkButton(self, text="OPEN EXCEL REPORT", 
                                          command=self.open_file, 
                                          fg_color="#28a745", hover_color="#218838", height=40, state="disabled", font=("Roboto", 14, "bold"))
        self.open_button.pack(pady=10)

        # Console Log Box
        self.textbox = ctk.CTkTextbox(self, width=800, height=180, corner_radius=10)
        self.textbox.pack(pady=20)

        self.filename = "scraped_data_report.csv"

    def log(self, message):
        self.textbox.insert("end", f">>> {message}\n")
        self.textbox.see("end")

    def open_file(self):
        """Opens the generated file with the system's default app (Excel)."""
        if os.path.exists(self.filename):
            os.startfile(self.filename)
            self.log("Opening report in Excel...")
        else:
            self.log("Error: Report file not found!")

    def start_scraping(self):
        self.button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.status_label.configure(text="Status: Bot is Running...", text_color="yellow")
        self.log("Initializing WebDriver...")
        threading.Thread(target=self.run_bot).start()

    def run_bot(self):
        try:
            options = Options()
            options.add_argument("--headless")
            # Pro tip: Added a common user-agent to avoid detection
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            self.log("Connecting to target source...")
            driver.get("http://books.toscrape.com/index.html")
            time.sleep(2)

            items = driver.find_elements(By.CLASS_NAME, "product_pod")
            self.log(f"Success! Found {len(items)} items.")

            data = []
            for item in items:
                title = item.find_element(By.TAG_NAME, "h3").text
                price = item.find_element(By.CLASS_NAME, "price_color").text
                data.append({"Product Name": title, "Price": price})

            df = pd.DataFrame(data)
            df.to_csv(self.filename, index=False, encoding="utf-16")
            
            self.log("Data saved successfully.")
            self.status_label.configure(text="Status: Task Completed!", text_color="#28a745")
            self.open_button.configure(state="normal")
            driver.quit()

        except Exception as e:
            self.log(f"Critical Error: {str(e)}")
            self.status_label.configure(text="Status: Error Occurred", text_color="red")
        
        self.button.configure(state="normal")

if __name__ == "__main__":
    app = ProScraperApp()
    app.mainloop()