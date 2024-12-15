document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        time: "",
        text: "",

        compileAction () {
            action = {
                name: this.name,
                time: this.time,
                text: this.text
            };

            return (JSON.stringify (action));
        },
        readAction () {
            action = JSON.parse(window.localStorage.getItem("cached_action"))
            if (action == null) { 
                return;
            }

            this.name = action.name;
            this.time = action.time;
            this.text = action.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})