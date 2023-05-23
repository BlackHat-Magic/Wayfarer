document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        query: "",
        bgROM: [],
        truncateEquipment(){
            for (let i = 0; i < this.bgROM.length; i++) {
                if(this.bgROM[i].equipment.length > 40) {
                    this.bgROM[i].equipment = this.bgROM[i].equipment.substring(0, 33) + "..."
                }
            }
        },
        filterQuery() {
            namematch = [];
            for(let i = 0; i < this.bgROM.length; i++) {
                if (this.bgROM[i].name.includes(this.query)) {
                    namematch.push(this.bgROM[i]);
                }
            }
            return(namematch);
        },
        capitalize (string) {
            words = string.split(" ");
            for (let i = 0; i < words.length; i++) {
                words[i] += words[i][0].toUpperCase() + words[i].substr(1) + " ";
            }
            return(words.join(" "));
        },

        filtertype: true,
        
        lstostr(input) {
            if(input.length < 1) {
                return("N/A")
            }
            output = ""
            for (let i = 0; i < input.length; i++) {
                if(output.length > 0) {
                    output += ", "
                }
                output += input[i];
            }
            return(output);
        }
    }))
})
