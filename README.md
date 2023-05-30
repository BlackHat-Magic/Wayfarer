# Wayfinder

A website used to store rulesets for tabletop roleplaying games. Primarily designed for 5th edition Dungeons and Dragons.

Powered by AlpineJS, ShowdownJS, and Flask.
Licensed under AGPL-v3.0

## Todo list

In no particular order...

 - [ ] finish website
 - [ ] make mobile site less unusable
 - [ ] make website pretty
 - [ ] add animations
 - [x] ~~clean up CSS file~~
 - [X] ~~add edit functionality~~
 - [X] ~~add duplication functionality~~
 - [x] ~~fix Races page~~
 - [x] ~~make background filters more useful~~
 - [ ] Add JSON import/export functionality
     - [ ] Export Functionality
     - [X] ~~Import races~~
     - [X] ~~Import backgrounds~~
     - [X] ~~Import feats~~
     - [ ] Import classes (will likely never be fully supported; partial support is planned)
     - [X] ~~Import actions~~
     - [X] ~~Import conditions, diseases, and statuses~~
     - [ ] Import items
         - [X] ~~Import item details~~
         - [ ] More comprehensive item type importing
     - [X] ~~Import languages~~
     - [X] ~~Import spells~~
     - [X] ~~Import skills~~
     - [ ] Import Entire Rulesets
     - [ ] Filter imported sources
 - [x] ~~Make races page work with custom ability scores~~
 - [x] ~~Add support for multiple administrator rulesets~~
 - [ ] Idiotproofing
     - [ ] Add instructions
     - [ ] Communicate unsupported data
     - [X] ~~Input validation for imported text~~
     - [ ] Validate pickles
     - [ ] Consolidate user content validation into a function
 - [ ] Make flash messages dismissable
 - [ ] Hyperlinks
     - [ ] Correctly parse and reformat 5e tools markup
 - [ ] Filter URLs
 - [ ] Cache unsaved database entries if user input is invalid
 - [ ] GM Tools (tables, traps, etc)
     - [ ] NPC Generator
     - [ ] Monster Maker
     - [ ] CR Calculator (Maybe)
     - [ ] Encounter Generator (Maybe)
     - [ ] Loot Generator (Maybe)
     - [ ] Initiative Tracker (Maybe)
 - [ ] Player Tools
     - [ ] Character sheets
     - [ ] Backstory Generator
     - [ ] Stat Calculator
     - [ ] Virtual Tabletop (Maybe)
 - [ ] Bulk content management tools
 - [ ] Legal/Privacy Mumbo Jumbo
     - [ ] DMCA stuff
     - [ ] Privacy Policy
     - [ ] CCPA/GDPR Right to be Forgotten
     - [ ] EULA
     - [ ] LibreJS support
     - [ ] Footer
 - [ ] Comment Code
 - [ ] Move the submit button on create/edit classes page to the bottom (this is less trivial than it sounds I swear)
 - [ ] Header Links
 - [ ] "Cantrip-level x"
 - [ ] Alert administrator of high ID collision probability
 - [ ] De-spaghettify import code (e.g. checking if item is list or dict can be more efficient)
 - [ ] Subdomain navigation
 - [ ] Images (find a host)
 - [ ] Better options for ruleset visibility

## Usage

Wayfinder assumes that the the first user is the administrator. **All rulesets created by the administrator account are public.** It is preferable that you be the only one who can access the site at this stage, to prevent someone else from potentially creating the administrator account. From here, you can add the rules and such for the default ruleset and begin using the site. Once the default ruleset and administrator account are set up, you can allow external connections to the site.

## Acknowledgements

This software is licensed under the GNU Affero General Public License Version 3.

It utilizes the following works licensed under different terms:

 - Alpine.js, licensed under the MIT License
 - Showdown.js, licensed under the MIT License