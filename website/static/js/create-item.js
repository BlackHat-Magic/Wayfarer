document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",

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
        damagedie: "d4",
        damagetype: "",
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
        }
    }))
})
