# LGBTQ Op Ed Tool

## Description:
Disinfolab is the first undergraduate led political misinformation think tank where student research groups produce their own investigation into contentious disinformation on the internet.
This automated data collection tool is meant to scrape social media content identified as disinformation in order to support a political op-ed article investigating the spread and influence of untrue homophobic narratives on social media.
The content is then analyzed for performance metrics to identify patterns in the content trail that parallels Russia's Firehose of Falsehoods propaganda strategy. 

Firehose of Falsehoods model is distinguished by these factors:
- Content is spread in high volume, and multiple channels
- Content is rapid, continuous, and repetitive
- Content lacks commitment to objective reality
- Content lacks consistency


## Installation

Clone the repo: 
```
git clone [link to repo]
```

Set up all necessary dependencies in your own virtual environment by running on your command-line first:
```
python -m venv virtualenv
```
Then activate it according to your computer:
### macOS (or Linux)
```
source virtualenv/bin/activate
```
### Windows
```
./virtualenv\Scripts\activate
```

Then once the environment is active, run the following command to download all needed dependencies: 
```pip install -r requirements.txt```

## Usage
Populate the links.txt to run the Facebook scraper to run through posts you would like to gather the comments from. For the reddit scraper utilize the custom class that queries subreddits for specific keywords. 
