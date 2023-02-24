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

        levels: 20,

        save: {},

        proficiencyselect: null,
        proficiencylist: [],
        appendProficiency () {
            if(!this.proficiencylist.includes(this.proficiencyselect)) {
                this.proficiencylist.push(this.proficiencyselect);
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

        multiproficselect: null,
        multiproficlist: [],
        appendMultiProfic () {
            if(!this.multiproficlist.includes(this.multiproficselect)) {
                this.multiproficlist.push(this.multiproficselect);
            }
        },
        removeMultiProfic(index) {
            output = [];
            for (let i = 0; i < this.multiproficlist.length; i++) {
                if(index != i) {
                    output.push(this.multiproficlist[i]);
                }
            }
            this.multiproficlist = output;
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
                text: "",
                is_subclass: false
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
                        text: "",
                        is_subclass: true
                    }
                ]
            }
        ],

        currentsubclass: 0,

        concatClassFeatures () {
            concatenated =[];

            for (let i = 0; i < this.features.length; i++) {
                concatenated.push(this.features[i]);
            }
            for (let i = 0; i < this.subclasses[this.currentsubclass].features.length; i++) {
                concatenated.push(this.subclasses[this.currentsubclass].features[i]);
            }

            sorted = concatenated.sort((a, b) => (a.level > b.level) ? 1 : -1);

            return(sorted);
        }
    }))
})
