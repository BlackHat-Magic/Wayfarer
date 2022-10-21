
document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        query: "",
        filterQuery() {
            races = []
            for (let i = 0; i < this.raceROM.length; i++) {
                if (this.raceROM[i].name.toLowerCase().includes(this.query.toLowerCase())) {
                    parsedrace = {};
                    parsedrace.name = this.raceROM[i].name;
                    parsedrace.url = this.raceROM[i].name.split(' ').join('-');
                    if (this.raceROM[i].asitext != "None") {
                        parsedrace.asi = this.raceROM[i].asitext;
                    } else {
                        asiarray = [
                            this.raceROM[i].strasi,
                            this.raceROM[i].dexasi,
                            this.raceROM[i].conasi,
                            this.raceROM[i].intasi,
                            this.raceROM[i].wisasi,
                            this.raceROM[i].chaasi
                        ];
                        namearray = [
                            " Str",
                            " Dex",
                            " Con",
                            " Int",
                            " Wis",
                            " Cha"
                        ]
                        parsedrace.asi = ""
                        for (let j = 0; j < asiarray.length; j++) {
                            if(asiarray[j] != null) { //dont ask me why
                                if(parsedrace.asi.length < 1) {
                                    parsedrace.asi += "+" + asiarray[j] + namearray[j];
                                } else {
                                    parsedrace.asi += ", +" + asiarray[j] + namearray[j];
                                }
                            }
                        }
                    }
                    sizes = [
                        "Tiny",
                        "Small",
                        "Medium",
                        "Large",
                        "Huge",
                        "Gargantuan"
                    ];
                    if (this.raceROM[i].sizetext != null) {
                        parsedrace.size = this.raceROM[i].sizetext;
                    } else {
                        parsedrace.size = sizes[this.raceROM[i].size];
                    }
                    races.push(parsedrace);
                }
            }
            console.log(races);
            return races;
        },
        raceROM: [],
        None: null,
    }))
})
