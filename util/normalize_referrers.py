big_referrers = (
            ('google.', 'Google'),
            ('bing.com', 'Bing'),
            ('twitter.com', 'Twitter'),
            ('t.com', 'Twitter'),
            ('reddit.com', 'Reddit'),
            ('duckduckgo.com', 'DuckDuckGo')
        )


def normalize_referrer(referrer_url):
    for big_ref in big_referrers:
        if big_ref[0] in referrer_url:
            return big_ref[1]

    return referrer_url
