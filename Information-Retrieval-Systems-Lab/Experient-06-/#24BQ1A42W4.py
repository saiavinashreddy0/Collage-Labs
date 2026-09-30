#24BQ1A42W4
#SOLLAPUR SAI AVINASH REDDY


import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
import re
import textwrap


# ============================================================
# WEB CRAWLING / INFORMATION RETRIEVAL SYSTEM
# ============================================================

WEBSITES = {
    "1": ("Wikipedia", "wikipedia.org"),
    "2": ("BBC", "bbc.com"),
    "3": ("CNN", "cnn.com"),
    "4": ("NHK", "nhk.or.jp")
}


# ============================================================
# HTTP HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}


# ============================================================
# 1. CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 2. WIKIPEDIA API SEARCH
# ============================================================

def wikipedia_answer(topic):

    print("\nSearching Wikipedia...")

    try:

        wikipedia_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + quote(
                topic.replace(" ", "_")
            )
        )

        response = requests.get(
            wikipedia_url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:

            return None

        data = response.json()

        title = data.get(
            "title",
            topic
        )

        summary = data.get(
            "extract"
        )

        page_url = (
            data
            .get("content_urls", {})
            .get("desktop", {})
            .get("page")
        )

        if not summary:

            return None

        return {
            "title": title,
            "summary": summary,
            "url": page_url
        }

    except Exception as e:

        print(
            "Wikipedia error:",
            e
        )

        return None


# ============================================================
# 3. DUCKDUCKGO WEB SEARCH
# ============================================================

def web_search(topic, domain):

    query = f"{topic} site:{domain}"

    search_url = (
        "https://html.duckduckgo.com/html/?q="
        + quote(query)
    )

    try:

        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        # DuckDuckGo search results
        for result in soup.select(
            ".result"
        ):

            link_tag = result.select_one(
                ".result__a"
            )

            if not link_tag:
                continue

            title = clean_text(
                link_tag.get_text()
            )

            link = link_tag.get(
                "href"
            )

            if not link:
                continue

            # Handle DuckDuckGo redirect URLs
            if link.startswith("//duckduckgo.com/l/?"):

                parsed_link = urlparse(
                    link
                )

                from urllib.parse import parse_qs

                query_parameters = parse_qs(
                    parsed_link.query
                )

                if "uddg" in query_parameters:

                    link = query_parameters[
                        "uddg"
                    ][0]

            # Only accept actual HTTP URLs
            if not link.startswith(
                "http"
            ):

                continue

            # Check domain
            result_domain = urlparse(
                link
            ).netloc.lower()

            if domain.lower() not in result_domain:

                continue

            results.append(
                {
                    "title": title,
                    "url": link
                }
            )

            if len(results) >= 5:

                break

        return results

    except Exception as e:

        print(
            f"Search error for {domain}: {e}"
        )

        return []


# ============================================================
# 4. EXTRACT TEXT FROM WEB PAGE
# ============================================================

def extract_page_text(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for tag in soup.find_all(
            [
                "script",
                "style",
                "noscript",
                "nav",
                "footer",
                "header",
                "aside",
                "form"
            ]
        ):

            tag.decompose()

        paragraphs = []

        for paragraph in soup.find_all(
            "p"
        ):

            text = clean_text(
                paragraph.get_text(
                    " ",
                    strip=True
                )
            )

            if len(text) >= 40:

                paragraphs.append(
                    text
                )

        # Combine useful paragraphs
        content = " ".join(
            paragraphs[:15]
        )

        return content

    except Exception as e:

        print(
            f"Could not read page: {e}"
        )

        return ""


# ============================================================
# 5. FIND RELEVANT SENTENCES
# ============================================================

def find_relevant_sentences(
    text,
    topic,
    max_sentences=5
):

    if not text:

        return []

    # Split text into sentences
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    # Extract words from topic
    topic_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            topic.lower()
        )
    )

    scored_sentences = []

    for sentence in sentences:

        sentence_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                sentence.lower()
            )
        )

        # Number of topic words appearing
        # in the sentence
        score = len(
            topic_words.intersection(
                sentence_words
            )
        )

        if score > 0:

            scored_sentences.append(
                (
                    score,
                    sentence
                )
            )

    # Highest relevance first
    scored_sentences.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        sentence
        for score, sentence
        in scored_sentences[:max_sentences]
    ]


