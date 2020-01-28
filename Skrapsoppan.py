from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# opens the connection and downloads html page from url
uClient = uReq("https://www.amazon.com/Cards-Against-Humanity-LLC-CAHUS/dp/B004S8F7QM/ref=sxin_0_osp48-65351ba5_cov?ascsubtag=65351ba5-a53b-4f39-bc09-fd8b9f6bb349&creativeASIN=B004S8F7QM&cv_ct_cx=game&cv_ct_id=amzn1.osp.65351ba5-a53b-4f39-bc09-fd8b9f6bb349&cv_ct_pg=search&cv_ct_wn=osp-search&keywords=game&linkCode=oas&pd_rd_i=B004S8F7QM&pd_rd_r=9f8df896-a81f-4959-855f-771845f6ae24&pd_rd_w=1mMMs&pd_rd_wg=vyH9a&pf_rd_p=62c00474-6fe0-420f-9956-a05256e04b43&pf_rd_r=PBSXE3PCE1G1BX6MZC19&qid=1580207572&sr=1-1-32a32192-7547-4d9b-b4f8-fe31bfe05040&tag=spyonsite-20")

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "item-container"})

# name the output file to write to local disk
out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "brand,product_name,shipping \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about
# each product
for container in containers:
    # Finds all link tags "a" from within the first div.
    make_rating_sp = container.div.select("a")

    # Grabs the title from the image title attribute
    # Then does proper casing using .title()
    brand = make_rating_sp[0].img["title"].title()

    # Grabs the text within the second "(a)" tag from within
    # the list of queries.
    product_name = container.div.select("a")[2].text

    # Grabs the product shipping information by searching
    # all lists with the class "price-ship".
    # Then cleans the text of white space with strip()
    # Cleans the strip of "Shipping $" if it exists to just get number
    shipping = container.findAll("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")

    # prints the dataset to console
    print("brand: " + brand + "\n")
    print("product_name: " + product_name + "\n")
    print("shipping: " + shipping + "\n")

    # writes the dataset to file
    f.write(brand + ", " + product_name.replace(",", "|") + ", " + shipping + "\n")

f.close()  # Close the file
