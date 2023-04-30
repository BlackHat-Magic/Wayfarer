document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        feature_file: null,
        parseFeatures () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed_features = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed_features: null,

        flavor_file: null,
        parseFlavor () {
            file = event.target.files[0];
            reader = new FileReader();

            reader.onload = () => {
                const contents = reader.result;
                const data = JSON.parse(contents);
                this.parsed_flavor = JSON.stringify(data);
            };

            reader.readAsText(file);
        },
        parsed_flavor: null
    }))
})