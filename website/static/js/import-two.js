document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        feature_file: null,
        modal: false,
        parseFeatures () {
            file = event.target.files[0];
            if(file.size > 2 * 1024 * 1024) {
                this.modal = true;
                event.target.value = null;
            } else {
                reader = new FileReader();

                reader.onload = () => {
                    const contents = reader.result;
                    const data = JSON.parse(contents);
                    this.parsed_features = JSON.stringify(data);
                };

                reader.readAsText(file);
            }
        },
        parsed_features: null,

        flavor_file: null,
        parseFlavor () {
            file = event.target.files[0];
            if(file.size > 2 * 1024 * 1024) {
                this.modal = true;
                event.target.value = null;
            } else {
                reader = new FileReader();

                reader.onload = () => {
                    const contents = reader.result;
                    const data = JSON.parse(contents);
                    this.parsed_flavor = JSON.stringify(data);
                };

                reader.readAsText(file);
            }
        },
        parsed_flavor: null
    }))
})