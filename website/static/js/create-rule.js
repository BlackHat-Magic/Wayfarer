document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        text: "",
        category: "",

        converter: new showdown.Converter({tables: true}),

        convert() {
            return(this.converter.makeHtml(this.text))
        },

        compileRule () {
            rule = {
                name: this.name,
                text: this.text,
                category: this.category
            }

            return (JSON.stringify (rule));
        },
        readRule () {
            rule = JSON.parse (localStorage.getItem ("cached_rule"));
            if (rule == null) {
                return;
            }

            this.text = rule.text;
            this.name = rule.name;
            this.category = rule.category;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})