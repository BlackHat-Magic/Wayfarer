document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({

        converter: new showdown.Converter({tables: true}),

        query: "",
    }))
})
