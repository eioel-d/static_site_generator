import os
from markdown_blocks import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path, base_path):

    paths = os.listdir(from_path)
    for path in paths:
        if os.path.isfile(os.path.join(from_path, path)):
            print(
                f"Generating page from {os.path.join(from_path, path)} to {os.path.join(dest_path)}/index.html using {template_path}"
            )
            with open(os.path.join(from_path, path), "r") as file:
                content = file.read()

            html_node = markdown_to_html_node(content)
            html = html_node.to_html()
            title = extract_title(content)

            with open(os.path.abspath(template_path), "r") as file:
                template = file.read()
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace('href="/', f'href="{base_path}')
            template = template.replace('src="/', f'src="{base_path}')
            os.makedirs(os.path.dirname(os.path.join(dest_path, path)), exist_ok=True)

            with open(os.path.join(dest_path, "index.html"), "w") as file:
                file.write(template)

        else:
            generate_page(
                os.path.join(from_path, path),
                template_path,
                os.path.join(dest_path, path),
                base_path,
            )
