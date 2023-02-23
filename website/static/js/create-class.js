document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",

        hitdie: 0,
        dicelist: [
            "d4",
            "d6",
            "d8",
            "d10",
            "d12",
            "d20"
        ],
        fhplist: [
            4,
            6,
            8,
            10,
            12,
            20
        ],

        gold_nums: null,
        gold_dice: 0,
        gold_mult: null,

        save: {},

        proficiencyselect: null,
        proficiencylist: [],
        appendProficiency () {
            if(!this.proficiencylist.includes(document.querySelector("#proficiencyselect").value)) {
                this.proficiencylist.push(document.querySelector("#proficiencyselect").value);
            }
        },
        removeProficiency(index) {
            output = [];
            for (let i = 0; i < this.proficiencylist.length; i++) {
                if(index != i) {
                    output.push(this.proficiencylist[i]);
                }
            }
            this.proficiencylist = output;
        },

        skillselect: null,
        skilllist: [],
        appendSkill () {
            if(!this.skilllist.includes(document.querySelector("#skillselect").value)) {
                this.skilllist.push(document.querySelector("#skillselect").value);
            }
        },
        removeSkill(index) {
            output = [];
            for (let i = 0; i < this.skilllist.length; i++) {
                if(index != i) {
                    output.push(this.skilllist[i]);
                }
            }
            this.skilllist = output;
        },

        parseList (list) {
            output = "";
            for (let i = 0; i < list.length; i++) {
                if(output.length == 0) {
                    output += list[i];
                } else {
                    output += ", " + list[i];
                }
            }
            return(output);
        },
        parseSaves () {
            output = "";
            for (const [key, value] of Object.entries(this.save)) {
                if (value) {
                    if (output.length == 0) {
                        output += key;
                    } else {
                        output += ", " + key;
                    }
                }
            }
            return(output);
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
