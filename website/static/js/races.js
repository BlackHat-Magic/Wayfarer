
document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        initParams () {
            params = new URLSearchParams(window.location.search);
            this.query = params.get("query") || "";
            this.ability = params.get("ability");
            this.size = params.get("size");
        },

        updateQuery() {
            params = new URLSearchParams(window.location.search);
            if (this.query != null && this.query != "") {
                params.set("query", this.query);
            } else {
                params.delete("query")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },

        query: "",
        namearray: [],
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

        updateAbility() {
            params = new URLSearchParams(window.location.search);
            if (this.abilityfilter != null && this.abilityfilter != "null") {
                params.set("ability", this.abilityfilter);
            } else {
                params.delete("ability")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },

        sizefilter: "",
        sizedict: [
            "Tiny",
            "Small",
            "Medium",
            "Large",
            "Huge",
            "Gargantuan"
        ],
        populateSize () {
            sizearray = []
            for (let i = 0; i < this.raceROM.length; i++) {
                if (!sizearray.includes(this.sizedict[this.raceROM[i].size])) {
                    sizearray.push(this.sizedict[this.raceROM[i].size]);
                }
            }
            target = document.querySelector("#size-filter");
            for (let i = 0; i < sizearray.length; i++) {
                target.innerHTML += `<option value="${sizearray[i]}">${sizearray[i]}</option>`;
            }
        },

        updateSize() {
            params = new URLSearchParams(window.location.search);
            if (this.sizefilter != null && this.sizefilter != "null") {
                params.set("size", this.sizefilter);
            } else {
                params.delete("size")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
    }))
})
