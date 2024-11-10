import praw
from datetime import date
from dotenv import load_dotenv, dotenv_values 

# global to unlock PRAW API
config = dotenv_values(".env") 


''' Class: wrapper for praw library meant to customize reddit scraper
to contain keyword, subreddit, and then write to files 
    Purpose: scrapes reddit content in a specific subreddit'''

class RedditScraper:
    def __init__(self, reddit, query, subreddit=None):
        # initialize scraper
        self.scraper = reddit
        self.keywords = query
        self.sub = subreddit
        self.posts = []

# refine to prioritize posts with max amount of keywords
    def search_subreddit_by_keywords(self, limit=100):
        assert self.sub is not None, "Subreddit not specified, use other search method"
        keyword_list = self.keywords.split("OR")
        subreddit = self.scraper.subreddit(self.sub)
        searchedPosts = subreddit.search(self.keywords,limit=limit)

        for post in searchedPosts:
         # Check if the post contains any of the keywords in the title or content
            title = post.title.lower()
            content = post.selftext.lower()
            
            match_count = sum(keyword in title or keyword in content for keyword in keyword_list)
            # store in custom scraper
            self.posts.append({
                'title': post.title,
                'content': post.selftext,
                'url': post.url,
                'matches': match_count
            })

    def get_str_keywords(self, keywords):
        output = ""
        for i in keywords:
            output += i
            if i != (len(keywords) - 1):
                output += ", "
        return(output)

    def get_num_posts(self):
        return len(self.posts)

    def output_posts_found(self, file):
        keyword_list = self.keywords.split("OR")
        file.write(f"*" * 80)
        file.write(f"\n \n Subreddit: {self.sub}   Keywords: {self.get_str_keywords(keyword_list)}\n")
        for post in self.posts:
        
            title = f"\nPost: {post['title']}\n"
            file.write(title)
            print(title)
            content = f"Content: {post['content']} \n"
            ''' matches = f"Matches: {post['matches']} \n"
            print(matches)
            file.write(matches)'''
            print(content)
            file.write(content)
            breaker = "-" * 80
            file.write(f" \n Url: {post['url']} \n" )
            file.write(f"{breaker} \n" )
            print(f"Url: {post['url']}")  # Show only the first 300 characters
            print(breaker)


if __name__ == "__main__":
    # set up reddit scraper
    reddit = praw.Reddit(
        client_id=config['REDDIT_CLIENT_ID'],
        client_secret=config['REDDIT_CLIENT_SECRET'],
        user_agent=config['REDDIT_USER_AGENT'])
    # establish keywords for each case has to use OR delimiter to comply with PRAW search query format
    case_1 = "immigrants OR illegals OR springfield OR border OR globalist OR crime OR fake ID"
    case_2 = "gender reassignment AND immigrant"
    case_3 = "transgender AND bathroom OR sexual assault"
    case_1_list = case_1.split("OR")
    case_2_list = case_2.split("OR")
    case_3_list = case_3.split("OR")



    


