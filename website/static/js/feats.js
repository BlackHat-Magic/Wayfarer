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

        query: "",
        featROM: [],
        filterQuery() {
            namematch = [];
            for(let i = 0; i < this.featROM.length; i++) {
                if (this.featROM[i].name.includes(this.query)) {
                    namematch.push(this.featROM[i]);
                }
            }

            nameskillmatch = [];
            return(namematch);
        },
        parseasi(asis) {
            output = "";
            for (let i = 0; i < asis.length; i++) {
                if(asis[i] != 0) {
                    if(output.length != 0) {
                        output.append(", " + asis[i]);
                    } else {
                        output.append(asis[i]);
                    }
                }
            }
        },
        truncate(text) {
            return(text.substring(0, 129) + "...");
        }
    }))
})
