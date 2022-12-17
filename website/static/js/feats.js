document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
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
            return(text.substring(0, 129));
        }
    }))
})
