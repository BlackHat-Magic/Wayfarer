def parseEntries(entries, depth):
    text = ""
    for entry in entries:
        if(type(entry) == str):
            text += entry
        elif(type(entry) == dict and entry["type"] == "list"):
            for item in entry["items"]:
                text += f" - {item}\n"
            text += "\n"
        elif(type(entry) == dict and entry["type"] == "table"):
            if("caption" in entry.keys()):
                text += f"##### {entry['caption']}\n\n"
            text += convertTable(entry)
        elif(type(entry) == dict and entry["type"] == "inset"):
            for paragraph in entry["entries"]:
                text += f"> {paragraph}\n"
            text += "\n"
        elif(type(entry) == dict and entry["type"] == "entries"):
            if("name" in entry.keys())
                for i in range(depth):
                    text += "#"
                text += f" {entry['name']}\n\n"
            text += parseEntries(entry["entries"])
        else:
            flash("Unrecognized entry type; skipping...", "orange")
    return(text)