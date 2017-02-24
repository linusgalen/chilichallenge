from app import app, db
from app.models import Product

product_list=[
    {
        'name': 'Svag Röd Chili',
        'description': 'Den har chilin kommer ifran den morkaste djungeln och har plockats med karlek. Perfekt för nyborjaren',
        'imgurl':'http://www.publicdomainpictures.net/pictures/10000/velka/1-1248162429KMBk.jpg',
        'price' : 59
    },
    {
        'name': 'Chili el medio',
        'description': 'Den har chilin kommer ifran har plockats med karlek och kommer ge en stabil hetta i munnen',
        'imgurl': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Red_Pepper_-_on_white.jpg',
        'price': 69
    },
    {
        'name': 'Chili el diablo',
        'description': 'Detta ar inget för veklingar. Chili el diablo kommer ifran El salvador och odlas av blinda munkar vilket gor den valdiigt exklusiv men ack sa stark!',
        'imgurl': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Habanero_peper.jpg',
        'price': 199
    }
]



for product in product_list:

    new_product = Product(
        name=product["name"],
        imgurl=product["imgurl"],
        description=product["description"],
        price=product["price"]
    )
    db.session.add(new_product)

db.session.commit()
print("Done!")
