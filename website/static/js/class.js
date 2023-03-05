document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        name: "",

        tabclass(index) {
            if(index - 1 == this.currentsubclass) {
                return("active tab");
            } else {
                return("tab")
            }
        },

        subclasses: [],
        save: [],
        features: [],

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
