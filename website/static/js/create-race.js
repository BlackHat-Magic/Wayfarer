document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",

        asis: {},
        asi_override: false,
        asi_text: "",
        parseASI () {
            result = "***Ability Scores:*** "
            if (this.asi_override) {
                result += this.asi_text;
                return(result);
            } else {
                multiple = false;
                for (const [key, value] of Object.entries(this.asis)) {
                    if (value > 0) {
                        if (multiple) {
                            result += ", ";
                        } else {
                            multiple = true;
                        }
                        result += key + " +" + value;
                    } else if (value < 0) {
                        if (multiple) {
                            result += ", ";
                        } else {
                            multiple = true;
                        }
                        result += key + value;
                    }
                }
                return(result);
            }
        },

        size: 2,
        size_override: false,
        size_text: "",
        parseSize () {
            result = "***Size:*** "
            if (this.size_override) {
                result += this.size_text;
                return(result)
            } else {
                size_array = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"];
                result += size_array[this.size];
                return(result);
            }
        },

        base_height: null,
        height_num: null,
        height_die: null,

        base_weight: null,
        weight_num: null,
        weight_die: null,

        walk: null,
        swim: null,
        climb: null,
        fly: null,
        burrow: null,
        parseSpeed () {
            result = "***Speed:*** ";
            multiple = false;
            if (parseInt(this.walk) > 0) {
                result += this.walk + " ft.";
            } else {
                result += "0 ft."
            }
            if (parseInt(this.swim) > 0) {
                result += ", swim " + this.swim + " ft.";
            }
            if (parseInt(this.climb) > 0) {
                result += ", climb " + this.climb + " ft.";
            }
            if (parseInt(this.fly) > 0) {
                result += ", fly " + this.fly + " ft.";
            }
            if (parseInt(this.burrow) > 0) {
                result += ", burrow " + this.burrow + " ft.";
            }
            return(result);
        },

        text: "",

        features: [
            {name: "Age", text: ""},
            {name: "Alignment", text: ""},
            {name: "Language", text: ""}
        ],
        addFeature () {
            this.features.push(
                {
                    name: "",
                    text: ""
                }
            );
        }, 
        removeFeature(index) {
            newfeatures = [];
            for (let i = 0; i < this.features.length; i++) {
                console.log("local id: " + this.features[i].lid + "; searching for: " + index);
                if(i != index) {
                    newfeatures.push(
                        this.features[i]
                    );
                }
            }
            console.log(newfeatures);
            this.features = newfeatures;
        },

        has_subraces: false,
        subraces: [],
        subrace_flavor: "",
        addSubrace () {
            this.subraces.push(
                {
                    name: "",
                    text: "",
                    features: []
                }
            )
        },
        removeSubrace (index) {
            newsubraces = [];
            for (let i = 0; i < this.subraces.length; i++) {
                if (i != index) {
                    newsubraces.push(
                        this.subraces[i]
                    )
                }
            }
            this.subraces = newsubraces;
        },
        addSubraceFeature (index) {
            this.subraces[index].features.push(
                {
                    name: "",
                    text: ""
                }
            )
        },
        removeSubraceFeature (subrace, feature) {
            newfeatures = [];
            for (let i = 0; i < this.subraces[subrace].features.length; i++) {
                if (i != feature) {
                    newfeatures.push(
                        this.subraces[subrace].features[i]
                    )
                }
            }
            this.subraces[subrace].features = newfeatures;
        },

        converter: new showdown.Converter({tables: true}),

        convert (text) {
            return(this.converter.makeHtml(text))
        }
    }))
})
