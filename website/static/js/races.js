
document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
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
                    if (this.raceROM[i].asitext != "None") {
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
                    if (this.raceROM[i].sizetext != null) {
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
            asis = [
                [],
                [],
                [],
                [],
                [],
                [],
                [" Str", " Dex", " Con", " Int", " Wis", " Cha"]
            ]
            output = [];
            for(let i = 0; i < this.raceROM.length; i++) {
                str = this.raceROM[i].strasi;
                dex = this.raceROM[i].dexasi;
                con = this.raceROM[i].conasi;
                int = this.raceROM[i].intasi;
                wis = this.raceROM[i].wisasi;
                cha = this.raceROM[i].chaasi;
                if(str != null && !asis[0].includes(str)) {
                    asis[0].push(str)
                }
                if (dex != null && !asis[1].includes(dex)) {
                    asis[1].push(dex);
                }
                if (con != null && !asis[2].includes(con)) {
                    asis[2].push(con);
                }
                if (int != null && !asis[3].includes(int)) {
                    asis[3].push(int);
                }
                if (wis != null && !asis[4].includes(wis)) {
                    asis[4].push(wis);
                }
                if (cha != null && !asis[5].includes(cha)) {
                    asis[5].push(cha);
                }
            }
            for (let i = 0; i < asis.length - 1; i++) {
                for (let j = 0; j < asis[i].length; j++) {
                    output.push(this.parseNum(asis[i][j]) + asis[6][i]);
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
