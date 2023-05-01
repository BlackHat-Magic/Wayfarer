document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        None: 0,
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
        parseComponents(verbal, somatic, material, material_specific, consumes_material) {
            output = "";
            if(verbal == "True") {
                output += "V";
            }
            if(somatic == "True") {
                if(output.length == 0) {
                    output += "S";
                } else {
                    output += ", S";
                }
            }
            if(material == "True") {
                if(output.length == 0) {
                    output += "M";
                } else {
                    output += ", M";
                }

                if(consumes_material == "True") {
                    output += " (" + material_specific + ", which the spell consumes)";
                } else {
                    output += " (" + material_specific +")";
                }
            }
            return(output)
        },
    }))
})
