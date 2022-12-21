document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        dicelist: [
            "d4",
            "d6",
            "d8",
            "d10",
            "d12",
            "d20"
        ],

        name: "",
        
        hitdie: 0,

        gold_nums: null,
        gold_dice: 0,
        gold_mult: null,

        str: false,
        dex: false,
        con: false,
        int: false,
        wis: false,
        cha: false,

        proficiencyselect: null,
        proficiencylist: [],
        proficiencies: null,
        appendProficiency () {
            if(!this.proficiencylisst.includes(document.querySelector("#proficiencyselect").value)) {
                this.proficiencylisst.push(document.querySelector("#proficiencyselect").value);
            }
            this.updateProficiencies();
        },
        removeProficiency(index) {
            output = [];
            for (let i = this.proficiencylist.length - 1; i >= 0; i--) {
                if(index != i) {
                    output.push(this.proficiencylist[i]);
                }
            }
            newoutput = [];
            for (let i = 0; i < output.length; i++) {
                newoutput.push(output[i]);
            }
            this.updateProficiencies;
            this.proficiencylist = newoutput;
        },
        updateProficiencies () {
            output = "";
            for (let i = 0; i < this.proficiencylist.length; i++) {
                if(output.length == 0) {
                    output += this.proficiencylist[i];
                } else {
                    output += ", ${this.proficiencylist[i]}";
                }
            }
        },

        skillselect: null,
        skilllist: [],
        skills: null,
        appendSkill () {
            if(!this.skilllist.includes(document.querySelector("#skillselect").value)) {
                this.skilllist.push(document.querySelector("#skillselect").value);
            }
            this.updateSkills();
        },
        removeSkill(index) {
            output = [];
            for (let i = this.skilllist.length -1; i >= 0; i--) {
                if(index != i) {
                    output.push(this.skilllist[i]);
                }
            }
            newoutput = [];
            for (let i = 0; i < newoutput.length; i++) {
                newoutput.push(output[i]);
            }
            this.updateProficiencies;
            this.skillist = newoutput;
        },
        updateSkills () {
            output = "";
            for (let i = 0; i < this.skilllist.length; i++) {
                if(output.length == 0) {
                    output += this.skilllist[i];
                } else {
                    output += ", ${this.skillist[i]}"
                }
            }
        },

        equipment: "",

        prereq: "",

        subclassname: "",

        text: "",

        features: [
            {
                name: "",
                level: null,
                text: ""
            }
        ],

        subclasses: [
            {
                name: "",
                text: "",
                features: [
                    {
                        name: "",
                        level: null,
                        text: ""
                    }
                ]
            }
        ]
    }))
})
