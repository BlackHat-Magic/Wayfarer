document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",
        ismagical: false,
        tier: null,
        rarity: null,
        strength: null,
        stealth: false,

        versatiledisplayers: [],
        rangedisplayers: [],
        checkVersatile() {
            for (let i = 0; i < this.versatiledisplayers.length - 1; i++) {
                if (this.propertylist.includes(this.versatiledisplayers[i])) {
                    return(true)
                }
            }
            return(false)
        },
        checkRange () {
            for (let i = 0; i < this.rangedisplayers.length - 1; i++) {
                if (this.propertylist.includes(this.rangedisplayers[i])) {
                    return(true)
                }
            }
            return(false)
        },

        cost: "",
        weight: "",
        costweight(){
            cost = 0;
            weight = 0;
            if(this.cost != null) {
                cost = this.cost;
            }
            if (this.weight != null) {
                weight = this.weight;
            }
            return(cost + "gp, " + weight + "lbs")
        },

        proficiency: false,
        isweapon: false,
        isarmor: false,
        adddex: false,
        armorclass: null,
        maxdex: null,
        stealthdisadvantage: false,

        tagselect: "",
        taglist: [],
        tags: "",
        appendTag() {
            if(!(this.taglist.includes(document.querySelector("#tagselect").value))){
                this.taglist.push(document.querySelector("#tagselect").value);
            }
            this.updateTags();
        },
        removeTag(index) {
            output = [];
            for (let i = this.taglist.length -1; i >=0; i--) {
                if(i != index) {
                    output.push(this.taglist[i]);
                }
            }
            newoutput = [];
            for (let i = output.length - 1; i >= 0; i--) {
                newoutput.push(output[i])
            }
            this.taglist = newoutput;
            this.updateTags();
        },
        updateTags(){
            output = "";
            for (let i = 0; i < this.taglist.length; i++) {
                if(output.length == 0) {
                    output += this.taglist[i];
                } else {
                    output += ", " + this.taglist[i];
                }
            }
            this.tags = output;
        },

        propertyselect: "",
        propertylist: [],
        properties: "",
        dienum: null,
        damagedie: 4,
        damagetype: "",
        longrange: null,
        shortrange: null,
        versatilenum: null,
        versatiledie: 4,
        appendProperty() {
            if(!(this.propertylist.includes(document.querySelector("#propertyselect").value))) {
                this.propertylist.push(document.querySelector("#propertyselect").value);
            }
            this.updateProperties();
        },
        removeProperty(index) {
            output = [];
            for (let i = this.propertylist.length - 1; i >= 0; i--) {
                if(i != index) {
                    output.push(this.propertylist[i]);
                }
            }
            newoutput = [];
            for (let i = output.length - 1; i >= 0; i--) {
                newoutput.push(output[i])
            }
            this.propertylist = newoutput;
            this.updateProperties();
        },
        updateProperties () {
            output = "";
            for(let i = 0; i < this.propertylist.length; i++) {
                if(output.length == 0) {
                    output += this.propertylist[i];
                } else {
                    output += ", " + this.propertylist[i];
                }
            }
            this.properties = output;
        },

        text: "",

        converter: new showdown.Converter({tables: true}),
        convert(text) {
            return(this.converter.makeHtml(text))
        },

        compileItem () {
            item = {
                name: this.name,
                ismagical: this.ismagical,
                tier: this.tier,
                rarity: this.rarity,
                strength: this.strength,
                stealth: this.stealth,

                versatiledisplayers: this.versatiledisplayers,
                rangedisplayers: this.rangedisplayers,

                cost: this.cost,
                weight: this.weight,

                proficiency: this.proficiency,
                isweapon: this.isweapon,
                isarmor: this.isarmor,
                adddex: this.adddex,
                armorclass: this.armorclass,
                maxdex: this.maxdex,
                stealthdisadvantage: this.stealthdisadvantage,

                taglist: this.taglist, //

                propertylist: this.propertylist, //
                dienum: this.dienum,
                damagedie: this.damagedie,
                damagetype: this.damagetype,
                longrange: this.longrange,
                shortrange: this.shortrange,
                versatilenum: null,
                versatiledie: 4,

                text: this.text
            }

            return (JSON.stringify (item));
        },

        readItem () {
            item = JSON.parse (localStorage.getItem ("cached_item"));
            if(item == null) {
                return;
            }

            this.name = item.name;
            this.ismagical = item.ismagical;
            this.tier = item.tier;
            this.rarity = item.rarity;
            this.strength = item.strength;
            this.stealth = item.stealth;

            this.versatiledisplayers = item.versatiledisplayers;
            this.rangedisplayers = item.rangedisplayers;

            this.cost = item.cost;
            this.weight = item.weight;

            this.proficiency = item.proficiency;
            this.isweapon = item.isweapon;
            this.isarmor = item.isarmor;
            this.adddex = item.adddex;
            this.armorclass = item.armorclass;
            this.maxdex = item.maxdex;
            this.stealthdisadvantage = item.stealthdisadvantage;

            this.taglist = item.taglist;
            this.updateTags ();

            this.propertylist = item.propertylist;
            this.updateProperties ();
            this.dienum = item.dienum;
            this.damagedie = item.damagedie;
            this.damagetype = item.damagetype;
            this.longrange = item.longrange;
            this.shortrannge = item.shortrange;
            this.versatilenum = item.versatilenum;
            this.versatiledie = item.versatiledie;

            this.text = item.text;
        }
    }))
})

document.addEventListener ("htmx:afterswap", (event) => {
    alpine.initializeWithin(event.detail.elt);
})