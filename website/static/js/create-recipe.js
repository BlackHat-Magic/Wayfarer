document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",
        text: "",

        compileRecipe () {
            recipe = {
                name: this.name,
                text: this.text
            }

            return (JSON.stringify (recipe));
        },
        readRecipe () {
            recipe = JSON.parse (localStorage.getItem ("cached_recipe"));
            if (recipe == null) {
                return;
            }

            this.name = recipe.name;
            this.text = recipe.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})