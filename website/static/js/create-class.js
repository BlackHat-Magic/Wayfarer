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

        subclasslevel: 3,

        columns: [],
        appendColumn () {
            values = [];
            for (let i = 0; i < this.levels; i++) {
                values.push("");
            }
            this.columns.push({
                name: "",
                values: values
            })
        },
        deleteColumn (index) {
            output = [];
            for (let i = 0; i < this.columns.length; i++) {
                if (i != index) {
                    output.push(this.columns[i]);
                }
            }
            this.columns = output;
        },

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
        deleteFeature(index) {
            output = [];
            for (let i = 0; i < this.features.length; i++) {
                if (index != i) {
                    output.push(this.features[i]);
                }
            }
            this.features = output;
        },

        subclasses: [
            {
                name: "",
                text: "",
                castertype: 0,
                columns: [],
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
        appendSubclassColumn (subclass) {
            console.log(subclass)
            values = [];
            for (let i = 0; i < this.levels; i++) {
                values.push("");
            }
            this.subclasses[subclass].columns.push({
                name: "",
                values: values
            })
        },
        deleteSubclassColumn (subclass, index) {
            output = [];
            for (let i = 0; i < this.columns.length; i++) {
                if (i != index) {
                    output.push(this.columns[i]);
                }
            }
            this.subclasses[subclass].columns = output;
        },
        spelllist: [
            [],
            [
                [0, 0, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                [0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
            ],
            [
                [0, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                [0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2]
            ],
            [
                [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                [0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
            ]
        ],
        deleteSubclass(index) {
            output = [];
            for (let i = 0; i < this.subclasses.length; i++) {
                if (index != i) {
                    output.push(this.subclasses[i]);
                }
            }
            this.subclasses = output;
        },
        deleteSubclassFeature (subclass, feature) {
            output = [];
            for (let i = 0; i < this.subclasses[subclass].features.length; i++) {
                if (feature != i) {
                    output.push(this.subclasses[subclass].features[i]);
                }
            }
            this.subclasses[subclass].features = output;
        },

        parseFeatures (level) {
            output = "";
            for (let i = 0; i < this.features.length; i++) {
                if (this.features[i].level == level) {
                    if (output.length < 1) {
                        output += this.features[i].name;
                    } else {
                        output += ", " + this.features[i].name;
                    }
                }
            }
            for (let i = 0; i < this.subclasses[this.currentsubclass].features.length; i++) {
                if (this.subclasses[this.currentsubclass].features[i].level == level) {
                    if (output.length < 1) {
                        output += this.subclasses[this.currentsubclass].name + " Feature: " + this.subclasses[this.currentsubclass].features[i].name;
                    } else {
                        output += ", " + this.subclasses[this.currentsubclass].name + " Feature: " + this.subclasses[this.currentsubclass].features[i].name;
                    }
                }
            }
            return(output);
        },

        currentsubclass: 0,

        concatClassFeatures () {
            concatenated =[];

            for (let i = 0; i < this.features.length; i++) {
                concatenated.push(this.features[i]);
            }
            for (let i = 0; i < this.subclasses[this.currentsubclass].features.length; i++) {
                concatenated.push(this.subclasses[this.currentsubclass].features[i]);
            }

            sorted = concatenated.sort((a, b) => (parseInt(a.level) > parseInt(b.level)) ? 1 : -1);

            return(sorted);
        }
    }))
})
