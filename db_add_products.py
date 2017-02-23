from app import app, db
from app.models import Product

product_list=[
    {
        'name': 'Svag Röd Chili',
        'description': 'Den här chilin kommer ifrån den mörkaste djungeln och har plockats med kärlek. Perfekt för nybörjaren',
        'imgurl':'http://www.publicdomainpictures.net/pictures/10000/velka/1-1248162429KMBk.jpg',
        'price' : 59
    },
    {
        'name': 'Chili el medio',
        'description': 'Den här chilin kommer ifrån har plockats med kärlek och kommer ge en stabil hetta i munnen',
        'imgurl': 'https://cdn.pixabay.com/photo/2015/02/06/01/16/pepper-625626_960_720.jpg',
        'price': 69
    },
    {
        'name': 'Chili el diablo',
        'description': 'Detta är inget för veklingar. Chili el diablo kommer ifrån El salvador och odlas av blinda munkar vilket gör den väldiigt exklusiv men ack så stark!',
        'imgurl': 'https://cdn.pixabay.com/photo/2015/02/06/01/16/pepper-625626_960_720.jpg',
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
