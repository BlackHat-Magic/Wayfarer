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
        },

        compileRace () {
            race = {
                name: this.name,

                asis: this.asis,
                asi_override: this.asi_override,
                asi_text: this.asi_text,

                size: this.size,
                size_override: this.size_override,
                size_text: this.size_text,

                base_height: this.base_height,
                height_num: this.height_num,
                height_die: this.height_die,

                base_weight: this.base_weight,
                weight_num: this.weight_num,
                weight_die: this.weight_die,

                walk: this.walk,
                swim: this.swim,
                climb: this.climb,
                fly: this.fly,
                burrow: this.burrow,

                text: this.text,

                features: this.features,

                has_subraces: this.has_subraces,
                subraces: this.subraces,
                subrace_flavor: this.subrace_flavor
            };

            return (race);
        },

        loadRace (race) {
            race = JSON.parse(localStorage.getItem("cached_race"))
            if (race == null) {
                return;
            }
            
            this.name = race.name;

            this.asis = race.asis;
            this.asi_override = race.asi_override;
            this.asi_text = race.asi_text;

            this.size = race.size;
            this.size_override = race.size_override;
            this.size_text = race.size_text;

            this.base_height = race.base_height;
            this.height_num = race.height_num;
            this.height_die = race.height_die;

            this.base_weight = race.base_weight;
            this.weight_num = race.weight_num;
            this.weight_die = race.weight_die;

            this.walk = race.walk;
            this.swim = race.swim;
            this.climb = race.climb;
            this.fly = race.fly;
            this.burrow = race.burrow;

            this.text = race.text;

            this.features = race.features;

            this.has_subraces = race.has_subraces;
            this.subraces = race.subraces;
            this.subrace_flavor = race.subrace_flavor;
        }
    }))
})

document.addEventListener("htmx:afterswap", (event) => {
    Alpine.initializeWithin(event.detail.elt);
})