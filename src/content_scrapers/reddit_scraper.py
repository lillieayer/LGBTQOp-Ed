import praw
from datetime import date


''' Class: wrapper for praw library meant to customize reddit scraper
to contain keyword, subreddit, and then write to files'''
class RedditScraper:
    def __init__(self, reddit, subreddit, query):
        # initialize scraper
        self.scraper = reddit
        self.keywords = query
        self.sub = subreddit
        self.posts = []


# refine to prioritize posts with max amount of keywords
    def find_posts_by_keyword(self, limit=100):
        subreddit = self.scraper.subreddit(self.sub)
        searchedPosts = subreddit.search(self.keywords,limit=limit)
        keyword_list = self.keywords.split("OR")
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
        client_id="U9MHvmfw08K75qXHwiUt4w",
        client_secret="zPuqIlajupd4wxR2a-DpM2hTtqkJXQ",
        user_agent="MyRedditScraper/Lillie Ayer")
    # establish keywords for each case
    case_1 = "immigrants OR illegals OR springfield OR border OR globalist OR crime OR fake ID"
    case_2 = "gender reassignment AND immigrant"
    case_3 = "transgender AND bathroom OR sexual assault"
    case_1_list = case_1.split("OR")
    case_2_list = case_2.split("OR")
    case_3_list = case_3.split("OR")
    # create custom scraper objects for each subreddit/keyword combo
    scrape1 = RedditScraper(reddit, "conservative", case_1)
    scrape2 = RedditScraper(reddit, 'politics', case_1)
    scrape3 = RedditScraper(reddit, 'tucker_carlson', case_1)
    scrape4 = RedditScraper(reddit, 'immigration', case_1)
    scrape5 = RedditScraper(reddit, "conservative", case_2)
    scrape6 = RedditScraper(reddit, 'politics', case_2)
    scrape7 = RedditScraper(reddit, 'immigration', case_2)
    scrape8 = RedditScraper(reddit, 'counteveryvote', case_2)
    # save all scrapers to loop through
    channels = [scrape1, scrape2, scrape3, scrape4, scrape5, scrape6, scrape7]
    current_date = date.today()
    
    for scraper in channels:
        scraper.find_posts_by_keyword()
        with open(f'{scraper.sub}_subreddit_output.txt', 'a') as file:
            scraper.output_posts_found(file)



    


