document.addEventListener ("alpine:init", () => {
    Alpine.data ("master", () => ({
        init_selected (rulesetid) {
            document.querySelector("#current_ruleset").value = rulesetid;
        },

        flashes: [],

        changeRuleset() {
            localStorage.setItem("cruleset", document.querySelector("#current_ruleset").value)
            console.log(localStorage.getItem("cruleset"))
            fetch("/Change-Ruleset", {
                method: "POST",
                body: JSON.stringify({
                    rulesetid: document.querySelector("#current_ruleset").value
                }),
            }).then(function () {
                window.location.reload();
            })
        }
    }))
})

