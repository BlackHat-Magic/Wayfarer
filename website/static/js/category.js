document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({

        converter: new showdown.Converter({tables: true}),

        rule(text) {
            return("<div>" + this.converter.makeHtml(text) + "</div>");
        },

        activate (id, text) {
            document.getElementById("rule").innerHTML = this.rule(text);
            tabs = document.getElementsByClassName("tab")
            for(let i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove("active")
            }
            document.getElementById("tab-" + id).classList.add("active");
        },

        addAbility () {
            console.log("added")
        }
    }))
})
