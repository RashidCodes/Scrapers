import uuid
import sqlite3
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
import time
from random import randrange
from math import ceil
from selenium.webdriver.common.by import By

class ScrapeLinkedinM:
    """Scrape the data of multiple linkedin members with your linkedin profile. Note that
    this is a breach of the terms and conditions associated with the usage of Linkedin.

    Your account WILL BE RESTRICTED if suspicious activity is detected.
    
    Attributes
    ----------
    email: String
    Your email address eg. yourEmail@email.com

    password: String
    Your password

    profiles: List of strings
    A list of linkedin profile links

    db_path: String
    The path of the SQLite database
    

    """
    
    URL = "https://linkedin.com"
 
    def __init__(self, email, password, profiles, db_path="ScientistsDB.db"):
        self._email = email
        self._password = password
        self._db_path = db_path
        self._profiles = profiles
        
    def __repr__(self):
        return "ScrapeLinkedinM"
    
    @staticmethod
    def insert_scientist(db_path, Id, firstname, lastname, title, connections, location=None):
        conn = sqlite3.connect(db_path)
        data = (Id, firstname, lastname, title, location, connections)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO tblScientist VALUES (?, ?, ?, ?, ?, ?) ", data)
            conn.commit()
            conn.close()

        except Exception:
            conn.close()
    

    @staticmethod
    def insert_experience(db_path, experiences):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        try:
            cur.executemany('INSERT INTO tblExperience VALUES (?, ?, ?, ?, ?, ?, ?)', experiences)
            conn.commit()
            conn.close()

        except Exception:
            conn.close()
        

    @staticmethod
    def insert_education(db_path, education):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        try:
            cur.executemany('INSERT INTO tblEducation VALUES (?, ?, ?)', education)
            conn.commit()
            conn.close()  

        except Exception:
            conn.close()
        

    @staticmethod
    def insert_certification(db_path, certifications):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        try:
            cur.executemany('INSERT INTO tblCertificates VALUES (?, ?, ?)', certifications)
            conn.commit()
            conn.close()

        except Exception:
            conn.close()

    
    @staticmethod
    def save_success(link):
        with open('success.txt', 'a') as success_file:
            success_file.write(link + "\n")
     

    @staticmethod
    def extract_connections(conn_string):
        if "+" in conn_string:
            return int(conn_string.split("+")[0])

        elif " " in conn_string:
            return int(conn_string.split(" ")[0])

        else:
            return

        
    

    def parse_experience(self, item, scientist_Id):
    
        ## Not a timeline item
        ul = item.find('ul')

        if ul:
            # get all timeline experiences
            return self.get_more(item, scientist_Id)


        # role
        try:
            role = item.find('h3').text.strip()

        except:
            role = None



        # company
        try:
            company = item.find('p', class_="pv-entity__secondary-title").contents

        except:
            company_name, employment_type = None, None

        else:
            company_name = company[0].strip()

            try:
                employment_type = company[1].text.strip()

            except:
                employment_type = None


        # start and end dates
        find_date_range = item.find('h4', class_="pv-entity__date-range")
        date_range = find_date_range.find_all('span')
        split_dates = date_range[1].text.split("–")

        if(len(split_dates) == 1):
            start_date = split_dates[0].strip()
            end_date = None

        else:
            start_date, end_date = split_dates[0].strip(), split_dates[1].strip()


        # location
        try:
            location = item.find('h4', class_="pv-entity__location").find_all('span')[1].text.strip()

        except:
            location = None


        return [(scientist_Id, company_name, employment_type, role, start_date, end_date, location)]
    

    @staticmethod
    def parse_education(edu, scientist_Id):
        """Parses education information"""

        try:
            school_name = edu.find('h3', class_ = 'pv-entity__school-name').text
            
        except:
            school_name = None
            
        try:
            list_of_paragraphs = edu.find('div', class_="pv-entity__degree-info").find_all('p')
            degree = " ".join([p.find('span', class_="pv-entity__comma-item").text for p in list_of_paragraphs]).strip()
            
        except:
            degree = None

        return [(scientist_Id, school_name, degree)]
    

    @staticmethod
    def parse_certificate(cert, scientist_Id):
        """Parse certificate information"""

        try:
            certificate = cert.find('h3', class_="t-16").string.strip()
        except:
            certificate = None

        try:
            issuer = cert.find('div', class_="pv-certifications__summary-info").find('p').contents[3].string.strip()
        except:
            issuer = None

        return [(scientist_Id, certificate, issuer)]
    
    
    def get_more(self, list_with_ul, scientist_Id):
    
        # timeline experiences
        tl_exps = []

        company_tag, ul_tag = list_with_ul.find('h3'), list_with_ul.find('ul')

        if (company_tag and ul_tag) != None:
            for list_tag in ul_tag.find_all('li'):
                tl_exps.append(self.get_tl_exp(scientist_Id, company_tag, list_tag))

            return tl_exps

        print("No unordered list was detected")
        
    
    @staticmethod
    def get_tl_exp(scientist_Id, company_tag, item):
    
        # employement type
        employment_type = None

        # role
        try:
            role = item.find('h3').find_all('span')[1].text.strip()

        except:
            role = None


        # company
        try:
            company_name = company_tag.find_all('span')[1].text.strip()

        except:
            company_name = None


        # start and end dates
        find_date_range = item.find('h4', class_="pv-entity__date-range")
        date_range = find_date_range.find_all('span')
        split_dates = date_range[1].text.split("–")

        if(len(split_dates) == 1):
            start_date = split_dates[0].strip()
            end_date = None

        else:
            start_date, end_date = split_dates[0].strip(), split_dates[1].strip()


        # location
        try:
            location = item.find('h4', class_="pv-entity__location").find_all('span')[1].text.strip()

        except:
            location = None


        return (scientist_Id, company_name, employment_type, role, start_date, end_date, location)

    

    def scrape_save(self):    
        """Scrape the data of each member""" 
        try:
            ## navigate to the linkedIN profile
            linkedIn_driver = Firefox(executable_path='./geckodriver')
            linkedIn_driver.get(self.URL)

            # Sign In...
            try:
                toggle_button = linkedIn_driver.find_element(By.CLASS_NAME, 'nav__button-secondary')
                toggle_button.click()

                time.sleep(2)

                ## fill the form
                try:
                    ## find the username input 
                    username = linkedIn_driver.find_element(By.ID, 'username')       

                    ## find the password input
                    password = linkedIn_driver.find_element(By.ID, 'password')

                    ## find the sign In button
                    sign_in = linkedIn_driver.find_element(By.XPATH, '//button[@type="submit"]')


                except Exception as e:
                    print('An error occured, probably one of the inputs was not found. Check error log!')
                    print()
                    print(e)

                ## no exception was raised, meaning all inputs were found
                else:
                    print("Entering your username...")
                    username.send_keys(self._email)

                    time.sleep(1)

                    print('Entering your password...')
                    password.send_keys(self._password)

                    time.sleep(1)

                    print('Signing you in...')
                    sign_in.click()
                    print('Successfully signed in.')

                    time.sleep(5)

                    self.counter = 0

                    
                    ## start scraping all profiles
                    for profile in self._profiles:

                        self._scientist_Id = str(uuid.uuid4())
                        
                        ## navigate to the new profile
                        try:             
                            linkedIn_driver.get(profile)
                            print("Scraping {}...".format(profile))

                            # wait for the page to finish loading
                            time.sleep(5)

                            # for redirects
                            if (profile != linkedIn_driver.current_url):
                                linkedIn_driver.get(linkedIn_driver.current_url)
                                time.sleep(5)

                        except Exception as e:
                            print("Unable to navigate to: {}.".format(profile))
                            print()
                            print(e)


                        else:
                            ## Scientist name
                            try:
                                name = linkedIn_driver.find_element(By.CSS_SELECTOR, ".pv-top-card--list li:nth-of-type(1)").text

                            except:
                                self.scientist_firstname, self.scientist_lastname = None, None

                            else:
                                scientist = name.split(" ")

                                # if the scientist has one name
                                if len(scientist) == 1:
                                    self.scientist_firstname = scientist[0].strip()
                                    self.scientist_lastname = None
                                    return

                                self.scientist_firstname = scientist[0].strip()
                                self.scientist_lastname = scientist[1].strip()


                            ## Title
                            try:
                                self.scientist_title = linkedIn_driver.find_element(By.CSS_SELECTOR, ".pb5 h2").text

                            except:
                                print("No title")
                                self.scientist_title = None


                            ## Location
                            try:
                                self.location = linkedIn_driver.find_element(By.CSS_SELECTOR, ".pv-top-card--list-bullet li:nth-of-type(1)").text

                            except:
                                print("No location")
                                self.location = None


                            ## Connections
                            try:
                                number = linkedIn_driver.find_element(By.CSS_SELECTOR, '.pv-top-card--list-bullet li:nth-of-type(2) span').text
                                self.connections = self.extract_connections(number)

                            except Exception as e:

                                print("No connections")
                                print(e)
                                self.connections = None



                            ## Experience
                            try:
                                exp_section = linkedIn_driver.find_element(By.CSS_SELECTOR, ".pv-profile-section.experience-section").get_attribute('innerHTML')

                            except:
                                print("No experience")
                                self.all_experiences = None
                                
                            else:
                                experience = BeautifulSoup(exp_section, 'lxml')
                                experience_list = experience.find_all('li', class_="pv-entity__position-group-pager")
                                self.all_experiences = []
                                for item in experience_list:
                                    self.all_experiences.extend(self.parse_experience(item, self._scientist_Id))


                            ## Education
                            try:
                                edu_section = linkedIn_driver.find_element(By.CSS_SELECTOR, ".education-section").get_attribute('innerHTML')

                            except:
                                print("No education")
                                self.all_education = None

                            else:
                                education = BeautifulSoup(edu_section, 'lxml')
                                education_list = education.find_all('li')
                                self.all_education = []
                                for edu_item in education_list:
                                    self.all_education.extend(self.parse_education(edu_item, self._scientist_Id))


                            ## Certifications
                            try:
                                cert = linkedIn_driver.find_element(By.CSS_SELECTOR, '.certifications-section').get_attribute("innerHTML")

                            except:
                                print("No certifications")
                                self.all_certifications = None

                            else:
                                certifications = BeautifulSoup(cert, 'lxml')
                                cert_list = certifications.find_all('li')
                                self.all_certifications = []
                                for cert_item in cert_list:
                                    self.all_certifications.extend(self.parse_certificate(cert_item, self._scientist_Id))

                            print("Done scraping")

                            ## save the profile
                            self.save_success(profile)

                            ## increase the counter
                            self.counter += 1

                            if (self.all_education and self.all_experiences):
                                ## save attributes 
                                self.save()

                            if(self.counter >=  50):
                                print("You've scraped more than {} profiles today. Please quit the scraper".format(self.counter))

                            ## sleep
                            sleep = randrange(60, 200, 1)
                            print("Sleeping for approximately {} minutes".format(ceil(sleep / 60)))
                            time.sleep(sleep)
                            print()


            except Exception as e:
                print("Sign In screen probably did not appear. Check error logs!")
                print(e)

        except Exception as e:
            print("Unable to navigate to linkedIn.com. Perhaps you have a bad internet connection. Check error logs!")
            print()
            print(e)

        finally:
            linkedIn_driver.quit()


    def save(self):
        """Save the data of a linkedin member"""
        
        print("Saving all credentials...")

        check = self._db_path and self._scientist_Id and self.scientist_firstname and  self.scientist_title and \
            self.scientist_lastname and self.connections and self.location

        if (check):
            self.insert_scientist(self._db_path, self._scientist_Id, self.scientist_firstname, self.scientist_lastname, \
                self.scientist_title, self.connections, self.location)
            print("Successfully saved scientist")

        if (check and self.all_experiences):
            self.insert_experience(self._db_path, self.all_experiences)
            print("Successfully saved experiences")

        if (check and self.all_education):
            self.insert_education(self._db_path, self.all_education)
            print("Successfully saved qualifications")

        if (check and self.all_certifications):
            self.insert_certification(self._db_path, self.all_certifications)
            print("Successfully saved certifications")

            
        
    