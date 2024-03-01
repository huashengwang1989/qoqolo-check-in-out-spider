from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
def add_query_params(url: str, params):
    parsed_url = urlparse(url)
    query_params = dict(parse_qsl(parsed_url.query))
    query_params.update(params)
    
    new_query = urlencode(query_params)
    
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))
    
    return new_url

def get_hostname_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname
