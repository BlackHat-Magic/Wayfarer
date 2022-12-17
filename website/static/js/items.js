document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        itemROM: [],

        query: "",
        filterQuery() {
            namematch = [];
            for(let i = 0; i < this.itemROM.length; i++) {
                if (this.itemROM[i].name.includes(this.query)) {
                    namematch.push(this.itemROM[i]);
                }
            }

            nameskillmatch = [];
            return(namematch);
        },
    }))
})
