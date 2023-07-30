document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        initParams () {
            params = new URLSearchParams(window.location.search);
            this.query = params.get("query") || "";
            this.taglist = params.get("tags").split(",");
            this.filtertype = params.get("filtertype") || "AND";
        },

        updateQuery() {
            params = new URLSearchParams(window.location.search);
            if (this.query != null && this.query != "") {
                params.set("query", this.query);
            } else {
                params.delete("query")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },

        updateTags() {
            params = new URLSearchParams(window.location.search);
            if (this.taglist != null && this.taglist.length > 0) {
                params.set("tags", this.taglist.toString());
            } else {
                params.delete("tags")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },

        updateFilter () {
            params = new URLSearchParams(window.location.search);
            params.set("filtertype", this.filtertype)
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
        itemROM: [],

        query: "",
        filtertype: "AND",
        filterQuery() {
            match = [];
            for(let i = 0; i < this.itemROM.length; i++) {
                if (this.itemROM[i].name.includes(this.query)) {
                    match.push(this.itemROM[i]);
                }
            }

            console.log(this.filtertype)

            if(this.filtertype == "AND") {
                for (let i = match.length - 1; i >= 0; i--) {
                    for (let j = 0; j < this.taglist.length; j++) {
                        if(!match[i].type.includes(this.taglist[j])) {
                            match.splice(i, 1);
                            break;
                        }
                    }
                }
            } else {
                newmatch = []
                console.log("or")
                for (let i = 0; i < match.length; i++) {
                    for (let j = 0; j < this.taglist.length; j++) {
                        console.log(match[i].type + "; " + this.taglist[j])
                        if(match[i].type.includes(this.taglist[j])) {
                            newmatch.push(match[i]);
                            break;
                        }
                    }
                }
                match = newmatch
            }
            return(match);
        },

        filterTags() {
            console.log("unfinished")
        },

        tags: "",
        taglist: [],
        appendTag() {
            if(!(this.taglist.includes(document.querySelector("#tags").value))){
                this.taglist.push(document.querySelector("#tags").value);
            }
            this.updateTags()
        },
        removeTag(index) {
            output = [];
            for (let i = this.taglist.length -1; i >=0; i--) {
                if(i != index) {
                    output.push(this.taglist[i]);
                }
            }
            newoutput = [];
            for (let i = output.length - 1; i >= 0; i--) {
                newoutput.push(output[i])
            }
            this.taglist = newoutput;
            this.updateTags()
        },
    }))
})
