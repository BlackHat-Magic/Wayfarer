document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({

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
