document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        time: "",
        text: "",
        writeAction (name, time, text) {
            console.log("hello world")
            window.localStorage.setItem(
                "reference",
                JSON.stringify({
                    actions: [
                        {
                            name: name,
                            time: time,
                            text: text
                        }
                    ]
                })
            )
        },
        readAction () {
            cachedAction = JSON.parse(window.localStorage.getItem("reference").actions[0])
            this.name = cachedAction.name
            this.time = cachedAction.time
            this.text = cachedAction.text
        }
    }))
})
