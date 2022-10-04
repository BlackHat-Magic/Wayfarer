document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        text: "",

        converter: new showdown.Converter(),

        convert() {
            return(this.converter.makeHtml(this.text))
        }
    }))
})
