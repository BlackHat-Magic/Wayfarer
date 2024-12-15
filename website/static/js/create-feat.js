document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        prereq: "",
        asis: {},
        text: "",

        converter: new showdown.Converter({tables: true}),
        convert(text) {
            return(this.converter.makeHtml(text))
        },

        compileFeat () {
            feat = {
                name: this.name,
                prereq: this.prereq,
                asis: this.asis,
                text: this.text
            };
            
            return (JSON.stringify (feat));
        },

        loadFeat () {
            feat = JSON.parse (localStorage.getItem ("cached_feat"));
            if (feat == null) {
                return;
            }

            this.name = feat.name;
            this.prereq = feat.prereq;
            this.asis = feat.asis;
            this.text = feat.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})