document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        text: "",
        base: "None",
        checkBase() {
            if (this.base == "" || this.base == "None") {
                return(true);
            }
            return(false);
        }
    }))
})
