# horse-race-winner-predictor
Predicting winning scores of horses in Horse race betting at winningform.co.za (desktop application). It was built using Python3 and PyQt5.

## Basic algorithm of how it works:
The application works on the basis of web scraping.
- Users choose the city and race they want to check the winning scores
- The scraper then scrapes the race page, extracts all the data points for each of the horses. Two functions have been designed to take care of it, they are: _extractHorseInfo()_ and _extractRaceInfo()_. The data points were: 
`['Rank','Name','Jockey','Trainer','HorseNo','Odds','Last3','Draw','Distance','Total Runs','WeightRate','Rating','Stakes','Total Factor']`
- The race analysis is then generated based on a set of metrics and equations using this function _generateAnalysis()_. 

## Resources used
- PyQt5
- BeautifulSoup4
- sqlite3
