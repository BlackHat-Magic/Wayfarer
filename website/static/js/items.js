document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        itemROM: [],

        query: "",
        filtertype: "AND",
        filterQuery() {
            match = [];
            for(let i = 0; i < this.itemROM.length; i++) {
                if (this.itemROM[i].name.includes(this.query)) {
                    match.push(this.itemROM[i]);
                }
            }

            console.log(this.filtertype)

            if(this.filtertype == "AND") {
                for (let i = match.length - 1; i >= 0; i--) {
                    for (let j = 0; j < this.taglist.length; j++) {
                        if(!match[i].type.includes(this.taglist[j])) {
                            match.splice(i, 1);
                            break;
                        }
                    }
                }
            } else {
                newmatch = []
                console.log("or")
                for (let i = 0; i < match.length; i++) {
                    for (let j = 0; j < this.taglist.length; j++) {
                        console.log(match[i].type + "; " + this.taglist[j])
                        if(match[i].type.includes(this.taglist[j])) {
                            newmatch.push(match[i]);
                            break;
                        }
                    }
                }
                match = newmatch
            }
            return(match);
        },

        filterTags() {
            console.log("unfinished")
        },

        tags: "",
        taglist: [],
        appendTag() {
            if(!(this.taglist.includes(document.querySelector("#tags").value))){
                this.taglist.push(document.querySelector("#tags").value);
            }
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
        },
    }))
})
