import uuid
from ScrapeLinkedin import ScrapeLinkedin
profile_link = "https://www.linkedin.com/in/alexnalmpantis/?originalSubdomain=uk"
Id = str(uuid.uuid4())

# a path to an SqliteDB is not required
alexander = ScrapeLinkedin("yourEmail@email.com", "yourPassword", profile_link, Id, "optional/path/to/sqlite.db"
alexander.scrape()

print(alexander.get_name())
print(alexander.get_experience())