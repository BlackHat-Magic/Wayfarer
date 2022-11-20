document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        ability: "",
        text: "",
        abilitydict: {
            "STR": "Strength",
            "DEX": "Dexterity",
            "CON": "Constitution",
            "INT": "Intelligence",
            "WIS": "Wisdom",
            "CHA": "Charisma",
            "": "N/A"
        },

        converter: new showdown.Converter({tables: true}),

        convert (text) {
            return(this.converter.makeHtml(text))
        },

    }))
})
