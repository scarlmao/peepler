import requests
import json
import os
import time
import urllib.parse
import random
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pystyle import Colors, Colorate
from pyfiglet import figlet_format  # For ASCII art banner

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)
response_time = config.get("response_time", 1)

# List of congratulatory messages
CONGRATS_MESSAGES = [
    "AWESOME!",
    "NICE!",
    "L33T HAX",
    "FANTASTIC!",
    "BRILLIANT!",
    "SUCCESS!",
    "YOU'RE HACKING NOW!"
]

# List of APIs or data sources (for demonstration in Settings & Transparency)
API_SOURCES = [
    "Bing Search (https://www.bing.com)",
    "TruePeopleSearch (https://truepeoplesearch.net)",
    "Radaris India (https://radaris.in)",
    "BAC-LAC (https://www.bac-lac.gc.ca)",
    "NigeriaPhoneBook (https://nigeriaphonebook.com)"
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(text="peepler"):
    """Prints the ASCII banner for the provided text."""
    banner_text = figlet_format(text, font="slant")
    print(Colorate.Vertical(Colors.cyan_to_green, banner_text, 1))


def print_congrats_ascii():
    """Prints a random congratulatory message in ASCII."""
    message = random.choice(CONGRATS_MESSAGES)
    ascii_text = figlet_format(message, font="slant")
    print(Colorate.Vertical(Colors.cyan_to_green, ascii_text, 1))


def write_results(data, filepath="results/output.txt"):
    """Writes data to a JSON file."""
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def get_name_input():
    """Prompts for first and last name."""
    first_name = input(Colors.cyan + "First Name --> ")
    last_name = input(Colors.cyan + "Last Name --> ")
    return first_name.strip(), last_name.strip()


def bing_search(query):
    """Performs a Bing search and returns a list of URLs."""
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q={query_encoded}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during Bing search: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http') or href.startswith('www'):
            search_results.append(href)
    return search_results


def process_and_print_results(results):
    """Prints out the search results and writes them to file."""
    if results:
        for idx, url in enumerate(results, 1):
            print(f"{idx}: {url}")
    else:
        print("No results found.")
    choice = input("Would you like to output results to a txt file? (y/n): ").strip().lower()
    if choice == "y":
        write_results(results)
        print("Exported To Results/Output.txt")
    print_congrats_ascii()


def search_usa(first_name, last_name):
    """
    Search logic for the USA using TruePeopleSearch.
    Prints found records to the CLI and offers an option to export to txt.
    """
    state = input(Colors.cyan + "State abbreviation (e.g., FL) [optional] --> ").strip()
    base_url = f'https://truepeoplesearch.net/search?first_name={first_name}&last_name={last_name}'
    url = f"{base_url}&state={state}" if state else base_url

    # Use a user-agent header to increase compatibility
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving USA search: {e}")
        return
    time.sleep(response_time)

    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if tag:
        try:
            json_data = tag.string.strip()
            if json_data.startswith("var"):
                json_data = json_data.split('=', 1)[1].strip().rstrip(';')
            data = json.loads(json_data)
            people_list = data['props']['pageProps'].get('people_list', [])
            if not people_list:
                print("No results found.")
            else:
                print("\nUSA Search Results:")
                for idx, person in enumerate(people_list, start=1):
                    print(f"Result {idx}:")
                    for key, value in person.items():
                        print(f"   {key}: {value}")
                    print("-" * 40)
            # Ask if the user wants to output the results to txt
            choice = input("Would you like to output these results to a txt file? (y/n): ").strip().lower()
            if choice == "y":
                result = {"people_list": people_list}
                write_results(result)
                print("Exported To Results/Output.txt")
            print_congrats_ascii()
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(json_data)
    else:
        print("Script tag with JSON data not found.")


def search_india(first_name, last_name):
    """Search logic for India."""
    results = {}
    url = f'https://radaris.in/person/{first_name}/{last_name}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving India search: {e}")
        return
    time.sleep(response_time)
    soup = BeautifulSoup(response.text, 'html.parser')
    full_name_tag = soup.find('h1', id='fullname_top')
    if full_name_tag:
        full_name = full_name_tag.text.strip()
        print(f"Full Name: {full_name}")
        results['full_name'] = full_name
    relatives_section = soup.find('div', id='namesakes')
    if relatives_section:
        print("\nPossible Relatives:")
        relatives_list = [rel.text.strip() for rel in relatives_section.find_all('a')]
        for relative in relatives_list:
            print(f"- {relative}")
        results['possible_relatives'] = relatives_list
    socials_section = soup.find(id='socials')
    if socials_section:
        print("\nSocial Media Profiles:")
        socials_info = {'xing': [], 'linkedin': []}
        for profile in socials_section.find_all('div', class_='card-data-item'):
            title = profile.find('span', class_='title')
            if title:
                locality_tag = profile.find('dd')
                job_tag = locality_tag.find_next('dd') if locality_tag else None
                print(f"Xing: {title.text.strip()}")
                if locality_tag and job_tag:
                    print(f"   Locality: {locality_tag.text.strip()}")
                    print(f"   Job: {job_tag.text.strip()}")
                xing_data = {
                    'name': title.text.strip(),
                    'locality': locality_tag.text.strip() if locality_tag else None,
                    'job': job_tag.text.strip() if job_tag else None
                }
                socials_info['xing'].append(xing_data)
        for profile in socials_section.find_all('div', class_='card-data-item'):
            title = profile.find('span', class_='title')
            if title:
                locality_tag = profile.find('dd')
                summary_tag = locality_tag.find_next('dd') if locality_tag else None
                print(f"LinkedIn: {title.text.strip()}")
                if locality_tag and summary_tag:
                    print(f"   Locality: {locality_tag.text.strip()}")
                    print(f"   Summary: {summary_tag.text.strip()}")
                linkedin_data = {
                    'name': title.text.strip(),
                    'locality': locality_tag.text.strip() if locality_tag else None,
                    'summary': summary_tag.text.strip() if summary_tag else None
                }
                socials_info['linkedin'].append(linkedin_data)
        results['socials'] = socials_info
    result = {"results": results}
    print("Exported To Results/Output.txt")
    write_results(result)
    print_congrats_ascii()


def search_bac(first_name, last_name):
    """Search logic for Canada (BAC-LAC)."""
    url = f'https://www.bac-lac.gc.ca/eng/discover/vital-statistics-births-marriages-deaths/births-marriages-deaths-recorded/Pages/list.aspx?Surname={last_name}&GivenName={first_name}&'
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving Canada search: {e}")
        return
    time.sleep(response_time)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    table_rows = soup.select('#result_table tbody tr')
    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            item = {
                'item_number': cols[0].text.strip(),
                'surname': cols[1].text.strip(),
                'given_name': cols[2].text.strip(),
                'location': cols[3].text.strip()
            }
            results.append(item)
    json_output = json.dumps(results, indent=4)
    print(json_output)
    result = {"results": json_output}
    print("Exported To Results/Output.txt")
    write_results(result)
    print_congrats_ascii()


def search_nigeria(first_name, last_name):
    """Search logic for Nigeria (nigeriaphonebook)."""
    url = f'https://nigeriaphonebook.com/search-result?startWidth=o&searchKey={first_name}+{last_name}&contactState=&contactLga=&contactGender='
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving Nigeria search: {e}")
        return
    time.sleep(response_time)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile = soup.find('div', class_='filter-search-cont-list')
    if profile:
        try:
            extracted_info = {
                'name': profile.find('h4', itemprop='name').text.strip(),
                'telephone': profile.find('span', itemprop='telephone').text.strip(),
                'state': profile.find('span', itemprop='addressRegion').text.strip(),
                'lga': profile.find('span', itemprop='addressLocality').text.strip(),
                'gender': profile.find('span', itemprop='gender').text.strip()
            }
            print(extracted_info)
            write_results(extracted_info)
            print_congrats_ascii()
        except AttributeError as e:
            print("Error extracting profile information:", e)
    else:
        print("Profile information not found in the response.")


def search_general(first_name, last_name):
    """Generic Bing search for any other country options."""
    query = f"{first_name} {last_name}"
    time.sleep(response_time)
    results = bing_search(query)
    process_and_print_results(results)


def settings_and_transparency_menu():
    """
    Displays a sub-menu for 'Settings and Transparency'.
    Allows toggling or updating APIs (placeholder),
    and clarifies which APIs are currently used.
    """
    clear_screen()
    print_banner("Settings")
    print(Colors.cyan + "=== Settings and Transparency ===\n")
    print(Colors.cyan + "1) Transparency - View APIs in use")
    print(Colors.cyan + "2) Toggle / Update API usage (placeholder)")
    print(Colors.cyan + "3) Return to Main Menu\n")
    
    choice = input(Colors.cyan + " --> ").strip()
    if choice == "1":
        clear_screen()
        print_banner("APIs")
        print(Colors.cyan + "=== APIs Currently in Use ===\n")
        for api in API_SOURCES:
            print(f" - {api}")
        input("\nPress Enter to return...")
        settings_and_transparency_menu()
    elif choice == "2":
        clear_screen()
        print_banner("Update")
        print(Colors.cyan + "=== Toggle / Update API usage (Placeholder) ===\n")
        print("In a real application, you'd have logic here to enable or disable certain APIs.")
        input("\nPress Enter to return...")
        settings_and_transparency_menu()
    elif choice == "3":
        main()
    else:
        print("Invalid option. Returning to main menu.")
        time.sleep(1)
        main()


def main():
    clear_screen()
    print_banner("peepler")
    # Print the menu options in a more aligned, easy-to-read format
    print(Colors.cyan + "1: USA         2: India       3: Canada")
    print(Colors.cyan + "4: China       5: Indonesia   6: Brazil")
    print(Colors.cyan + "7: Nigeria     8: Japan       9: Russia")
    print(Colors.cyan + "10: Settings and Transparency\n")
    
    option = input(Colors.cyan + "--> ").strip()

    # Mapping options to corresponding search functions.
    if option == "1":
        first_name, last_name = get_name_input()
        search_usa(first_name, last_name)
    elif option == "2":
        first_name, last_name = get_name_input()
        search_india(first_name, last_name)
    elif option == "3":
        first_name, last_name = get_name_input()
        search_bac(first_name, last_name)
    elif option == "7":
        first_name, last_name = get_name_input()
        search_nigeria(first_name, last_name)
    elif option in {"4", "5", "6", "8", "9"}:
        first_name, last_name = get_name_input()
        search_general(first_name, last_name)
    elif option == "10":
        settings_and_transparency_menu()
    else:
        print("Invalid option selected.")
        time.sleep(1)
        main()

    input("Press Enter To Go To Main Menu")
    main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colors.red + "\nExiting... Goodbye")
        sys.exit(0)
