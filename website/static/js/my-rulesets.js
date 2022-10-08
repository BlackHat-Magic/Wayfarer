document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        show: "display: none",
        rulesetid: 0,

        toggle(id) {
            this.rulesetid = id;
            if (this.show === "display: none") {
                this.show = "display: flex"
            } else {
                this.show = "display: none"
            }
        },

        confirmDelete() {
            fetch("/Remove-Ruleset", {
                method: "POST",
                body: JSON.stringify({
                    rulesetid: this.rulesetid
                }),
            }).then((_res) => {
                window.location.href="/My-Rulesets"
            })
        }
    }))
})