# ============================================================
# 6. DISPLAY WIKIPEDIA ANSWER
# ============================================================

def display_wikipedia_answer(topic):

    data = wikipedia_answer(
        topic
    )

    if not data:

        print(
            "\nWikipedia information "
            "could not be retrieved."
        )

        return

    print("\n" + "=" * 70)

    print("ANSWER")

    print("=" * 70)

    print(
        f"\nTopic: {data['title']}\n"
    )

    # Display wrapped text
    print(
        textwrap.fill(
            data["summary"],
            width=75
        )
    )

    if data["url"]:

        print(
            f"\nWikipedia: {data['url']}"
        )


# ============================================================
# 7. MAIN PROGRAM
# ============================================================

print("=" * 70)

print(
    "WEB CRAWLING / INFORMATION RETRIEVAL SYSTEM"
)

print("=" * 70)


# ============================================================
# USER QUERY
# ============================================================

topic = input(
    "\nEnter the topic to search: "
).strip()


if not topic:

    print(
        "\nPlease enter a topic."
    )

    exit()


# ============================================================
# WIKIPEDIA ANSWER
# ============================================================

display_wikipedia_answer(
    topic
)


# ============================================================
# WEBSITE SELECTION
# ============================================================

print("\n" + "=" * 70)

print("SELECT WEBSITES")

print("=" * 70)

print(
    "1. Wikipedia"
)

print(
    "2. BBC"
)

print(
    "3. CNN"
)

print(
    "4. NHK"
)

print(
    "5. All Websites"
)


choice = input(
    "\nEnter your choice: "
).strip()


# ============================================================
# DETERMINE SELECTED WEBSITES
# ============================================================

if choice == "5":

    selected_sites = list(
        WEBSITES.values()
    )

elif choice in WEBSITES:

    selected_sites = [
        WEBSITES[choice]
    ]

else:

    print(
        "\nInvalid choice."
    )

    print(
        "Using Wikipedia."
    )

    selected_sites = [
        WEBSITES["1"]
    ]


# ============================================================
# SEARCH RESULTS
# ============================================================

print("\n" + "=" * 70)

print("SEARCH RESULTS")

print("=" * 70)


all_results = []


for site_name, domain in selected_sites:

    # Wikipedia has already been searched
    # using its official API.
    if site_name == "Wikipedia":

        continue


    print(
        f"\n--- {site_name} ({domain}) ---"
    )


    # Search website
    results = web_search(
        topic,
        domain
    )


    if not results:

        print(
            "No search results found."
        )

        continue


    # Process results
    for i, result in enumerate(
        results,
        start=1
    ):

        title = result["title"]

        link = result["url"]


        print(
            f"\n{i}. {title}"
        )

        print(
            f"   URL: {link}"
        )


        # ----------------------------------------------------
        # Crawl the actual webpage
        # ----------------------------------------------------

        print(
            "   Crawling page..."
        )


        page_text = extract_page_text(
            link
        )


        # ----------------------------------------------------
        # Find relevant information
        # ----------------------------------------------------

        relevant_sentences = (
            find_relevant_sentences(
                page_text,
                topic,
                max_sentences=3
            )
        )


        if relevant_sentences:

            print(
                "\n   Relevant Information:"
            )


            for sentence in (
                relevant_sentences
            ):

                wrapped = textwrap.fill(
                    sentence,
                    width=70,
                    initial_indent="   - ",
                    subsequent_indent="     "
                )

                print(
                    wrapped
                )


        else:

            print(
                "   No relevant text extracted."
            )


        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        all_results.append(
            {
                "Website": site_name,
                "Title": title,
                "URL": link,
                "Content": page_text
            }
        )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)

print(
    "CRAWLING COMPLETED"
)

print("=" * 70)


print(
    "Topic searched:",
    topic
)


print(
    "Total results collected:",
    len(all_results)
)


print("=" * 70)

print(
    "Information Retrieval completed successfully."
)

print("=" * 70)