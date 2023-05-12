from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import current_user

def convertTable(table):
    text = ""
    for label in table["colLabels"]:
        text += f"| {label} "
    text += "|\n"
    for style in table["colStyles"]:
        text += "| "
        if("center" in style.casefold() or "left" in style.casefold()):
            text += ":"
        text += "---"
        if("center" in style.casefold() or "right" in style.casefold()):
            text += ":"
        text += " "
    text += "|\n"
    for row in table["rows"]:
        for datum in row:
            text += f"| {datum}"
        text += "|\n"
    return(text)

def parseEntries(entries, depth, name):
    text = ""
    if(depth > 6):
        depth = 6
    for entry in entries:
        if(type(entry) == str):
            text += f"{entry}\n"
        elif(type(entry) == dict and entry["type"] == "list"):
            for item in entry["items"]:
                text += " - "
                if(type(item) == str):
                    text += f"{item}\n"
                else:
                    if("name" in item.keys()):
                        text += f"***{item['name']}***"
                    if("entry" in item.keys()):
                        text += f"{item['entry']}\n"
                    elif("entries" in item.keys()):
                        text += f"{item['entries'][0]}\n"
                    elif("type" in item.keys() and item["type"] == "list"):
                        text += "sublist\n"
                        for sitem in item["items"]:
                            text += f"     - {sitem}\n"
            text += "\n"
        elif(type(entry) == dict and entry["type"] == "table"):
            if("caption" in entry.keys()):
                text += f"###### {entry['caption']}\n\n"
            text += convertTable(entry)
        elif(type(entry) == dict and (entry["type"] == "inset" or entry["type"] == "quote" or entry["type"] == "insetReadaloud")):
            if("name" in entry.keys()):
                text += f"> ###### {entry['name']}\n\n"
            for paragraph in entry["entries"]:
                if(type(paragraph) == str):
                    text += f"> {paragraph}\n"
                elif("name" in paragraph.keys()):
                    text += f"> ***{paragraph['name']}.*** {paragraph['entries'][0]}\n"
                elif("type" in paragraph.keys() and paragraph["type"] == "list"):
                    for item in paragraph["items"]:
                        text += f"> - {item}\n"
                else:
                    text += f"> {paragraph['entries'][0]}\n"
                text += "\n"
        elif(type(entry) == dict and (entry["type"] == "entries" or entry["type"] == "section")):
            if("name" in entry.keys()):
                for i in range(depth):
                    text += "#"
                text += f" {entry['name']}\n\n"
            text += parseEntries(entry["entries"], depth + 1, name)
        else:
            flash(f"Unrecognized entry type in {name}; skipping...", "orange")
        text += "\n"
    return(text)
