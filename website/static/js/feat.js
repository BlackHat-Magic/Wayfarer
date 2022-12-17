document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },
        parseASI(asis) {
            output = "";
            for (let i = 0; i < asis.length; i++) {
                if(asis[i] != 0) {
                    if(output.length == 0) {
                        output.append(asis[i]);
                    } else {
                        output.append(", " + asis[i]);
                    }
                }
            }
            return(output);
        }
    }))
})
