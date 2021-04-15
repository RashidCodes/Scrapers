<h1>Scrape the data of linkedin members</h1>
Please note that this activity is a breach of terms and conditions associated with the usage of LinkedIn. This code was created solely for educational purposes. Your account WILL BE RESTRICTED if suspicious activity is detected.

<br/>

<h1>Data</h1>
The scraper returns some personal information of the member, their educational qualifications, work experiences and certifications.

<br/>

<h1>Requirements</h1>

    - An HTML parser eg. lxml
    - Selenium
    - BeautifulSoup

<br/>

<h1>Usage</h1>

<h2> Scraping data from a single profile</h2>

```bash
>>> import uuid
>>> profile_link = "https://www.linkedin.com/in/alexnalmpantis/?originalSubdomain=uk"
>>> Id = str(uuid.uuid4())

>>> alexander = ScrapeLinkedin("yourEmail@email.com", "yourPassword", profile_link, Id)
>>> alexander.scrape()
Entering your username...
Entering your password...
Signing you in...
Successfully signed in. Proceeding to another profile.
Scraping...
No certifications
Done scraping.

>>> alexander.get_name()
'Alexander Nalmpantis'

>>> alexander.get_location()
'London, Greater London, United Kingdom'

>>> alexander.get_education()
[('d10a208c-2375-421d-b450-34e1341ecb21',
  'City University London',
  "Master's degree Data Science"),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'Harvard Business School',
  'Core: Credential of Readiness'),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'Technologiko Ekpaideutiko Idrima, Kavalas',
  'Bachelor of Engineering (BEng) Petroleum and Natural Gas Engineering')]

>>> alexander.get_experience()
[('d10a208c-2375-421d-b450-34e1341ecb21',
  'BP',
  None,
  'Lead Data Scientist',
  'Dec 2018',
  'Present',
  None),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'Deloitte',
  None,
  'Manager - Analytics & Modelling',
  'Apr 2017',
  'Dec 2018',
  'London, United Kingdom'),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'IHS Consulting',
  None,
  'Business Analyst - Upstream Consulting',
  'Oct 2014',
  'Mar 2017',
  'London, United Kingdom'),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'GlobalData',
  None,
  'Oil & Gas Analyst',
  'Jan 2014',
  'Oct 2014',
  'London, United Kingdom'),
 ('d10a208c-2375-421d-b450-34e1341ecb21',
  'Chatzikosmas Co',
  None,
  'Production Engineer',
  'Sep 2008',
  'Oct 2012',
  'Greece')]

>>> alexander.save()
Successfully saved scientist
Successfully saved experiences
Successfully saved qualifications
Successfully saved certifications
```

<br/>

<h2>Scraping data from multiple profiles</h2>

The data is automatically stored in an SQLite database.

```bash
>>> unscraped_urls = ["member1_url", "member2_url"]
>>> scrape_multiple = ScrapeLinkedinM("yourEmail@email.com", "yourPassword", unscraped_urls)
>>> scrape_multiple.scrape_save()
Entering your username...
Entering your password...
Signing you in...
Successfully signed in.
Scraping member1_url...
No certifications
Done scraping
Saving all credentials...
Successfully saved scientist
Successfully saved experiences
Successfully saved qualifications
Sleeping for approximately 3 minutes
```
