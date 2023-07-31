document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },

        InitHeaderIDs () {
            headers = document.querySelector("#flavor").querySelectorAll("h1, h2, h3, h4, h5, h6") + document.querySelector("#subrace-flavor").querySelectorAll("h1, h2, h3, h4, h5, h6");

            for (let i = 0; i < headers.length; i++) {
                header = headers[i]
                header.innerHTML += ` <span class="anchor">🔗</span>`
                id = header.textContent.replace(/\s+/g, "-").toLowerCase()
                while (document.querySelectorAll(`#${id}`).length > 0) {
                    id += "-";
                }
                header.id = id
                new_html = `<a @click="CopyHash('${id}')">${header.innerHTML}</a>`
            }

            for (let i = 0; i < headers.length; i++) {
                header = headers[i];
                header.innerHTML
            }
        },
        CopyHash (id) {
            window.location.hash = id;
            url_with_hash = window.location.href;
            navigator.clipboard.writeText(url_with_text);
        }
    }))
})