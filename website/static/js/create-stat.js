document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        abbr: "",
        numb: "",
        text: "",
        order: null,

        compileStat () {
            stat = {
                name: this.name,
                abbr: this.abbr,
                numb: this.numb,
                text: this.text,
                order: this.order
            };

            return (JSON.stringify (stat));
        },

        readStat () {
            stat = JSON.parse(localStorage.getItem("cached_stat"));
            if (stat == null) {
                return;
            }

            this.name = stat.name;
            this.abbr = stat.abbr;
            this.numb = stat.numb;
            this.text = stat.text;
            this.order = stat.order;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})