document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        initParams () {
            params = new URLSearchParams(window.location.search);
            this.query = params.get("query") || "";
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


        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },

        query: "",

        classROM: [],

        filterQuery() {
            namematch = [];
            for(let i = 0; i < this.classROM.length; i++) {
                if (this.classROM[i].name.includes(this.query)) {
                    namematch.push(this.classROM[i]);
                }
            }
            return(namematch);
        },

        truncate(text) {
            return(text.substring(0, 129) + "...");
        }
    }))
})
