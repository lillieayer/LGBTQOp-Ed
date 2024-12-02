all_posts_links = extract_links_from_file(dir + '/' + file)
        narrative_insights = []
        # records failed links per narrative
        failed_links = {}
        if "twitter" in file:
            post_type = Tweet
        
        for post_link in all_posts_links:
            # if analyzing fb links must check each for media type
            if 'fb' in file:
                if ('facebook.com/watch' in post_link) or ('fb.watch' in post_link) or ('/videos/' in post_link):
                    post_type = FBVideo
                elif ('facebook.com/reel' in post_link) or ('fb.reel' in post_link):
                    post_type = FBReel
                else:
                    post_type = FBPost

            assert post_type is not None, f"Error when analyzing post type in {post_link}"
            post_insights = find_num_engagements_from_link(driver, post_link, post_type, failed_links)
            # add dictionary of each post info to narrative list
            narrative_insights.append(post_insights)
            # record narratives failed links
        all_failed_links.append(failed_links)
        filename = file.split('.')
        with open('./output/control/' + filename[0] + '_engagements.json', 'w', encoding='utf-8') as engagement_file:
            json.dump(narrative_insights, engagement_file, ensure_ascii=False, indent=4)