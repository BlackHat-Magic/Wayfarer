document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        prereq: "",
        strasi: 0,
        dexasi: 0,
        conasi: 0,
        intasi: 0,
        wisasi: 0,
        chaasi: 0,
        text: "",

        converter: new showdown.Converter({tables: true}),
        convert(text) {
            return(this.converter.makeHtml(text))
        }
    }))
})
