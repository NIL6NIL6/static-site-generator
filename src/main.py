import os
import shutil

from src.markdown_helpers import extract_title
from src.md_to_html import markdown_to_html_node


def copy_dir(src: str, dest: str) -> None:
    # If the destination exists, remove it first to ensure a clean copy.
    if os.path.exists(dest):
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        else:
            os.remove(dest)
    os.mkdir(dest)
    # Copy the contents of the source directory to the destination.
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            print("Copying directory:", s, "to", d)
            copy_dir(s, d)
        else:
            print("Copying file:", s, "to", d)
            shutil.copy(s, d)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )
    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()

    html_contents = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)

    page_contents = template_contents.replace("{{ Title }}", title)
    page_contents = page_contents.replace("{{ Content }}", html_contents)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page_contents)


def generate_pages(from_path: str, template_path: str, dest_path: str) -> None:
    for item in os.listdir(from_path):
        s = os.path.join(from_path, item)
        if os.path.isfile(s) and s.endswith(".md"):
            d = os.path.join(dest_path, os.path.splitext(item)[0] + ".html")
            generate_page(s, template_path, d)
        elif os.path.isdir(s):
            d = os.path.join(dest_path, item)
            generate_pages(s, template_path, d)


def main():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(project_dir, "static")
    public_dir = os.path.join(project_dir, "public")
    copy_dir(static_dir, public_dir)
    generate_pages(
        from_path=os.path.join(project_dir, "content"),
        template_path=os.path.join(project_dir, "template.html"),
        dest_path=public_dir,
    )


if __name__ == "__main__":
    main()
