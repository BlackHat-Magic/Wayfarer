# Wayfarer

A website used to store rulesets for tabletop roleplaying games. Primarily designed for 5th edition Dungeons and Dragons.

Powered by AlpineJS, ShowdownJS, and Flask.
Licensed under AGPL-v3.0

## Todo list

In no particular order...

 - [ ] finish website
 - [ ] make mobile site less unusable
 - [ ] make website pretty
 - [ ] add animations
 - [ ] Payment Processing
 - [ ] Add JSON import/export functionality
     - [X] ~~Export Functionality~~
     - [X] ~~Import Functionality~~
     - [ ] Import Entire Rulesets
     - [ ] Export Entire Rulesets
 - [ ] Idiotproofing
     - [ ] Add instructions
     - [ ] Communicate unsupported data
     - [X] ~~Input validation for imported text~~
     - [ ] Validate pickles
     - [ ] Consolidate user content validation into a function
 - [X] ~~Make flash messages dismissable~~
 - [ ] Hyperlinks
     - [ ] Correctly parse and reformat 5e tools markup
 - [X] ~~URL Parameters/Header URLs~~
 - [ ] Cache unsaved database entries if user input is invalid
     - [ ] Disabled Buttons
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
     - [X] ~~Footer~~
     - [ ] Make site work without JS
 - [ ] Code Cleanup
     - [ ] Comment Code
     - [X] ~~Move the submit button on create/edit classes page to the bottom (this is less trivial than it sounds I swear)~~
     - [X] ~~De-spaghettify import code~~
     - [ ] dict keys
     - [ ] comprehension
     - [ ] dict.get() instead of if in dict.keys()
 - [ ] "Cantrip-level x"
 - [ ] Alert administrator of high ID collision probability
 - [ ] Site administration panel
 - [ ] Images (find a host)
 - [ ] Inventory Slots
 - [ ] Custom Data (Pickle)
 - [ ] Container info
 - [ ] Remove Strength, Dexterity, Etc from items
 - [ ] Hover tooltips

## Usage

Wayfarer assumes that the the first user is the administrator. **All rulesets created by the administrator account are public.** It is preferable that you be the only one who can access the site at this stage, to prevent someone else from potentially creating the administrator account. From here, you can add the rules and such for the default ruleset and begin using the site. Once the default ruleset and administrator account are set up, you can allow external connections to the site.

## Acknowledgements

This software is licensed under the GNU Affero General Public License Version 3.

It utilizes the following works licensed under different terms:

 - Alpine.js, licensed under the MIT License
 - Showdown.js, licensed under the MIT License