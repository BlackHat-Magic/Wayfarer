document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        race_file: null,
        parse () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed_races = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed_races: null
    }))
})
