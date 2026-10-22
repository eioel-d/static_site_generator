from textnode import TextNode, TextType
from copy_contents import copy_contents
from generate_page import generate_page

print("hello world")


def create_text_node(text, text_type, url):
    text_node = TextNode(text, text_type, url)
    print(text_node)


create_text_node("This is some anchor text", TextType.LINK, "www.google.com")

copy_contents(
    "./static",
    "./public",
)

generate_page("./content/", "./template.html", "./public/")
