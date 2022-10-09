document.addEventListener ("alpine:init", () => {
    Alpine.data ("master", () => ({
        init_selected () {
            fetch("/Get-Current-Ruleset")
                .then(function (response) {
                    return(response.json());
                }).then(function (ruleset) {
                    document.querySelector("#current_ruleset").value = ruleset.id;
                });
        },

        changeRuleset() {
            fetch("/Change-Ruleset", {
                method: "POST",
                body: JSON.stringify({
                    rulesetid: document.querySelector("#current_ruleset").value
                }),
            }).then(function(){
                window.location.reload();
            })
        }
    }))
})

