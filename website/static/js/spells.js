document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        initParams () {
            params = new URLSearchParams(window.location.search);
            this.query = params.get("query") || "";
            if (params.get("schools")) {
                this.schools = params.get("schools").split(",");
            }
            this.level = params.get("level") || 13;
            this.time = params.get("time") || 11;
            this.range = params.get("range") || 24;
            this.duration = params.get("duration") || 12;
            console.log(params.get("level"))
        },
        updateQuery () {
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
        updateSchools () {
            params = new URLSearchParams(window.location.search);
            if (this.schools != null && this.schools != []) {
                params.set("schools", this.schools.toString());
            } else {
                params.delete("schools")
            }
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
        updateLevel () {
            params = new URLSearchParams(window.location.search);
            params.set("level", this.level)
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
        updateTime () {
            params = new URLSearchParams(window.location.search);
            params.set("time", this.time)
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
        updateRange () {
            params = new URLSearchParams(window.location.search);
            params.set("range", this.range)
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },
        updateDuration () {
            params = new URLSearchParams(window.location.search);
            params.set("duration", this.duration)
            new_url = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
            if (params.toString() != null && params.toString() != "") {
                new_url += `?${params.toString()}`
            }
            history.pushState({}, null, new_url)
        },

        itemROM: [],

        query: "",
        filtertype: "AND",

        level: 13,
        levellist: [
            "Cantrip",
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th",
            "8th",
            "9th",
            "10th",
            "11th",
            "12th",
            "Any"
        ],
        time: 11,
        timelist: [
            "1 Reaction",
            "1 Bonus Action",
            "1 Action",
            "1 Round",
            "1 Minute",
            "10 Minutes",
            "1 Hour",
            "8 Hours",
            "12 Hours",
            "24 Hours",
            "Special",
            "Any"
        ],
        range: 24,
        rangelist: [
            "Self",
            "Touch",
            "5 feet",
            "10 feet",
            "15 feet",
            "20 feet",
            "25 feet",
            "30 feet",
            "40 feet",
            "60 feet",
            "90 feet",
            "100 feet",
            "120 feet",
            "150 feet",
            "240 feet",
            "300 feet",
            "500 feet",
            "1000 feet",
            "1 mile",
            "5 miles",
            "500 miles",
            "Sight",
            "Unlimited",
            "Special",
            "Any"
        ],
        duration: 12,
        durationlist: [
            "Instantaneous",
            "1 Round",
            "1 Minute",
            "10 Minutes",
            "1 Hour",
            "8 Hours",
            "24 Hours",
            "10 Days",
            "30 Days",
            "1 Year",
            "Until Dispelled",
            "Special",
            "Any"
        ],
        parseComponents(spell) {
            output = "";
            if(spell.verbal == "True") {
                output += "V";
            }
            if(spell.somatic == "True") {
                if(output.length == 0) {
                    output += "S";
                } else {
                    output += ", S";
                }
            }
            if(spell.material == "True") {
                if(output.length == 0) {
                    output += "M";
                } else {
                    output += ", M";
                }
                output += " (" + spell.material_specific + ")"
            }
            return(output)
        },
        filterQuery() {
            match = [];
            for(let i = 0; i < this.itemROM.length; i++) {
                if (this.itemROM[i].name.includes(this.query)) {
                    match.push(this.itemROM[i]);
                }
            }

            //schools
            newmatch = []
            for (let i = 0; i < match.length; i++) {
                if(this.schools.includes(match[i].school)) {
                    newmatch.push(match[i]);
                }
            }
            match = newmatch;

            //level
            if(this.level != 13){
                newmatch = [];
                for (let i = 0; i < match.length; i++) {
                    if(match[i].level == this.level) {
                        newmatch.push(match[i]);
                    }
                }
                match = newmatch;
            }

            //time
            if(this.time != 11){
                newmatch = [];
                for (let i = 0; i < match.length; i++) {
                    if(match[i].casting_time == this.time) {
                        newmatch.push(match[i]);
                    }
                }
                match = newmatch;
            }

            //range
            if(this.range != 24) {
                newmatch = [];
                for (let i = 0; i < match.length; i++) {
                    if(match[i].spell_range == this.range) {
                        newmatch.push(match[i]);
                    }
                }
                match = newmatch;
            }

            //duration
            if(this.duration != 12){
                newmatch = [];
                for (let i = 0; i < match.length; i++) {
                    if(match[i].duration == this.duration) {
                        newmatch.push(match[i]);
                    }
                }
                match = newmatch;
            }
            return(match);
        },

        school: "Abjuration",
        schools: [],
        appendSchool() {
            this.updateSchools();
            if(!(this.schools.includes(document.querySelector("#school").value && this.school != ""))){
                this.schools.push(document.querySelector("#school").value);
            }
        },
        removeSchool(index) {
            this.updateSchools();
            output = [];
            for (let i = this.schools.length -1; i >=0; i--) {
                if(i != index) {
                    output.push(this.schools[i]);
                }
            }
            newoutput = [];
            for (let i = output.length - 1; i >= 0; i--) {
                newoutput.push(output[i])
            }
            this.schools = newoutput;
        },
    }))
})
