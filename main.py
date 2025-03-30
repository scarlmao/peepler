import requests
import json
import os
from pystyle import Colors, Colorate, Center, Box
import time
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse, urljoin

with open("config.json", "r") as file:
    config = json.load(file)
    response_time = config.get("response_time")

def bing_search(query):

    query = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q={query}"

    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http') or href.startswith('www'):
                search_results.append(href)

        return search_results
    else:
        print(f"Error: {response.status_code}")
        return []
   
def main():
    os.system('cls')
    banner = r"""
                               .__                
   ______   ____   ____ ______ |  |   ___________ 
   \____ \_/ __ \_/ __ \\____ \|  | _/ __ \_  __ \
   |  |_> >  ___/\  ___/|  |_> >  |_\  ___/|  | \/          Search Over 2 Billion People
   |   __/ \___  >\___  >   __/|____/\___  >__|   
   |__|        \/     \/|__|             \/       

      1 : USA      2: India      3: Canada
      4 : China    5: Indonesia  6: Brazil
      7 : Nigeria  8: Japan      9: Russia
      
"""
    print((Colorate.Vertical(Colors.cyan_to_green, banner,1)))
    option = input(Colors.cyan + " --> ")

    if option == "9":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       time.sleep(response_time)
       query = First_name + ' ' + Last_name
       results = bing_search(query)
        
       if results:
            for idx, url in enumerate(results, 1):
                print(f"{url}")
       else:
            print("")
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(results, indent=4))
          input("Press Enter To Go To Main Menu")
          main()

    if option == "8":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       time.sleep(response_time)
       query = First_name + ' ' + Last_name
       results = bing_search(query)
        
       if results:
            for idx, url in enumerate(results, 1):
                print(f"{url}")
       else:
            print("")
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(results, indent=4))
          input("Press Enter To Go To Main Menu")
          main()

    if option == "7":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       response = requests.get(f'https://nigeriaphonebook.com/search-result?startWidth=o&searchKey={First_name}+{Last_name}&contactState=&contactLga=&contactGender=')
       time.sleep(response_time)
       soup = BeautifulSoup(response.text, 'html.parser')

    profile = soup.find('div', class_='filter-search-cont-list')  
    
    if profile:
        name = profile.find('h4', itemprop='name').text.strip()

        telephone = profile.find('span', itemprop='telephone').text.strip()

        state = profile.find('span', itemprop='addressRegion').text.strip()

        lga = profile.find('span', itemprop='addressLocality').text.strip()

        gender = profile.find('span', itemprop='gender').text.strip()

        extracted_info = {
            'name': name,
            'telephone': telephone,
            'state': state,
            'lga': lga,
            'gender': gender
        }

        print(extracted_info)
    else:
        print("Profile information not found in the response.")

    with open("results/output.txt", "w") as file:
          file.write(json.dumps(extracted_info, indent=4))
          input("Press Enter To Go To Main Menu")
          main()


    if option == "6":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       time.sleep(response_time)
       query = First_name + ' ' + Last_name
       results = bing_search(query)
        
       if results:
            for idx, url in enumerate(results, 1):
                print(f"{url}")
       else:
            print("")
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(results, indent=4))
          input("Press Enter To Go To Main Menu")
          main()


    if option == "5":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       time.sleep(response_time)
       query = First_name + ' ' + Last_name
       results = bing_search(query)
        
       if results:
            for idx, url in enumerate(results, 1):
                print(f"{url}")
       else:
            print("")
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(results, indent=4))
          input("Press Enter To Go To Main Menu")
          main()

    if option == "4":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       time.sleep(response_time)
       query = First_name + ' ' + Last_name
       results = bing_search(query)
        
       if results:
            for idx, url in enumerate(results, 1):
                print(f"{url}")
       else:
            print("")
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(results, indent=4))
          input("Press Enter To Go To Main Menu")
          main()


    if option == "3":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       r = requests.get(f'https://www.bac-lac.gc.ca/eng/discover/vital-statistics-births-marriages-deaths/births-marriages-deaths-recorded/Pages/list.aspx?Surname={Last_name}&GivenName={First_name}&')
       soup = BeautifulSoup(r.text, 'html.parser')
       time.sleep(response_time)
       results = []
       table_rows = soup.select('#result_table tbody tr')
       for row in table_rows:
        item_number = row.find('td').text.strip()  
        surname = row.find_all('td')[1].text.strip()  
        given_name = row.find_all('td')[2].text.strip()  
        location = row.find_all('td')[3].text.strip()  
    
        results.append({
        'item_number': item_number,
        'surname': surname,
        'given_name': given_name,
        'location': location
    })
       json_output = json.dumps(results, indent=4)

       print(json_output)
       result = {
            "results": json_output
        }
       print("Exported To Results/Output.txt")        
       if not os.path.exists("results"):
        os.makedirs("results")
        
       with open("results/output.txt", "w") as file:
          file.write(json.dumps(result, indent=4))
          input("Press Enter To Go To Main Menu")
          main()

    if option == "2":
      First_name = input(Colors.cyan + "First Name --> ")
      Last_name = input(Colors.cyan + "Last Name --> ")
      results = {}
      response = requests.get(f'https://radaris.in/person/{First_name}/{Last_name}/')
      time.sleep(response_time)
      soup = BeautifulSoup(response.text, 'html.parser')
      full_name = soup.find('h1', id='fullname_top')
      if full_name:
          print(f"Full Name: {full_name.text.strip()}")
          results['full_name'] = full_name.text.strip()

      

      relatives_section = soup.find('div', id='namesakes')
      if relatives_section:
          print("\nPossible Relatives:")
          relatives_list = relatives_section.find_all('a')
          for relative in relatives_list:
              print(f"- {relative.text.strip()}")
              results['possible_relatives'] = relatives_list

      socials_section = soup.find(id='socials')
      if socials_section:
          print("\nSocial Media Profiles:")
          socials_info = {'xing': [], 'linkedin': []}

          xing_profiles = socials_section.find_all('div', class_='card-data-item')
          for profile in xing_profiles:
              title = profile.find('span', class_='title')
              if title:
                  locality = profile.find('dd')
                  job = locality.find_next('dd') if locality else None
                  print(f"Xing: {title.text.strip()}")
                  if locality and job:
                      print(f"  Locality: {locality.text.strip()}")
                      print(f"  Job: {job.text.strip()}")
                      xing_data = {
                'name': title.text.strip(),
                'locality': locality.text.strip() if locality else None,
                'job': job.text.strip() if job else None
            }
                      socials_info['xing'].append(xing_data)
                     

          linkedin_profiles = socials_section.find_all('div', class_='card-data-item')
          for profile in linkedin_profiles:
              title = profile.find('span', class_='title')
              if title:
                  locality = profile.find('dd')
                  summary = locality.find_next('dd') if locality else None
                  print(f"LinkedIn: {title.text.strip()}")
                  if locality and summary:
                      print(f"  Locality: {locality.text.strip()}")
                      print(f"  Summary: {summary.text.strip()}")
                      linkedin_data = {
                'name': title.text.strip(),
                'locality': locality.text.strip() if locality else None,
                'summary': summary.text.strip() if summary else None
            }
                      socials_info['linkedin'].append(linkedin_data)

      result = {
            "results": results
        }
      print("Exported To Results/Output.txt")                
      with open("results/output.txt", "w") as file:
          file.write(json.dumps(result, indent=4))
          input("Press Enter To Go To Main Menu")
          main()
          

    if option == "1":
       First_name = input(Colors.cyan + "First Name --> ")
       Last_name = input(Colors.cyan + "Last Name --> ")
       State = input(Colors.cyan + "State ex. Fl--> ")
       
       response = requests.get(f'https://truepeoplesearch.net/search?first_name={First_name}&last_name={Last_name}&state={State}')
       time.sleep(response_time)
       
       soup = BeautifulSoup(response.text, 'html.parser')
       
       tag = soup.find('script', {'id': '__NEXT_DATA__'})
       if tag:
        try:
         json_data = tag.string.strip()

         if json_data.startswith("var"):
            json_data = json_data.split('=')[1].strip().rstrip(';')

         data = json.loads(json_data)
         people_list = data['props']['pageProps']['people_list']
        
         result = {
            "people_list": people_list
        }

         print((Colorate.Vertical(Colors.cyan_to_green, json.dumps(result, indent=4)))) 
         print("Exported To Results/Output.txt")
         if not os.path.exists('results'):
          os.makedirs('results')

         with open("results/output.txt", "w") as file:
          file.write(json.dumps(result, indent=4))
         input("Press Enter To Go To Main Menu")
         main()
         


         
        except json.JSONDecodeError as e:
         print(f"Error parsing JSON: {e}")
         print(json_data)  
        

    
    

if __name__ == "__main__":
 main()