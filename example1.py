from olx_scrapper import olx_scrap_add

#olx_link = name = input("Enter olx link: \n")
olx_link = 'https://www.olx.ro/oferta/placa-video-asus-gtx-1080-IDbWtV3.html#b22c96c23c'
olx = olx_scrap_add(olx_link)
print('title: ' , olx.get_title())
print('-----')
print('description: ', olx.get_description())
print('-----')
print('price:', olx.get_price())
print('-----')
print('features:', olx.get_features())
print('-----')
print('city:', olx.get_city())
print('-----')
print('images:', olx.get_images())
print('-----')
print('date, time:', olx.get_date_time())
print('-----')
print('add number:', olx.get_add_number())
# an alternate approach is to use .get_all()
# method that returns a dictionary with all the information about an add
print(olx.get_all())