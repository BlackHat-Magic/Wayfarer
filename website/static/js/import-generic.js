document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        file: null,
        modal: false,
        parse () {
            file = event.target.files[0];
            if(file.size > 2 * 1024 * 1024) {
                this.modal = true;
                event.target.value = null;
            } else {
                reader = new FileReader();

                reader.onload = () => {
                    const contents = reader.result;
                    const data = JSON.parse(contents);
                    this.parsed = JSON.stringify(data);
                };

                reader.readAsText(file);
            }
        },
        parsed: null,
    }))
})