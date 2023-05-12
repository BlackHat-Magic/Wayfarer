document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        ability: "",
        text: "",
        abilitydict: {
        },

        converter: new showdown.Converter({tables: true}),

        convert (text) {
            return(this.converter.makeHtml(text))
        },

    }))
})
