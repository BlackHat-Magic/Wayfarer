document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        selected: fetch("/Get-Current-Ruleset", {
            method: "POST",
        }),

    }))
})

