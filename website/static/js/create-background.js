document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        skillselect: "",
        skills: [],
        tools: "",
        languages: "",
        equipment: "",
        text: "",
        features: [
            {
                name: "",
                text: ""
            }
        ],
        parseSkills() {
            result = "";
            for (let i = 0; i < this.skills.length; i++) {
                if(result.length < 1) {
                    result += this.skills[i];
                } else {
                    result += ", " + this.skills[i];
                }
            }
            result = "<strong>Skill Proficiencies: </strong> " + result;
            return(result)
        },
        appendSkill() {
            if(!(this.skills.includes(this.skillselect) || this.skillselect == "select")) {
                this.skills.push(this.skillselect);
            }
        },
        removeSkill(index) {
            newSkills = [];
            for (let i = 0; i < this.skills.length; i++) {
                if(i != index) {
                    newSkills.append(this.skills[i]);
                }
            }
            this.skills = newSkills;
        },
        
        addFeature() {
            this.features.push({
                name: "",
                text: ""
            })
        },
        deleteFeature(index) {
            output = [];
            for (let i = 0; i < this.features.length; i++) {
                if(i != index) {
                    output.push(this.features[i]);
                }
            }
            this.features = output;
        },

        converter: new showdown.Converter({tables: true}),
        convert(text) {
            return(this.converter.makeHtml(text))
        },
        submit() {
            fname = this.name;
            skills = this.skills;
            tools = this.tools;
            lang = document.querySelector("#languages").value; //for some reason this gets set to null if I try to define it using the variable, so document.querySelector it is.
            equipment = this.equipment;
            text = this.text;
            features = this.features;
            fetch ("/Character/Backgrounds/Create", {
                method: "POST",
                body: JSON.stringify({
                    name: fname,
                    skills: skills,
                    tools: tools,
                    equipment: equipment,
                    text: text,
                    features: features,
                    lang: lang
                })
            }).then (function (response) {
                return(response.json());
            }).then(function (result) {
                if(result == 0) {
                    window.location.href="/Character/Backgrounds";
                } else {
                    window.location.reload();
                }
            })
        },
    }))
})
