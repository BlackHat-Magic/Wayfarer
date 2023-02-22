document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        skillselect: "",
        skills: [],

        toolselect: "",
        tools: [],

        langnum: 0,
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
            numlist = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
            langstring = "";
            for (let i = 0; i < this.languages.length; i++) {
                if (i == 0) {
                    langstring += this.languages[i];
                } else {
                    langstring += ", " + this.languages[i];
                }
            }
            if (this.langnum == this.languages.length) {
                result = langstring;
            } else if (this.langnum == 0) {
                result = "none";
            } else if (this.langnum < 10) {
                if (this.langnum.includes("Any")) {
                    result = "Any " + numlist[this.langnum - 1] + " of your choice.";
                } else {
                    result = "Any " + numlist[this.langnum - 1] + " of your choice from: " + langstring;
                }
            } else {
                if (this.langnum.includes("Any")) {
                    result = "Any " + this.langnum + " of your choice.";
                } else {
                    result = "Any " + this.langnum + " of your choice from: " + langstring;
                }
            }
            return(result);
        },
        appendLanguage() {
            if (this.languageselect == "Any") {
                this.languages = ["Any"];
            } else if (this.languages[0] == "Any") {
                this.languages = [this.languageselect];
            } else if (!(this.languages.includes(this.languageselect) || this.languageselect == "select")) {
                this.languages.push(this.languageselect);
            }
        },
        removeLanguage(index) {
            newLanguages = [];
            for (let i = 0; i < this.languages.length; i++) {
                if (i != index) {
                    newLanguages.push(this.languages[i]);
                }
            }
            this.languages = newLanguages;
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
