document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        item_file: null,
        parseItem () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed_item = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed_item: null,

        base_file: null,
        parseBase () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed_base = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed_base: null
    }))
})