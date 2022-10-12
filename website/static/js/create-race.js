document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",

        str: null,
        dex: null,
        con: null,
        int: null,
        wis: null,
        cha: null,
        asi_override: false,
        asi_text: "",
        parseASI () {
            result = "***Ability Scores:*** "
            if (this.asi_override) {
                result += this.asi_text;
                return(result);
            } else {
                stat_array = [
                    {name: "Str", value: this.str}, 
                    {name: "Dex", value: this.dex}, 
                    {name: "Con", value: this.con}, 
                    {name: "Int", value: this.int}, 
                    {name: "Wis", value: this.wis}, 
                    {name: "Cha", value: this.cha}
                ];
                multiple = false;
                for (let i = 0; i < stat_array.length; i++) {
                    if (stat_array[i].value > 0) {
                        if (multiple) {result += ", "} else {multiple = true}
                        result += stat_array[i].name + " +" + stat_array[i].value;
                    } else if (stat_array[i].value < 0) {
                        if (multiple) {result += ", "} else {multiple = true}
                        result += stat_array[i].name + stat_array[i].value;
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
            for (let i = 0; i < this.subraces[subrace].features; i++) {
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

        submit() {
            fname = this.name;
            str = this.str;
            dex = this.dex;
            con = this.con;
            int = this.int;
            wis = this.wis;
            cha = this.cha;
            if (this.asi_override) {
                str = null;
                dex = null;
                con = null;
                int = null;
                wis = null;
                cha = null;
                asi_text = this.asi_text;
            } else {
                asi_text = null;
            }
            size = this.size;
            size_override = this.size_override;
            if (this.size_override) {
                size_text = this.size_text;
            } else {
                size_text = null;
            }
            base_height = this.base_height;
            height_num = this.height_num;
            height_die = this.height_die;
            base_weight = this.base_weight;
            weight_num = this.weight_num;
            weight_die = this.weight_die;
            walk = this.walk;
            swim = this.swim;
            fly = this.fly;
            burrow = this.burrow;
            flavor = this.text;
            features = this.features;
            has_subraces = this.has_subraces;
            if (has_subraces) {
                subraces = this.subraces;
            } else {
                subraces = null;
            }
            
            fetch("/Character/Races/Create", {
                method: "POST",
                body: JSON.stringify({
                    name: fname,
                    str: str,
                    dex: dex,
                    con: con,
                    int: int,
                    wis: wis,
                    cha: cha,
                    asi_text: asi_text,
                    size: size,
                    size_text: size_text,
                    base_height: base_height,
                    height_num: height_num,
                    height_die: height_die,
                    base_weight: base_weight,
                    weight_num: weight_num,
                    weight_die: weight_die,
                    walk: walk,
                    swim: swim,
                    fly: fly,
                    burrow: burrow,
                    flavor: flavor,
                    features: features,
                    has_subraces: has_subraces,
                    subraces: subraces
                })
            })
        }
    }))
})
