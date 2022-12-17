document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        time: "",
        text: ""
    }))
})
