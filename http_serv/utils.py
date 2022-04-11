import os
from pathlib import Path
import base64
from re import T

from pyparsing import html_comment

from http_serv.http_status import HttpStatusCode
from http_serv.http_exceptions import (
    Http404Exception,
    Http500Exception,
    Http405Exception,
)


def identify_resource(public_html, resource):
    """
    Return path to file at specific resource. eg:
    '/index.html' -> public_html/index.html
    '/' -> public_html/index.html
    '/blog' -> public_html/blog/index.html
    '/blog/index.html' -> public_html/blog/index.html
    '/nonexisting' -> raise exception
    """
    # given that resource starts with /
    # os.path.join() won't work properly if elements start/end with /, hence .strip()
    if public_html != "":
        if "." in resource:
            resource_path = os.path.join(public_html, resource.strip("/"))
        else:
            resource_path = os.path.join(public_html, resource.strip("/"), "index.html")

        full_path = os.path.join(os.getcwd(), resource_path)

    else:
        full_path = resource.strip()  # can be together?
        resource_path = resource.strip()

    if os.path.exists(full_path):
        if full_path.endswith(".html"):
            return (resource_path, "text/html")
        elif full_path.endswith(".txt"):
            return (resource_path, "text/plain; charset=utf-8")
        elif full_path.endswith(".css"):
            return (resource_path, "text/css")
        elif full_path.endswith(".json"):
            return (resource_path, "application/json")
        elif full_path.endswith(".png"):
            return (resource_path, "image/png")
        else:
            return (resource_path, "application/octet-stream")

    else:
        raise Http404Exception(resource=resource)


def save_resource(resource_path):
    """
    This method supports only files and requires file's exact path
    """
    file_path = Path(resource_path)  # any need for that? do test

    # no need to check if path exists because it's already checked in identify_resource method
    file_name = os.path.basename(file_path)

    with file_path.open("rb") as i_file:
        with open(f"public_html/added_via_POST/{file_name}", "wb") as new_file:
            new_file.write(i_file.read())

    # it cuts off the sentence - dig into binary pls
    return f"The file {file_name} has been created.".encode()

    # todo:
    # handling duplicates and checking if file already exists


# works
def check_for_index_html(dir_path):

    if "index.html" not in dir_path and "." not in dir_path:
        full_path = os.path.join("public_html", dir_path.strip("/"), "index.html")

        if not os.path.exists(full_path):
            return True
