document.addEventListener ("alpine:init", () => {
    Alpine.data ("master", () => ({
        // init_selected () {
        //     fetch("/Get-Current-Ruleset", {
        //         method: "GET",
        //         // body: JSON.stringify({
        //         //     local: localStorage.getItem("cruleset")
        //         // })
        //     }).then(function (response) {
        //         return(response.json());
        //     }).then(function (ruleset) {
        //         document.querySelector("#current_ruleset").value = ruleset.id;
        //     });
        // },

        init_selected (rulesetid) {
            document.querySelector("#current_ruleset").value = rulesetid
        },

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

