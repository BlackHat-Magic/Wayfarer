document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({

        converter: new showdown.Converter(),

        rule(text) {
            return(this.converter.makeHtml(text))
        }
    }))
})
