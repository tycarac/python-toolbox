from pathlib import Path
from resources.urlText import UrlText


# _____________________________________________________________________________
def get(filename: str, url: str):
    filepath = Path(Path.cwd(), 'temp', filename).resolve()
    data, is_cached = UrlText.get(filepath, url)
    return data, is_cached


temp_folder = Path(Path.cwd(), 'temp').resolve()
temp_folder.mkdir(exist_ok=True)

get('recommendations.txt', 'https://www.npr.org/proxy/listening/v2/newscast/1/recommendations')
