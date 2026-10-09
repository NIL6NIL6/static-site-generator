import os
import shutil

from src.textnode import TextNode, TextType


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


def main():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(project_dir, "static")
    public_dir = os.path.join(project_dir, "public")
    copy_dir(static_dir, public_dir)
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(text_node)


if __name__ == "__main__":
    main()
