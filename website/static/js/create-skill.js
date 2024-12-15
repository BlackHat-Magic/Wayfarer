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

        compileSkill () {
            skill = {
                name: this.name,
                ability: this.ability,
                text: this.text,
                abilitydict: this.abilitydict
            }

            return (JSON.stringify (skill));
        },
        readSkill () {
            skill = JSON.parse (localStorage.getItem ("cached_skill"));
            if (skill == null) {
                return;
            }

            this.name = skill.name;
            this.ability = skill.ability;
            this.text = skill.text;
            this.abilitydict = skill.abilitydict;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})