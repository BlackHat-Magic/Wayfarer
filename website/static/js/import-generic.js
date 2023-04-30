document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        file: null,
        parse () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed: null,
    }))
})