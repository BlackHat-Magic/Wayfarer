document.addEventListener ("alpine:init", () => {
    Alpine.data ("master", () => ({
        selected: "",

        init_selected () {
            this.selected = fetch("/Get-Current-Ruleset");
            console.log(this.selected);
        },
        test(){
            // alert(this.selected);
            console.log(this.selected);    
        },

        changeRuleset() {
            alert("Hello" + this.selected)
            fetch("/Change-Ruleset", {
                method: "POST",
                body: JSON.stringify({
                    rulesetid: 2
                }),
            }).then((_res) => {
                window.location.href="";
            })
        }
    }))
})

