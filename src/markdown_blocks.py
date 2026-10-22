from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered"
    OLIST = "ordered"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "######")):
        return BlockType.HEADING

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}."):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = None
        if block_to_block_type(block) == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.TEXT)
            html_node = ParentNode("code", [text_node_to_html_node(text_node)])
            block_nodes.append(ParentNode("pre", [html_node]))

        elif block_to_block_type(block) == BlockType.HEADING:
            child_nodes = text_to_children(block.lstrip("# "))
            if block.startswith("# "):
                html_node = ParentNode("h1", child_nodes)
            elif block.startswith("## "):
                html_node = ParentNode("h2", child_nodes)
            elif block.startswith("### "):
                html_node = ParentNode("h3", child_nodes)
            elif block.startswith("#### "):
                html_node = ParentNode("h4", child_nodes)
            elif block.startswith("##### "):
                html_node = ParentNode("h5", child_nodes)
            elif block.startswith("###### "):
                html_node = ParentNode("h6", child_nodes)
            block_nodes.append(html_node)

        elif block_to_block_type(block) == BlockType.PARAGRAPH:
            lines = block.split("\n")
            lines = " ".join(lines)
            child_nodes = text_to_children(lines)
            html_node = ParentNode("p", child_nodes)
            block_nodes.append(html_node)

        elif block_to_block_type(block) == BlockType.QUOTE:
            quotes = block.split("\n")
            new_quotes = []
            for quote in quotes:
                new_quotes.append(quote.lstrip("> "))
            quotes = " ".join(new_quotes)
            child_nodes = text_to_children(quotes)
            html_node = ParentNode("blockquote", child_nodes)
            block_nodes.append(html_node)

        elif block_to_block_type(block) == BlockType.ULIST:
            lists = block.split("\n")
            child_nodes = []
            for list in lists:
                child_nodes.append(
                    ParentNode("li", text_to_children(list.lstrip("- ")))
                )
            html_node = ParentNode("ul", child_nodes)
            block_nodes.append(html_node)

        elif block_to_block_type(block) == BlockType.OLIST:
            lists = block.split("\n")
            child_nodes = []
            i = 1
            for list in lists:
                child_nodes.append(
                    ParentNode("li", text_to_children(list.removeprefix(f"{i}. ")))
                )
                i += 1
            html_node = ParentNode("ol", child_nodes)
            block_nodes.append(html_node)
    parent_node = ParentNode("div", block_nodes)
    return parent_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("There is no 'h1' header")
