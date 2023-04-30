
document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        query: "",
        namearray: [" Str", " Dex", " Con", " Int", " Wis", " Cha"],
        filterQuery() {
            sizes = [
                "Tiny",
                "Small",
                "Medium",
                "Large",
                "Huge",
                "Gargantuan"
            ];
            namematch = [];
            for (let i = 0; i < this.raceROM.length; i++) {
                if (this.raceROM[i].name.toLowerCase().includes(this.query.toLowerCase())) {
                    parsedrace = {};
                    parsedrace.name = this.raceROM[i].name;
                    parsedrace.url = this.raceROM[i].name.split(' ').join('-');
                    if (this.raceROM[i].asitext != "None" && this.raceROM[i].asitext != "") {
                        parsedrace.asi = this.raceROM[i].asitext;
                    } else {
                        parsedrace.asi = ""
                        for (let j = 0; j < this.raceROM[i].asis.length; j++) {
                            if(this.raceROM[i].asis[j] != "") { //dont ask me why
                                if(parsedrace.asi.length < 1) {
                                    parsedrace.asi += "+" + this.raceROM[i].asis[j] + " " + this.namearray[j];
                                } else {
                                    parsedrace.asi += ", +" + this.raceROM[i].asis[j] + " " + this.namearray[j];
                                }
                            }
                        }
                    }
                    if (this.raceROM[i].sizetext != null && this.raceROM[i].sizetext != "None") {
                        parsedrace.size = this.raceROM[i].sizetext;
                    } else {
                        parsedrace.size = sizes[this.raceROM[i].size];
                    }
                    namematch.push(parsedrace);
                }
            }
            nameasimatch = [];
            for (let i = 0; i < namematch.length; i++) {
                if(namematch[i].asi.includes(this.abilityfilter) || this.abilityfilter == "null") {
                    nameasimatch.push(namematch[i]);
                } else if (this.abilityfilter == "other" && !namematch[i].asi.includes("+") && !namematch[i].asi.includes("-")) {
                    nameasimatch.push(namematch[i])
                }
            }
            races = []
            for (let i = 0; i < nameasimatch.length; i++) {
                if(nameasimatch[i].size.includes(this.sizefilter) || this.sizefilter == "null") {
                    races.push(nameasimatch[i]);
                } else if (this.sizefilter == "other" && !sizes.includes(nameasimatch[i].size)) {
                    races.push(nameasimatch[i]);
                }
            }
            return races;
        },
        raceROM: [],
        None: null,

        abilityfilter: "",
        parseNum (num) {
            if(num < 0) {
                return("-" + num);
            } else if (num > 0) {
                return("+" + num);
            } else {
                return(null);
            }
        },
        populateASI() {
            output = [];
            for (let i = 0; i < this.raceROM.length; i++) {
                for (let j = 0; j < this.raceROM[i].asis.length; j++) {
                    if (this.raceROM[i].asis[j] != 0 && !output.includes(this.namearray[j])) {
                        output.push(this.namearray[j]);
                    }
                }
            }
            for (let i = 0; i < output.length; i++) {
                document.querySelector("#ability-filter").innerHTML += "<option value='" + output[i] +"'>" + output[i] + "</option>";
            }
            document.querySelector("#ability-filter").innerHTML += "<option value='other'>Other</option>";
        },

        sizefilter: "",
        populateSize () {
            sizearray = [
                "Tiny",
                "Small",
                "Medium",
                "Large",
                "Huge",
                "Gargantuan"
            ]
            target = document.querySelector("#size-filter");
            for (let i = 0; i < this.raceROM.length; i++) {
                if(!target.innerHTML.includes(sizearray[this.raceROM[i].size])) {
                    target.innerHTML += "<option value='" + sizearray[this.raceROM[i].size] + "'>" + sizearray[this.raceROM[i].size] + "</option>";
                }
            }
            target.innerHTML += "<option value='other'>Other</option>"
        }
    }))
})
