document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        text: "",

        compileLanguage () {
            language = {
                name: this.name,
                text: this.text
            }

            return (JSON.stringify (language))
        },

        readLanguage () {
            language = JSON.parse (localStorage.getItem ("cached_language"));
            if (language == null) {
                return;
            }

            this.name = language.name;
            this.text = language.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})