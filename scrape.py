from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def login_and_get_data(username, password):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        
        print("Opening login page...")
        driver.get("https://kmctce.etlab.app/user/login")
        
        # Wait for the page to load
        time.sleep(2)
        
        # Get login credentials
        # Find username and password fields
        username_field = driver.find_element(By.ID, "LoginForm_username")  # Adjust selector if needed
        password_field = driver.find_element(By.ID, "LoginForm_password")  # Adjust selector if needed
        
        # Enter credentials
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  # Adjust selector if needed
        login_button.click()
        
        # Wait for login to complete
        time.sleep(5)
        
        # Check if login was successful
        if "login" not in driver.current_url:
            print("Login successful!")
            
            # Navigate to attendance page
            print("Navigating to attendance page...")
            driver.get("https://kmctce.etlab.app/ktuacademics/student/viewattendancesubject/37")
            
            # Wait for the page to load
            time.sleep(3)
            
            # Get attendance data
            print("Extracting attendance data...")
            attendance_tables = driver.find_elements(By.TAG_NAME, "table")
            
            if attendance_tables:
                # Get the first table
                attendance_table = attendance_tables[0]
                
                # Extract table data
                header_cells = attendance_table.find_elements(By.TAG_NAME, "th")
                headers = [cell.text for cell in header_cells]
                
                rows = attendance_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
                attendance_data = []
                
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = [cell.text for cell in cells]
                    if row_data:
                        attendance_data.append(row_data)
                
                # Create and save DataFrame
                if headers and attendance_data:
                    df = pd.DataFrame(attendance_data, columns=headers)
                    df.to_csv('attendance_data.csv', index=False)
                    print("Attendance data saved to 'attendance_data.csv'")
                    print(df.head())
                else:
                    print("Could not extract attendance data properly.")
            else:
                print("No attendance tables found on the page.")
            
            # Now try to find assignments
            print("\nAttempting to find and extract assignments...")
            try:
                # Look for a link to assignments page
                driver.get("https://kmctce.etlab.app/student/assignments")

                time.sleep(3)
                print("Extracting assignment data...")

                assignment_table = driver.find_elements(By.TAG_NAME, "table")
                
                if assignment_table:
                    # Get the first table
                    assignment_table = assignment_table[0]
                
                    # Extract table data
                    header_cells = assignment_table.find_elements(By.TAG_NAME, "th")
                    headers = [cell.text for cell in header_cells]
                    
                    rows = assignment_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
                    assignment_data = []
                    
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        row_data = [cell.text for cell in cells]
                        if row_data:
                            assignment_data.append(row_data)
                    
                    # Create and save DataFrame
                    if headers and assignment_data:
                        df = pd.DataFrame(assignment_data, columns=headers)
                        df.to_csv('assignment_data.csv', index=False)
                        print("Assignments data saved to 'assignment_data.csv'")
                        print(df.head())
                    else:
                        print("Could not extract assignment data properly.")
                else:
                    print("No assignment tables found on the page.")
                    
            except Exception as e:
                print(f"Error while trying to find assignment: {str(e)}")
                
            # Try to find internal marks
            print("\nAttempting to find and extract internal marks...")
            try:
                # Look for a link to internal marks page
                driver.get("https://kmctce.etlab.app/student/results")
                internal_table = driver.find_elements(By.ID, "yw0")
                
                if internal_table:
                    # Get the first table
                    internal_table = internal_table[0]
                
                    # Extract table data
                    header_cells = internal_table.find_elements(By.TAG_NAME, "th")
                    headers = [cell.text for cell in header_cells]
                    
                    rows = internal_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
                    internal_data = []
                    
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        row_data = [cell.text for cell in cells]
                        if row_data:
                            internal_data.append(row_data)
                    
                    # Create and save DataFrame
                    if headers and internal_data:
                        df = pd.DataFrame(internal_data, columns=headers)
                        df.to_csv('internal_data.csv', index=False)
                        print("Internal marks data saved to 'internal_data.csv'")
                        print(df.head())
                    else:
                        print("Could not extract internal data properly.")
                else:
                    print("No internal tables found on the page.")
                    
            except Exception as e:
                print(f"Error while trying to find internals: {str(e)}")
            
            # Take screenshots for debugging
            #driver.save_screenshot("dashboard_screenshot.png")
            #print("Saved screenshot of the dashboard.")
            
            return True
        else:
            print("Login failed. Please check your credentials.")
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        # Close the browser
        driver.quit()

