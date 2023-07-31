document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },

        CopyHash (id) {
            window.location.hash = id;
            url_with_hash = window.location.href;
            navigator.clipboard.writeText(url_with_text);
        }
    }))
})