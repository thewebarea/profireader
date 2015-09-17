from config import Config
import math

def pagination(query, page_size, page=1, items_per_page=Config.ITEMS_PER_PAGE):

        pages = math.ceil(query.count()/items_per_page)
        page -= 1
        if page_size:
            query = query.limit(page_size)
        if page:
            query = query.offset(page*page_size) if int(page) in range(
                0, int(pages)) else query.offset(pages*page_size)
        return query, pages, page+1
