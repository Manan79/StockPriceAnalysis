import feedparser
import streamlit as st


st.title("Latest News")
# List of RSS feed URLs for news

urls = [
"https://www.moneycontrol.com/rss/markets.xml",
"https://www.business-standard.com/rss/markets-5.rss",
"https://www.livemint.com/rss/markets",

]

for url in urls:
    print(f"Fetching news from: {url}")

    feed = feedparser.parse(url)
    flag = 0
    for entry in feed.entries:

        flag += 1
        col1 , col2 = st.columns(2)
        with col1:

            print(f"News {flag}:")
            st.write(f"**News {flag}:**")
            st.subheader(f"**Title:** {entry.title}")
            # print("Title:", entry.title)
            st.write(f"**Link:** {entry.link}")
            # print("Link:", entry.link)
            st.write (f"**Published:** {entry.published}")
            # print("Published:", entry.published)
            st.write(f"**Summary:** {entry.summary}")
            # print("Summary:", entry.summary)
            # print("Image:" , entry.get('media_thumbnail', [{'url': 'No Image'}])[0]['url'])
        with col2:

            st.image(entry.media_content[0]['url'] if 'media_content' in entry else 'No Image')
        st.write("-----" *20)

        
        
        