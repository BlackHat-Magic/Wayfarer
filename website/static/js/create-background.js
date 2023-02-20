document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        skillselect: "",
        skills: [],

        toolselect: "",
        tools: [],

        langnum: null,
        languageselect: "",
        languages: [],

        itemselect: "",
        items: [],

        equipment: "",
        text: "",
        features: [
            {
                name: "",
                text: ""
            }
        ],
        toolROM: [],
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

        parseTools() {
            result = "";
            for (let i = 0; i < this.tools.length; i++) {
                if(result.length < 1) {
                    result += this.tools[i];
                } else {
                    result += ", " + this.tools[i];
                }
            }
            result = "<strong>Tool Proficiencies: </strong> " + result;
            return(result);
        },
        appendTool() {
            if(!(this.tools.includes(this.toolselect) || this.toolselect == "select")) {
                this.tools.push(this.toolselect);
            }
        },
        removeTool(index) {
            newTools = [];
            for (let i = 0; i < this.tools.length; i++) {
                if (i != index) {
                    newTools.push(this.tools[i]);
                }
            }
            this.tools = newTools;
        },

        parseLanguages() {
            result = "";
            if(this.languages[0] == "Any") {
                result = "<strong>Languages: </strong>";
            }
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
    }))
})
