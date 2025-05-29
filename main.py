from helper.submit_confession import submit_petfess
from helper.scraper import Scraper

# submission = "hello world x2!"
# submit_petfess(submission, open_GUI=True)

scraper = Scraper(open_GUI=True)
post = scraper.get_latest_post()
print(post)
