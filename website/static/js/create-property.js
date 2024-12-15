document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        time: "",
        text: "",
        showversatile: false,
        showrange: false,

        compileProperty () {
            property = {
                name: this.name,
                time: this.time,
                text: this.text,
                showversatile: this.showversatile,
                showrange: this.showrange
            }

            return (JSON.stringify (property));
        },
        readProperty () {
            property = JSON.parse (localStorage.getItem ("cached_property"));
            if (property == null) {
                return;
            }

            this.name = property.name,
            this.time = property.time,
            this.text = property.text,
            this.showversatile = property.showversatile,
            this.showrange = property.showrange
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})