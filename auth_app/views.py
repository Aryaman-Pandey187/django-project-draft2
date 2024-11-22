from django.shortcuts import render, redirect
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

import logging
logging.basicConfig(level=logging.INFO)

def login_view(request):
    if request.method == 'POST':
        # Retrieve the form data
        intranetID = request.POST.get('intranetID')
        password = request.POST.get('password')

        # Check if both fields are filled
        if intranetID and password:
            # Store the values in the session
            request.session['intranetID'] = intranetID
            request.session['password'] = password

            # Redirect to the source info page
            return redirect('source_info_page')
            
        else:
            # Return the form with an error if fields are missing
            return render(request, 'auth_app/login.html', {'error': 'Please fill in both fields'})

    # # Render the login page for GET requests
    # return render(request, 'auth_app/login.html')

        # print(intranetID, password, source_database, source_table)

        # logging.debug(intranetID, password, source_database, source_table)

        # if source_database and source_table:
        #     return redirect('target_env_details')
        # return render(request, 'auth_app/login.html', {'error': 'Please fill in all fields'})
        # Selenium logic to verify credentials
        # success = authenticate_with_selenium(intranetID, password)

        # if success:
        #     return JsonResponse({'status': 'success', 'message': 'Authentication Successful!'})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Authentication Failed!'})

    return render(request, 'auth_app/login.html')


def authenticate_with_selenium(intranetID, password):
    # Configure Selenium
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for production
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Replace with the target website URL
        target_url = 'https://example.com/login'
        driver.get(target_url)

        # Locate input fields and enter credentials (adjust locators as needed)
        driver.find_element(By.ID, 'username').send_keys(intranetID)
        driver.find_element(By.ID, 'password').send_keys(password, Keys.RETURN)

        time.sleep(2)  # Wait for the page to load

        # Check for a successful login (adjust logic based on the site)
        if "Welcome" in driver.page_source:
            return True
        return False
    except Exception as e:
        print(f"Error during Selenium authentication: {e}")
        return False
    finally:
        driver.quit()

# Render the source information page
def source_info_page(request):
    intranetID = request.session.get('intranetID')
    password = request.session.get('password')

    if request.method == 'POST':
        source_database = request.POST.get('source_database')
        source_table = request.POST.get('source_table')

        request.session['intranetID'] = intranetID
        request.session['password'] = password

        request.session['source_database'] = source_database
        request.session['source_table'] = source_table

        print(f"Intranet ID: {intranetID}, Password: {password}")
        print(f"Source Database: {source_database}, Source Table: {source_table}")

        # Check if credentials are available
        if source_table and source_database:
            return redirect('target_env_page')  # Redirect back to login if session data is missing

            # ,{
            #     'intranetID': intranetID,
            #     'password': password,
            #     'source_database': source_database,
            #     'source_table':source_table,
            # }

        # print(f"Intranet ID: {intranetID}, Password: {password}")
        # print(f"Source Database: {source_database}, Source Table: {source_table}")

    #     # Further processing
    #     # ...

    return render(request, 'auth_app/source_info.html')

def target_env_page(request):
    intranetID = request.session.get('intranetID')
    password = request.session.get('password')
    source_database = request.session.get('source_database')
    source_table = request.session.get('source_table')

    if request.method == 'POST':
        target_env_name = request.POST.get('target_env_name')

        request.session['target_env_name'] = target_env_name

        print(f"Intranet ID: {intranetID}, Password: {password}")
        print(f"Source Database: {source_database}, Source Table: {source_table}")
        print(f"radio-button-choice: {target_env_name}")

        context = {
            'target_env_name': target_env_name,   
        }

        if target_env_name:
            return redirect('target_env_login')
        
        # ,{
        #     'intranetID': intranetID,
        #     'password': password,
        #     'source_database': source_database,
        #     'source_table':source_table,
        #     'target_env_name':target_env_name,
        # }

    return render(request, 'auth_app/target_env_page.html')

def target_env_login(request):
    intranetID = request.session.get('intranetID')
    password = request.session.get('password')
    source_database = request.session.get('source_database')
    source_table = request.session.get('source_table')
    target_env_name = request.session.get('target_env_name')

    if request.method == 'POST':
        target_env_username = request.POST.get('target_env_username')
        target_env_password = request.POST.get('target_env_password')

        request.session['target_env_username'] = target_env_username
        request.session['target_env_password'] = target_env_password

        print(f"Intranet ID: {intranetID}, Password: {password}")
        print(f"Source Database: {source_database}, Source Table: {source_table}")
        print(f"radio-button-choice: {target_env_name}")
        print(f"Target Env Username: {target_env_username}, Target Env Password: {target_env_password}")

        # return redirect(target_info_page)
        return redirect('target_info_page')
    
    # , {
    #         'intranetID': intranetID,
    #         'password': password,
    #         'source_database': source_database,
    #         'source_table':source_table,
    #         'target_env_name':target_env_name,
    #         'target_env_username':target_env_username,
    #         'target_env_password':target_env_password,
    #     }

    return render(request, 'auth_app/target_env_login.html', {'message': target_env_name})

def target_info_page(request):
    intranetID = request.session.get('intranetID')
    password = request.session.get('password')
    source_database = request.session.get('source_database')
    source_table = request.session.get('source_table')
    target_env_name = request.session.get('target_env_name')
    target_env_username = request.session.get('target_env_username')
    target_env_password = request.session.get('target_env_password')

    if request.method == 'POST':
        target_database = request.POST.get('target_database')
        target_table = request.POST.get('target_table')

        request.session['target_database'] = target_database
        request.session['target_table'] = target_table

        print(f"Intranet ID: {intranetID}, Password: {password}")
        print(f"Source Database: {source_database}, Source Table: {source_table}")
        print(f"radio-button-choice: {target_env_name}")
        print(f"Target Env Username: {target_env_username}, Target Env Password: {target_env_password}")
        print(f"Target Database: {target_database}, Target Table: {target_table}")

        return redirect('details_verification_page_with_logging')

    return render(request, 'auth_app/target_info_page.html')

    # ,{
    #     'intranetID': intranetID,
    #     'password': password,
    #     'source_database': source_database,
    #     'source_table':source_table,
    #     'target_env_name':target_env_name,
    #     'target_env_username':target_env_username,
    #     'target_env_password':target_env_password,
    # }


def details_verification_page_with_logging(request):
    # if request.method == 'POST':
    #     pass

    context = {
        'message':"HEYYYYYYYYYYYY",
    }
    return render(request, 'auth_app/details_verification_page_with_logging.html', context)


# delete all DB data once all required data is inserted into the DB.
def clear_session_data(request):
    request.session.flush()  # Clears all session data
    return redirect('login')  # Redirect to the desired page


