document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        show: "display: none",

        toggle() {
            if (this.show === "display: none") {
                this.show = "display: flex"
            } else {
                this.show = "display: none"
            }
        },

        confirmDelete(id) {
            fetch("/Delete-Ruleset", {
                method: "POST",
                body: JSON.stringify({
                    rulesetid: id
                }),
            }).then((_res) => {
                window.location.href="/My-Rulesets"
            })
        }
    }))
})
