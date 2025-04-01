import time 
from playwright.sync_api import sync_playwright
import pandas as pd

def login_and_get_data(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Opening login page...")
        page.goto("https://kmctce.etlab.app/user/login", timeout=60000)
        
        # Enter credentials and login
        page.fill("#LoginForm_username", username)
        page.fill("#LoginForm_password", password)
        page.click("button[type='submit']")
        
        # Wait for navigation after login
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        if "login" not in page.url:
            print("Login successful!")
            
            # Navigate to attendance page
            print("Navigating to attendance page...")
            page.goto("https://kmctce.etlab.app/ktuacademics/student/viewattendancesubject/37")
            time.sleep(2)
            
            # Extract attendance data
            print("Extracting attendance data...")
            tables = page.query_selector_all("table")
            if tables:
                attendance_table = tables[0]
                rows = attendance_table.query_selector_all("tr")
                
                headers = [th.inner_text() for th in rows[0].query_selector_all("th")]
                data = [[td.inner_text() for td in row.query_selector_all("td")] for row in rows[1:]]
                
                if headers and data:
                    df = pd.DataFrame(data, columns=headers)
                    df.to_csv("attendance_data.csv", index=False)
                    print("Attendance data saved to 'attendance_data.csv'")
                    print(df.head())
                else:
                    print("Could not extract attendance data properly.")
            else:
                print("No attendance tables found.")
            
            # Extract assignments
            print("\nAttempting to find and extract assignments...")
            page.goto("https://kmctce.etlab.app/student/assignments")
            time.sleep(2)
            
            tables = page.query_selector_all("table")
            if tables:
                assignment_table = tables[0]
                rows = assignment_table.query_selector_all("tr")
                
                headers = [th.inner_text() for th in rows[0].query_selector_all("th")]
                data = [[td.inner_text() for td in row.query_selector_all("td")] for row in rows[1:]]
                
                if headers and data:
                    df = pd.DataFrame(data, columns=headers)
                    df.to_csv("assignment_data.csv", index=False)
                    print("Assignments data saved to 'assignment_data.csv'")
                    print(df.head())
                else:
                    print("Could not extract assignment data properly.")
            else:
                print("No assignment tables found.")
            
            # Extract internal marks
            print("\nAttempting to find and extract internal marks...")
            page.goto("https://kmctce.etlab.app/student/results")
            time.sleep(2)
            
            tables = page.query_selector_all("#yw0")
            if tables:
                internal_table = tables[0]
                rows = internal_table.query_selector_all("tr")
                
                headers = [th.inner_text() for th in rows[0].query_selector_all("th")]
                data = [[td.inner_text() for td in row.query_selector_all("td")] for row in rows[1:]]
                
                if headers and data:
                    df = pd.DataFrame(data, columns=headers)
                    df.to_csv("internal_data.csv", index=False)
                    print("Internal marks data saved to 'internal_data.csv'")
                    print(df.head())
                else:
                    print("Could not extract internal data properly.")
            else:
                print("No internal tables found.")
        
        else:
            print("Login failed. Please check your credentials.")
            return False
        
        browser.close()
        return True
