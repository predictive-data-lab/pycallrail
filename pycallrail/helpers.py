from urllib.parse import urljoin
import typing
def build_url(base_url: str, endpoint: str, path: typing.Optional[str] = None ) -> str:
    
    url_result: str = urljoin(base_url, endpoint)

    if path:
        # Ensure the endpoint has a trailing slash
        if not url_result.endswith('/'):
            url_result += '/'

        # Ensure the path doesn't have a leading slash
        if path.startswith('/'):
            path = path[1:]

        url_result: str = urljoin(url_result, path) # type: ignore

    return url_result