document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        time: "",
        text: "",
        endpoint: null,

        compileCondition () {
            action = {
                name: this.name,
                time: this.time,
                text: this.text
            }

            return (JSON.stringify (action));
        },

        readCondition () {
            action = JSON.parse (localStorage.getItem (this.endpoint));
            if (action == null) {
                return;
            }

            this.name = action.name;
            this.time = action.time;
            this.text = action.time;
        }
    }))
})
