document.addEventListener ("alpine:init", () => {
    Alpine.data ("main", () => ({
        converter: new showdown.Converter({tables: true}),
        convert (text) {
            return(this.converter.makeHtml(text));
        },

        randint(num1, num2) {
            return(Math.floor(Math.random() * (num1 - num2) + num1))
        },
        displayed_character: null,

        random_name: true,
        name: "",
        sex: "Random",

        race_select: "all",
        raceROM: [],
        raceSelectWarnEval () {
            if (this.race_select != "select") {
                return(false);
            }

            for (let i = 0; i < this.raceROM.length; i++) {
                if (this.raceROM[i].selected) {
                    return(false);
                }
            }
            return(true);
        },

        subrace_select: "all",
        subraceShowEval () {
            if (this.race_select != "select") {
                return (false);
            }

            result = false;
            for (let i = 0; i < this.raceROM.length; i++) {
                if (this.raceROM[i].selected) {
                    if (!result) {
                        result = true;
                    } else {
                        return(false)
                    }
                }
            }
            return(result);
        },

        ge_good_weight: 50,
        ge_neutral_weight: 34,
        ge_evil_weight: 16,

        lc_lawful_weight: 50,
        lc_neutral_weight: 34,
        lc_chaotic_weight: 16,

        unaligned_probability: 25,

        random_hw: true,
        height: null,
        weight: null,

        generate () {
            character = {};

            if (this.sex == "Random") {
                character.sex = ["Male", "Female"][Math.floor(Math.random() * 2)]
            } else {
                character.sex = this.sex
            }

            racenames = [];
            uncommonracenames = [];
            for (let i = 0; i < this.raceROM.length; i++) {
                if(this.raceROM[i].selected || this.race_select == "all") {
                    racenames.push(this.raceROM[i].name);
                }
            }
            for (let i = 0; i < racenames.length; i++) {
                if (!["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Elf", "Half-Orc"].includes(racenames[i])) {
                    uncommonracenames.push(racenames[i]);
                }
            }

            racepercent = Math.random();
            if (racepercent <= 0.5) {
                if (racenames.includes("Human")) {
                    character.race = "Human";
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)];
                }
            } else if (racepercent <= 0.65) {
                if (racenames.includes("Elf")) {
                    character.race = "Elf";
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)];
                }
            } else if (racepercent <= 77) {
                if (racenames.includes("Dwarf")) {
                    character.race = "Dwarf";
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)];
                }
            } else if (racepercent <= 85) {
                if (racenames.includes("Halfling")) {
                    character.race = "Haflling";
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)];
                }
            } else if (racepercent <= 89) {
                if (racenames.includes("Gnome")) {
                    character.race = "Gnome"
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)];
                }
            } else if (racepercent <= 92) {
                if (racenames.includes("Half-Elf")) {
                    character.race = "Half-Elf"
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)]
                }
            } else if (racepercent <= 95) {
                if (racenames.includes("Half-Orc")) {
                    character.race = "Half-Orc"
                } else {
                    character.race = racenames[Math.floor(Math.random() * racenames.length)]
                }
            } else if (uncommonracenames.length > 0) {
                character.race = uncommonracenames[Math.floor(Math.random() * uncommonracenames.length)]
            } else {
                character.race = racenames[Math.floor(Math.random() * racenames.length)]
            }

            for (let i = 0; i < this.raceROM.length; i++) {
                if (this.raceROM[i].name == character.race) {
                    if (this.raceROM[i].subraces.length > 0) {
                        possible_subraces = []
                        for (let j = 0; j < this.raceROM[i].subraces.length; j++) {
                            if (this.raceROM[i].subraces[j].selected) {
                                possible_subraces.push(this.raceROM[i].subraces[j].name)
                            }
                        }
                        character.subrace = possible_subraces[Math.floor(Math.random() * this.raceROM[i].subraces.length)]
                    } else {
                        character.subrace = "N/A"
                    }
                }
            }

            if (!this.random_name) {
                character.full_name = this.name;
            } else {
                namelib = []
                first_syl = [
                    "","","","","A","Be","De","El","Fa","Jo","Ki","La","Ma","Na","O","Pa","Re","Si","Ta","Va"
                ]
                second_syl = [
                    "Bar","Ched","Dell","Far","Gran","Hal","Jen","Kel","Lim","Mor","Net","Penn","Quil","Rond","Sark","Shen","Tur","Vash","Yor","Zen"
                ]
                third_syl = [
                    "","a","ac","ai","al","am","an","ar","ea","el","er","ess","ett","ic","id","il","in","is","or","us"
                ]
                for (let i = 0; i < first_syl.length; i++) {
                    for (let j = 0; j < second_syl.length; j++) {
                        for (let k = 0; k < third_syl.length; k++) {
                            fillername = first_syl[i] + second_syl[j] + third_syl[k]
                            namelib.push(fillername.charAt(0) + fillername.slice(1));
                        }
                    }
                }
                if (character.race == "Dragonborn") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Akra","Aasathra","Antrara","Arava","Biri","Blendaeth","Burana","Chassath","Daar","Dentratha","Doudra","Driindar","Eggren", "Farideh","Findex","Furelle","Gesrethe","Gilkass","Harann","Havilar","Hethress","Hillanot","Jaxi","Jezean","Jheri","Kadana", "Kava","Korinn","Megren","Mijira","Mishan","Nala","Nuthra","Perra","Pogranix","Pyxrin","Quespa","Raiann","Rezena","Ruloth", "Saphara","Savaran","Sora","Surina","Synthrin","Tatyan","Thava","Thava","Uadjit","Vezera","Zykroff"
                        ]
                    } else {
                        namelib = [
                            "Arjhan","Balasar","Bharash","Donaar","Ghesh","Heskan","Kriv","Medrash","Mehen","Nadarr","Pandjed","Patrin","Rhogar", "Shamash","Shedinn","Tarhun","Torinn","Adrex","Azzakh","Baradad","Bharash","Bidreked","Dadalan","Dazzazn","Direcris","Fax", "Gargax","Gorbundus","Greethen","Hirrathak","Ildrex","Kaladan","Kerkad","Kiirith","Maagog","Medrash","Mozikth","Mreksh", "Mugrunden","Nithther","Norkruuth","Nykkan","Pijjirik","Quarethon","Rathkran","Rivaan","Srorthen","Trynnicus","Valorean", "Vrondiss","Zedaar"
                        ]
                    }
                } else if (character.race == "Dwarf") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Anbera","Artin","Audhild","Balifra","Barbena","Bardryn","Bolhild","Dagnal","Dariff","Delre","Diesa","Eldeth","Eridred", "Falkrunn","Fallthra","Finellen","Gillydd","Gunnloda","Gurdis","Helgret","Helja","Hlin","Ilde","Jarana","Kathra","Kilia", "Kristryd","Liftrasa","Marastyr","Mardred","Morana","Nalaed","Nora","Nurkara","Oriff","Ovina","Riswynn","Sann","Therlin", "Thodris","Torbera","Tordrid","Torgga","Urshar","Valida","Vistra","Vonana","Werydd","Whurdred","Yurgunn"
                        ]
                    } else {
                        namelib = [
                            "Adrik","Alberich","Baern","Berendd","Beloril","Brottor","Dain","Dalgal","Darrak","Delg","Duergarth","Dworic","Eberk", "Einkil","Elaim","Erias","Fallond","Fargrim","Gardain","Gilthur","Gimgen","Gimurt","Harbek","Kildrak","Kilvar","Morgran", "Morkral","NalRal","Nordak","Nuraval","Oloric","Olunt","Orsik","Oskar","Rangrim","Reirak","Rurik","Taklinn","Thoradin", "Thorin","Thradal","Tordek","Traubon","Travok","Ulfgar","Uraim","Veit","Vonbin","Vondal","Whurbin"
                        ]
                    }
                } else if (character.race == "Elf") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Adran","Aelar","Aerdeth","Ahvain","Aramil","Arannis","Aust","Azaki","Beiro","Berrian","Caeldrim","Carric","Dayereth", "Dreali","Efferil","Eiravel","Enialis","Erdan","Erevan","Fivin","Galinndan","Gennal","Hadarai","Halimath","Heian", "Himo","Immeral","Ivellios","Korfel","Lamlis","Laucian","Lucan","Mindartis","Naal","Nutae","Paelias","Peren","Quarion", "Riardon","Rolen","Soveliss","Suhnae","Thamior","Tharivol","Theren","Theriatis","Thervan","Uthemar","Vanuath","Varis", "Ael","Ang","Ara","Ari","Arn","Aym","Broe","Bryn","Cael","Cy","Dae","Del","Eli","Eryn","Faen","Fera","Gael","Gar","Innil", "Jar","Kan","Koeth","Lael","Lue","Mai","Mara","Mella","Mya","Naeris","Naill","Nim","Phann","Py","Rael","Ren","Rinn","Rua", "Sael","Sai","Sumi","Syllin","Ta","Shia","Thia","Tia","Traki","Vall","Von","Wil","Za"
                        ]
                    } else {
                        namelib = [
                            "Adran","Aelar","Aerdeth","Ahvain","Aramil","Arannis","Aust","Azaki","Beiro","Berrian","Caeldrim","Carric","Dayereth", "Dreali","Efferil","Eiravel","Enialis","Erdan","Erevan","Fivin","Galinndan","Gennal","Hadarai","Halimath","Heian", "Himo","Immeral","Ivellios","Korfel","Lamlis","Laucian","Lucan","Mindartis","Naal","Nutae","Paelias","Peren","Quarion", "Riardon","Rolen","Soveliss","Suhnae","Thamior","Tharivol","Theren","Theriatis","Thervan","Uthemar","Vanuath","Varis", "Ael","Ang","Ara","Ari","Arn","Aym","Broe","Bryn","Cael","Cy","Dae","Del","Eli","Eryn","Faen","Fera","Gael","Gar","Innil", "Jar","Kan","Koeth","Lael","Lue","Mai","Mara","Mella","Mya","Naeris","Naill","Nim","Phann","Py","Rael","Ren","Rinn","Rua", "Sael","Sai","Sumi","Syllin","Ta","Shia","Thia","Tia","Traki","Vall","Von","Wil","Za"
                        ]
                    }
                } else if (character.race == "Gnome") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Abalaba","Bimpnottin","Breena","Buvvie","Callybon","Caramip","Carlin","Cumpen","Dalaba","Donella","Duvamil","Ella", "Ellyjoybell","Ellywick","Enidda","Lilli","Loopmottin","Lorilla","Luthra","Mardnab","Meena","Menny","Mumpena","Nissa", "Numba","Nyx","Oda","Oppah","Orla","Panana","Pyntle","Quilla","Ranala","Reddlepop","Roywyn","Salanop","Shamil","Siffress", "Symma","Tana","Tenena","Tervaround","Tippletoe","Ulla","Unvera","Veloptima","Virra","Waywocket","Yebe","Zanna"
                        ]
                    } else {
                        namelib = [
                            "Alston","Alvyn","Anverth","Arumawann","Bilbron","Boddynock","Brocc","Burgell","Cockaby","Crampernap","Dabbledob", "Delebean","Dimble","Eberdeb","Eldon","Erky","Fablen","Fibblestib","Fonkin","Frouse","Frug","Gerbo","Gimble","Glim","Igden", "Jabble","Jebeddo","Kellen","Kipper","Namfoodle","Oppleby","Orryn","Paggen","Pallabar","Pog","Qualen","Ribbles","Rimple", "Roondar","Sapply","Seebo","Senteq","Sindri","Umpen","Wrryn","Wiggens","Wobbles","Wrenn","Zaffarb","Zook"
                        ]
                    }
                } else if (character.race == "Half-Elf") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Adrie","Ahinar","Althaea","Anastrianna","Andraste","Antinua","Arara","Baelitae","Bethrynna","Birel","Caelynn","Chaedi", "Cliara","Dara","Drusilia","Elama","Enna","Faral","Felosial","Hatae","Ielenia","Ilanis","Irann","Jarsali","Jelenneth", "Keyleth","Leshanna","Lia","Maiathah","Malquis","Meriele","Mialee","Myathethil","Naivara","Quelenna","Quillathe","Ridaro", "Sariel","Shanairla","Shava","Silaqui","Sumnes","Theirastra","Thiala","Tiaathque","Traulam","Vadania","Valanthe","Valna", "Xanaphia"
                        ]
                    } else {
                        namelib = [
                            "Adran","Aelar","Aerdeth","Ahvain","Aramil","Arannis","Aust","Azaki","Beiro","Berrian","Caeldrim","Carric","Dayereth", "Dreali","Efferil","Eiravel","Enialis","Erdan","Erevan","Fivin","Galinndan","Gennal","Hadarai","Halimath","Heian", "Himo","Immeral","Ivellios","Korfel","Lamlis","Laucian","Lucan","Mindartis","Naal","Nutae","Paelias","Peren","Quarion", "Riardon","Rolen","Soveliss","Suhnae","Thamior","Tharivol","Theren","Theriatis","Thervan","Uthemar","Vanuath","Varis"
                        ]
                    }
                } else if (character.race == "Halfling") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Alain","Andry","Anne","Bella","Blossom","Bree","Callie","Chenna","Cora","Dee","Dell","Elda","Eran","Euphemia","Georgina", "Gynnie","Hariet","Jasmine","Jillian","Jo","Kithri","Lavinia","Lidda","Maegan","Marigold","Merla","Myria","Nedda","Nikki", "Nora","Olivia","Paela","Pearl","Pennie","Philomena","Portia","Robbie","Rose","Saral","Serephina","Shaena","Stacee","Tawna", "Thea","Trym","Tyna","Vani","Verna","Wella","Willow"
                        ]
                    } else {
                        namelib = [
                            "Alton","Ander","Bernie","Bobbin","Cade","Callus","Corrin","Dannad","Danniel","Eddie","Egart","Eldon","Errich","Fildo", "Finnan","Franklin","Garret","Garth","Garth","Gilbert","Gob","Harol","Igor","Jasper","Keith","Kevin","Lazam","Lerry", "Lindal","Lyle","Merric","Mican","Milo","Morrin","Nebin","Nevil","Osborn","Ostran","Oswalt","Perrin","Poppy","Reed", "Roscoe","Sam","Shardon","Tye","Ulmo","Wllby","Wendel","Wenner","Wes"
                        ]
                    }
                } else if (character.race == "Half-Orc") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Arha","Baggi","Bendoo","Bilga","Brakka","Creega","Drenna","Ekk","Emen","Engong","Fistula","Gaaki","Gorga","Grai","Greeba", "Grigi","Gynk","Hrathy","Huru","Ilga","Kabbarg","Kansif","Lagazi","Lezre","Murgen","Murook","Myev","Nagrette","Neega", "Nella","Nogu","Oolah","Ootah","Ovak","Ownka","Puyet","Reeza","Shautha","Silgre","Sutha","Tagga","Tawar","Tomph","Ubada", "Vanchu","Vola","Volen","Vorka","Yevelda","Zagga"
                        ]
                    } else {
                        namelib = [
                            "Argran","Braak","Brug","Cagak","Dench","Dorn","Dren","Druuk","Feng","Gell","Gnarsh","Grog","Grumbar","Gubrash","Hagren", "Henk","Hogar","Holg","Imsh","Karash","Karg","Keth","Korag","Krusk","Lubash","Megged","Mhurren","Mord","Morg","Nil", "Nybarg","Odorr","Ohr","Rendar","Resh","Ront","Rrath","Sark","Scrag","Sheggen","Shump","Tanglar","Tarak","Thar","Thokk", "Trag","Ugarth","Varg","Vilberg","Yurk","Zed"
                        ]
                    }
                } else if (character.race == "Human" || character.race == "Tiefling") {
                    if (character.sex == "Female") {
                        namelib = [
                            "Abigail", "Ada", "Addison", "Aimee", "Alice", "Alicia", "Allison", "Alyssa", "Amanda", "Amber", "Amy", "Andrea", "Angela", "Anna", "Anne", "April", "Ariel", "Ashley", "Audrey", "Ava", "Barbara", "Becky", "Bella", "Bernice", "Beth", "Betty", "Beverly", "Bonnie", "Brenda", "Brianna", "Brittany", "Brooke", "Caitlin", "Camilla", "Candice", "Cara", "Carla", "Carol", "Caroline", "Casey", "Catherine", "Cecilia", "Charlotte", "Chelsea", "Cheryl", "Christina", "Christine", "Claire", "Clara", "Claudia", "Colleen", "Connie", "Crystal", "Cynthia", "Daisy", "Dana", "Danielle", "Daphne", "Deanna", "Deborah", "Denise", "Diana", "Diane", "Donna", "Dora", "Doris", "Edith", "Elaine", "Eleanor", "Elizabeth", "Ella", "Ellen", "Emily", "Emma", "Erica", "Erin", "Esther", "Eva", "Evelyn", "Faith", "Felicia", "Fiona", "Frances", "Gabrielle", "Gail", "Grace", "Hailey", "Hannah", "Heather", "Helen", "Holly", "Irene", "Isabel", "Isabella", "Jacqueline", "Jane", "Janet", "Janice", "Jasmine", "Jean", "Jennifer", "Jessica", "Jill", "Jillian", "Joan", "Joanne", "Jocelyn", "Joy", "Joyce", "Judy", "Julia", "Julie", "Kaitlyn", "Karen", "Kate", "Kathleen", "Kathryn", "Katie", "Kayla", "Kelly", "Kelsey", "Kim", "Kimberly", "Kristen", "Laura", "Lauren", "Leah", "Lillian", "Linda", "Lindsay", "Lisa", "Lois", "Lori", "Louise", "Lydia", "Lynne", "Mabel", "Madeline", "Madison", "Margaret", "Maria", "Marie", "Marilyn", "Marissa", "Martha", "Mary", "Megan", "Melanie", "Melissa", "Meredith", "Mia", "Michelle", "Mildred", "Monica", "Nancy", "Naomi", "Natalie", "Natasha", "Nicole", "Nina", "Nora", "Norma", "Olivia", "Paige", "Pamela", "Patricia", "Paula", "Peggy", "Penelope", "Phoebe", "Priscilla", "Rachel", "Rebecca", "Renee", "Rhonda", "Rita", "Robin", "Rose", "Ruth", "Samantha", "Sandra", "Sara", "Sarah", "Shannon", "Sharon", "Sheila", "Sherry", "Shirley", "Sofia", "Sonia", "Stephanie", "Susan", "Sylvia", "Tamara", "Tanya", "Teresa", "Tina", "Trisha", "Valerie", "Vanessa"
                        ]
                    } else if (character.sex == "Male") {
                        namelib = [
                            "Aaron", "Adam", "Adrian", "Aiden", "Alan", "Albert", "Alex", "Alexander", "Alfred", "Andrew", "Anthony", "Arnold", "Arthur", "Austin", "Barry", "Benjamin", "Bernard", "Bill", "Blake", "Bobby", "Brad", "Bradley", "Brandon", "Brett", "Brian", "Bruce", "Bryan", "Caleb", "Cameron", "Carl", "Carlos", "Chad", "Charles", "Chris", "Christian", "Christopher", "Cody", "Colin", "Connor", "Corey", "Dale", "Daniel", "Darren", "David", "Dean", "Dennis", "Derek", "Devin", "Dominic", "Don", "Donald", "Douglas", "Drew", "Dylan", "Earl", "Eddie", "Edward", "Elijah", "Eric", "Ethan", "Evan", "Felix", "Francis", "Frank", "Fred", "Gabriel", "Gary", "George", "Gerald", "Greg", "Harry", "Henry", "Howard", "Ian", "Isaac", "Jack", "Jackson", "Jacob", "Jake", "James", "Jason", "Jeff", "Jeffrey", "Jeremy", "Jerry", "Jesse", "Jim", "Joe", "John", "Johnny", "Joseph", "Josh", "Justin", "Keith", "Ken", "Kevin", "Kyle", "Lance", "Larry", "Lawrence", "Lee", "Leo", "Leonard", "Liam", "Logan", "Louis", "Lucas", "Luke", "Malcolm", "Mark", "Martin", "Mason", "Matthew", "Michael", "Mike", "Miles", "Mitchell", "Neil", "Nelson", "Nick", "Noah", "Oliver", "Oscar", "Owen", "Pat", "Patrick", "Paul", "Peter", "Phil", "Philip", "Ralph", "Randy", "Ray", "Richard", "Rick", "Riley", "Robert", "Roger", "Ron", "Ross", "Roy", "Ryan", "Sam", "Scott", "Sean", "Sebastian", "Seth", "Shane", "Shawn", "Simon", "Spencer", "Stan", "Stephen", "Steve", "Stuart", "Ted", "Terry", "Thomas", "Tim", "Todd", "Tom", "Tony", "Travis", "Trevor", "Tyler", "Vincent", "Walter", "Wayne", "William", "Xavier", "Zach", "Zachary", "Zane", "Abel", "Maximilian", "Alonzo", "Anders", "Bradford", "Clarence", "Cornelius", "Dante", "Edmund", "Emerson", "Fletcher", "Gunner", "Harrison", "Ira", "Jarvis", "Kendrick", "Lawson", "Orson", "Preston", "Quentin", "Reginald", "Silas", "Thaddeus", "Ulrich", "Vaughn", "Winston", "York"
                        ]
                    } else {
                        namelib = [
                            "Alex", "Andy", "Angel", "Ash", "Avery", "Bailey", "Blair", "Blake", "Casey", "Charlie", "Chris", "Corey", "Dana", "Devon", "Drew", "Dylan", "Elliot", "Emery", "Finley", "Frankie", "Gale", "Harley", "Hayden", "Jamie", "Jay", "Jesse", "Jordan", "Kai", "Kelly", "Kennedy", "Lane", "Lee", "Logan", "Morgan", "Pat", "Peyton", "Quinn", "Reese", "Riley", "Robin", "Rory", "Sam", "Skyler", "Taylor", "Terry", "Tony", "Tyler", "Avery", "Cameron", "Carson", "Casey", "Dallas", "Dana", "Devon", "Dorian", "Harley", "Harper", "Hayden", "Jackie", "Jordan", "Kendall", "Kennedy", "Landry", "Lee", "Leslie", "Logan", "Mackenzie", "Madison", "Micah", "Morgan", "Parker", "Peyton", "Phoenix", "Presley", "Reese", "River", "Ryan", "Sage", "Shannon", "Sidney", "Sky", "Sydney", "Taylor", "Teagan", "Terry", "Tracy", "Val", "Whitney", "Addison", "Ainsley", "Alex", "Bailey", "Casey", "Charlie", "Dale", "Ellis", "Finley", "Grey", "Harper", "Spencer"
                        ]
                    }
                }
                character.first_name = namelib[Math.floor(Math.random() * namelib.length)]

                namelib = []
                first_syl = [
                    "","","","","A","Be","De","El","Fa","Jo","Ki","La","Ma","Na","O","Pa","Re","Si","Ta","Va"
                ]
                second_syl = [
                    "Bar","Ched","Dell","Far","Gran","Hal","Jen","Kel","Lim","Mor","Net","Penn","Quil","Rond","Sark","Shen","Tur","Vash","Yor","Zen"
                ]
                third_syl = [
                    "","a","ac","ai","al","am","an","ar","ea","el","er","ess","ett","ic","id","il","in","is","or","us"
                ]
                for (let i = 0; i < first_syl.length; i++) {
                    for (let j = 0; j < second_syl.length; j++) {
                        for (let k = 0; k < third_syl.length; k++) {
                            namelib.push(first_syl[i] + second_syl[j] + third_syl[k]);
                        }
                    }
                }
                if (character.race == "Dragonborn") {
                    namelib = [
                        "Akambheryliax","Argenthrixus","Baharoosh","Beryntolthropal","Bhenkumbyrznaax","Caavylteradyn","Chumbyxirinnish", "Clethinthiallor","Daardendrian","Delmirev","Dhyrktelonis","Ebynichtomonis","Esstyrlynn","Fharngnarthnost","Ghaallixirn", "Grrrmmballhyst","Gygazzylyshrift","Hashphronyxadyn","Hshhsstoroth","Imbixtellrhyst","Jerynomonis","Jharthraxyn", "Kerrhylon","Kimbatuul","Lhamboldennish","Linxakasendalor","Mohradyllion","Mystan","Nemmonis","Norixius","Ophinshtalajiir", "Orexijandilin","Pfaphnyrennish","Phrahdrandon","Qyxpahrgh","Raghthroknaar","Shestendeliath","Skaarzborroosh","Sumnarghthrysh", "Tiammanthyllish","Turnuroth","Umbyrphrael","Vangdondalor","Verthisathurgiesh","Wivvyrholdalphiax","Wystongjiir","Xephyrbahnor", "Yarjerit","Zzzxaaxthroth"
                    ]
                } else if (character.race == "Dwarf") {
                    namelib = [
                        "Aronore","Balderk","Battlehammer","Bigtoe","Bloodkith","Bofdann","Brawnanvil","Brazzik","Broodfist","Burrowfound","Caebrek", "Daerdahk","Dankil","Daraln","Deepdelver","Durthane","Eversharp","Fallack","Fireforge","Foamtankard","Frostbeard","Glanhig", "Goblinbane","Goldfinder","Gorunn","Graybeard","Whitebeard","Blackbeard","Brownbeard","Redbeard","Hammerstone","Helcral", "Holderhek","Ironfist","Loderr","Lutgehr","Morigak","Orcfoe","Rakankrak","Ruvy-Eye","Rumnaheim","Silveraxe","Silverstone", "Steelfist","Stoutale","Strakeln","Strongheart","Thrahak","Torevir","Torunn","Trollbleeder","Trueanvil","Trueblood","Ungart"
                    ]
                } else if (character.race == "Elf") {
                    namelib = [
                        "Aloro","Amakiir","Amastacia","Ariessus","Arnuanna","Berevan","Caerdonel","Caphaxath","Casilltenirra","Cithreth","Dalanthan", "Eathalena","Erenaeth","Ethanasath","Fasharash","Firahel","Floshem","Galanodel","Goltorah","Hanali","Holimion","Horineth", "Iathrana","Lathrana","Ilphelkiir","Iranapha","Koehlanna","Lathalas","Liadon","Meliamne","Mellerelel","Mystralath","Nailo", "Netyoive","Ofandrus","Ostoroth","Othronus","Qualanthri","Raethran","Rothenel","Selevarun","Siannodel","Suithrasas","Sylvaranth", "Teinithra","Tilathana","Wasanthi","Withrethin","Xiloscient","Xistsrith","Yaeldrin"
                    ]
                } else if (character.race == "Gnome") {
                    namelib = [
                        "Albaratie","Baffleston","Beren","Boondiggles","Cobblelob","Daergel","Dunben","FabbleStabble","Fapplestamp","Fiddlefen", "Folkor","Garrick","Gimlen","Glittergem","Gobblefirn","Gummen","Horcusporcus","Humplebumple","Ironhide","Leffery","Lingenhall", "Loofollue","Maekkelferce","Miggledy","Munggen","Murnig","Musgraben","Nackle","Ningel","Nopenstallen","Nucklestamp","Offund", "Oomtrowl","Pilwicken","Pingun","Quillsharpener","Raulnor","Reese","Rofferton","Scheppen","Shadowcloak","Silverthread","Sympony", "Tarkelby","Timbers","Turen","Umbodoben","Waggletop","Welber","Wildwander"
                    ]
                } else if (character.race == "Halfling") {
                    namelib = [
                        "Appleblossom","Bigheart","Brightmoon","Brushgather","Cherrycheeks","Copperkettle","Deephollow","Elderberry","Fastfoot", "Fatrabbit","Glenfellow","Goldfound","Goodbarrel","Goodearth","Greenbottle","Greenleaf","High-hill","Hilltopple","Hogcollar", "Honeypot","Jamjar","Kettlewhistle","Leagallow","Littlefoot","Nimblefingers","Nimbletop","Porridgepot","Quickpot","Reedfellow", "Shadowquick","Silvereyes","Smoothhands","Stonebridge","Stoutbridge","Stoutman","Strongbones","Sunmeadow","Swiftwhistle", "Tallfellow","Tealeaf","Tenpenny","Thistletop","Thorngage","Tosscobble","Underbough","Underfoot","Warmwater","Whispermouse", "Wildcloak","Wildheart","Wiseacre"
                    ]
                }
                character.last_name = namelib[Math.floor(Math.random() * namelib.length)]
                character.full_name = character.first_name + " " + character.last_name
            }

            if (!this.random_hw) {
                character.total_height = this.height
                character.total_weight = this.weight
            } else {
                if (character.race == "Dragonborn") {
                    character.base_height = 66;
                    character.height_mod = this.randint(1, 8) + this.randint(1, 8);
                    character.base_weight = 175
                    character.weight_mod = character.height_mod * (this.randint(1, 6) + this.randint(1, 6))
                } else if (character.race == "Dwarf") {
                    character.base_height = 46;
                    character.height_mod = this.randint(1, 4) + this.randint(1, 4);
                    character.base_weight = 115
                    character.weight_mod = character.height_mod * (this.randint(1, 6) + this.randint(1, 6))
                } else if (character.race == "Elf") {
                    character.base_height = 54;
                    character.height_mod = this.randint(1, 10) + this.randint(1, 10);
                    character.base_weight = 90;
                    character.weight_mod = character.height_mod * this.randint(1, 4)
                } else if (character.race == "Gnome") {
                    character.base_height = 35;
                    character.height_mod = this.randint(1, 4) + this.randint(1, 4);
                    character.base_weight = 35;
                    character.weight_mod = this.randint(1, 4) + this.randint(1, 4);
                } else if (character.race == "Half-Orc") {
                    character.base_height = 58;
                    character.height_mod = this.randint(1, 10) + this.randint(1, 10);
                    character.base_weight = 140
                    character.weight_mod = character.height_mod * (this.randint(1, 6) + this.randint(1, 6))
                } else if (character.race == "Half-Elf" || character.race == "Tiefling") {
                    character.base_height = 57;
                    character.height_mod = this.randint(1, 8) + this.randint(1, 8);
                    character.base_weight = 110
                    character.weight_mod = character.height_mod * (this.randint(1, 4) + this.randint(1, 4)) 
                } else if (character.race == "Halfling") {
                    character.base_height = 31;
                    character.height_mod = this.randint(1, 4) + this.randint(1, 4);
                    character.base_weight = 35;
                    character.weight_mod = this.randint(1, 4) + this.randint(1, 4);
                } else {
                    character.base_height = 56;
                    character.height_mod = this.randint(1, 10) + this.randint(1, 4);
                    character.base_weight = 110
                    character.weight_mod = character.height_mod * (this.randint(1, 4) + this.randint(1, 4)) 
                }
                character.total_height = character.base_height + character.height_mod;
                character.total_weight = character.base_weight + character.weight_mod;
            }

            featurelib = [
                "Distinctive Jewelry","Piercings","Flamboyant or Outlandish Clothes","Formal, Clean Clothes","Ragged, Dirty Clothes", "Pronounced Scar","Missing Teeth","Missing Fingers","Unmatching Eye Color","Tattos","Birthmark","Braided Hair or Beard", "Naturally Highlighted Hair","Nervous Eye Twitch","Distinctive Nose","Rigid Posture","Crooked Posture","Exceptionally Beautiful", "Exceptionally Ugly"
            ]
            character.feature_one = featurelib[Math.floor(Math.random() * featurelib.length)]
            character.feature_two = featurelib[Math.floor(Math.random() * featurelib.length)]
            while (character.feature_two == character.feature_one || (character.feature_one.includes("Clothes") && character.feature_two.includes("Clothes")) || (character.feature_one.includes("Exceptionally") && character.feature_two.includes("Exceptionally"))) {
                character.feature_two = featurelib[Math.floor(Math.random() * featurelib.length)]
            }

            talentlib = [
                "Plays a musical instrument","Speaks several languages fluently","Unbelievably Lucky","Perfect memory","Great with animals", "Great with children","Great at solving puzzles","Great at one game","Great at impersonations","Draws beautifully", "Paints beautifully","Sings beautifully","Drinks everyone under the table","Expert Carpenter","Expert Cook", "Expert Dart Thrower","Expert Rock Skipper","Expert Juggler","Skilled Actor","Master of Disguise","Skilled Dancer", "Knows thieves' cant"
            ]
            character.talent = talentlib[Math.floor(Math.random() * talentlib.length)]

            mannerismlib = [
                "Prone to singing quietly"," Prone to whistling quietly","Prone to humming quietly","Speaks in rhymes or other peculiar way", "Particularly high voice","Particularly low voice","Slurs words","Has a lisp","Stutters","Enunciates overly clearly", "Speaks loudly","Whispers","Uses flowery speech or long words","Frequently uses the wrong word", "Uses colorful oaths and exclamations","Makes constant jokes or puns","Prone to predictions of doom","Fidgets","Squints", "Stares into distance","Chews something","Paces","Taps fingers","Bites fingernails","Twirls hair or tugs beard"
            ]
            character.mannerism = mannerismlib[Math.floor(Math.random() * mannerismlib.length)]

            traitlib = [
                "Argumentative","Arrogant","Blustering","Rude","Curious","Friendly","Honest","Hot Tempered","Irritable","Ponderous","Quiet", "Suspicious"
            ]
            character.trait = traitlib[Math.floor(Math.random() * traitlib.length)]

            if (Math.random() < this.unaligned_probability / 100) {
                character.alignment = "Unaligned"
            } else {
                ge_good_prob = this.ge_good_weight / (this.ge_good_weight + this.ge_neutral_weight + this.ge_evil_weight)
                ge_neutral_prob = this.ge_neutral_weight / (this.ge_good_weight + this.ge_neutral_weight + this.ge_evil_weight)
                ge_evil_prob = this.ge_evil_weight / (this.ge_good_weight + this.ge_neutral_weight + this.ge_evil_weight)

                lc_lawful_prob = this.lc_lawful_weight / (this.lc_lawful_weight + this.lc_neutral_weight + this.lc_chaotic_weight)
                lc_neutral_prob = this.lc_neutral_weight / (this.lc_lawful_weight + this.lc_neutral_weight + this.lc_chaotic_weight)
                lc_chaotic_prob = this.lc_chaotic_weight / (this.lc_lawful_weight + this.lc_neutral_weight + this.lc_chaotic_weight)

                character.aligment = ""
                lawful_chaotic = Math.random()
                if(lawful_chaotic <= lc_lawful_prob) {
                    character.alignment = "Lawful"
                } else if (lawful_chaotic <= lc_lawful_prob + lc_neutral_prob) {
                    character.alignment = "Neutral"
                } else {
                    character.alignment = "Chaotic"
                }
                good_evil = Math.random()
                if (good_evil <= ge_good_prob) {
                    character.alignment += " Good"
                } else if (good_evil <= ge_good_prob + ge_neutral_prob) {
                    character.alignment += " Neutral"
                } else {
                    character.alignment += " Evil"
                }
                if (character.alignment == "Neutral Neutral") {
                    character.alignment = "True Neutral"
                }
                // console.log(character)
            }
            ideallib = ["Balance", "Knowledge", "Live and let live", "Moderation", "Neutrality", "People", "Aspiration", "Discovery", "Glory", "Nation", "Redemption", "Self-Knowledge"]
            if (character.alignment.includes("Good")) {
                ideallib.concat([
                    "Beauty", "Charity", "Greater Good", "Life", "Respect", "Self-Sacrifice"
                ])
            } else if (character.alignment.includes("Evil")) {
                ideallib.concat([
                    "Domination", "Greed", "Might", "Pain", "Retribution", "Slaughter"
                ])
            }
            if (character.alignment.includes("Lawful")) {
                ideallib.concat([
                    "Community", "Fairness", "Honor", "Logic", "Responsibility", "Tradition"
                ])
            } else if (character.alignment.includes("Chaotic")) {
                ideallib.concat([
                    "Change", "Creativity", "Freedom", "Independence", "No Limits", "Whimsy"
                ])
            }
            console.log(ideallib)
            character.ideal = ideallib[Math.floor(Math.random() * ideallib.length)]

            bondlib = [
                "Dedicated to fulfilling a personal life goal","Protective of close family members","Protective of colleagues or compatriots", "Loyal to a benefactor, patron, or employer","Captivated by a romantic interest","Drawn to a special place", "Protective of a sentimental keepsake","Protective of a valuable possession","Out for revenge"
            ]
            character.bond = bondlib[Math.floor(Math.random() * bondlib.length)]

            flawlib = [
                "Forbidden love","Romantic succeptibility","Enjoys decadent pleasures","Arrogance","Envies another creature's possessions", "Overpowering greed","Prone to rage","Has a powerful enemy","Specific phobia","Shameful or scandalous history", "Secret crime or misdeed","Possession of forbidden lore","Foolhardy bravery"
            ]
            character.flaw = flawlib[Math.floor(Math.random() * flawlib.length)]

            character.strength = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1
            character.dexterity = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1
            character.constitution = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1
            character.intelligence = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1
            character.wisdom = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1
            character.charisma = Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1 + Math.floor(Math.random() * 6) + 1

            character.statfeature = ""
            if (character.strength >= 13) {
                character.statfeature += "Powerful, Brawny, Strong as an Ox";
            }
            if (character.dexterity >= 13) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Lithe, Agile, Graceful"
            }
            if (character.constitution >= 13) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Hardy, Hale, Healthy"
            }
            if (character.intelligence >= 13) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Studious, Learned, Inquisitive"
            }
            if (character.wisdom >= 13) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Perceptive, Spiritual, Insightful"
            }
            if (character.charisma >= 13) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Persuasive, Forceful, Born Leader"
            }
            if (character.strength <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Feeble, Scrawny"
            }
            if (character.dexterity <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Clumsy, Fumbling"
            }
            if (character.constitution <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Sickly, Pale"
            }
            if (character.intelligence <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Dim-Witted, Slow"
            }
            if (character.wisdom <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Oblivious, Absentminded"
            }
            if (character.charisma <= 7) {
                if (character.statfeature.length > 0) {
                    character.statfeature += "; "
                }
                character.statfeature += "Dull, Boring"
            }

            this.displayed_character = character;
        },

        InitSSE () {
            window.addEventListener ("beforeunload", () => {
                if (this.nld_source) {
                    this.nld_source.close();
                }
                if (this.rpi_source) {
                    this.rpi_source.close()
                }
            })
        },

        nld_source: null,
        nld: "",
        RequestNLD () {
            let description = ""
            description += ` - ${character.sex != "Neither" ? character.sex : ""} ${character.race}`
            description += `\n - Height: ${Math.floor(character.total_height / 12 + 1)}' ${character.total_height % 12}"`
            description += `\n - Weight: ${character.total_weight}`
            description += `\n - ${character.feature_one}`
            description += `\n - ${character.feature_two}`
            description += `\n - Talent: ${character.talent}`
            description += `\n - Mannerism: ${character.mannerism}`
            description += `\n - Trait: ${character.trait}`
            for (let i = 0; i < character.statfeature.split("; ").length; i++) {
                description += `\n - ${character.statfeature.split("; ")[i]}`
            }
            description += `\n - Ideal: ${character.ideal}`
            description += `\n - Bond: ${character.bond}`
            description += `\n - Flaw: ${character.flaw}`

            processed = encodeURIComponent(description)

            this.nld_source = new EventSource(`/Tools/NPC-Gen/NLD?description=${processed}`)
            this.nld_source.onmessage = (event) => {
                this.nld = event.data;
            }
            this.nld_source.addEventListener("END", () => {
                this.StopNLD();
            })
        },
        StopNLD () {
            if (this.nld_source) {
                this.nld_source.close();
                this.nld_source = null;
            }
        },

        rpi_source: null,
        rpi: "",
        RequestRPI () {
            let description = ""
            description += ` - ${character.sex != "Neither" ? character.sex : ""} ${character.race}`
            description += ` - Name: ${character.full_name}`
            description += `\n - Height: ${Math.floor(character.total_height / 12 + 1)}' ${character.total_height % 12}"`
            description += `\n - Weight: ${character.total_weight}`
            description += `\n - ${character.feature_one}`
            description += `\n - ${character.feature_two}`
            description += `\n - Talent: ${character.talent}`
            description += `\n - Mannerism: ${character.mannerism}`
            description += `\n - Trait: ${character.trait}`
            for (let i = 0; i < character.statfeature.split("; ").length; i++) {
                description += `\n - ${character.statfeature.split("; ")[i]}`
            }
            description += `\n - Ideal: ${character.ideal}`
            description += `\n - Bond: ${character.bond}`
            description += `\n - Flaw: ${character.flaw}`

            processed = encodeURIComponent(description)

            this.rpi_source = new EventSource(`/Tools/NPC-Gen/RPI?description=${processed}`)
            this.rpi_source.onmessage = (event) => {
                this.rpi = event.data;
            }
            this.nld_source.addEventListener("END", () => {
                this.stopRPI();
            })
        },
        StopRPI () {
            if (this.rpi_source) {
                this.rpi_source.close();
                this.rpi_source = null;
            }
        }
    }))
})
