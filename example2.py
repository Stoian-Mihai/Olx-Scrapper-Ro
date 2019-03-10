from olx_scrapper import olx_scrap_add
from olx_scrapper import olx_page

first_page_link = 'https://www.olx.ro/oferte/q-gtx-1080/'
olx_p = olx_page(first_page_link)
# Getting  the number of pages
number_of_pages = olx_p.get_pages_number()
print('number of pages = ',number_of_pages)

# Getting of adds for ' number_of_pages' from starting page
ads = olx_p.get_ads_for_x_pages(number_of_pages)

# Printing the number of ads that we found
print('found ', len(ads), 'ads')

# Getting title for all those ads
# You can also get the description/price/features/etc (see example1)

title_list = []
for ad_link in ads:
    olx_ad = olx_scrap_add(ad_link)
    title_list.append(olx_ad.get_title())

print(title_list)