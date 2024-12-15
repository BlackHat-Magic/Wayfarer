document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        text: "",

        compileTag () {
            tag = {
                name: this.name,
                text: this.text
            }

            return (JSON.stringify (tag));
        },
        readTag () {
            tag = localStorage.getItem("cached_tag");
            if(tag == null) {
                return;
            }

            this.name = tag.name;
            this.text = tag.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})