document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        name: "",

        level: 0,
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
        ],
        time: 0,
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
        ],
        range: 0,
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
        ],
        duration: 0,
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
        ],

        verbal: false,
        somatic: false,
        material: false,
        consumes_material: false,
        concentration: false,
        parseComponents() {
            output = "";
            if(this.verbal) {
                output += "V";
            }
            if(this.somatic) {
                if(output.length == 0) {
                    output += "S";
                } else {
                    output += ", S";
                }
            }
            if(this.material) {
                if(output.length == 0) {
                    output += "M";
                } else {
                    output += ", M";
                }

                if(this.consumes_material) {
                    output += " (" + this.material_specific + ", which the spell consumes)";
                } else {
                    output += " (" + this.material_specific +")";
                }
            }
            return(output)
        },

        school: "Abjuration",

        material_specific: "",

        text: "",

        converter: new showdown.Converter({tables: true}),
        convert(text) {
            return(this.converter.makeHtml(text))
        }
    }))
})
