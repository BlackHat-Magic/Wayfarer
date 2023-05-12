# Wayfinder

A website used to store rulesets for tabletop roleplaying games. Primarily designed for 5th edition Dungeons and Dragons. On paper, storing rulesets for almost any TTRPG should be possible with minimal changes to the website.

Powered by AlpineJS, ShowdownJS, and Flask.
Licensed under AGPL-v3.0

## Todo list

In no particular order...

 - [ ] finish website
 - [ ] make mobile site less unusable
 - [ ] make website pretty
 - [ ] add CSS animations
 - [x] ~~clean up CSS file~~
 - [X] ~~add edit functionality~~
 - [X] ~~add duplication functionality~~
 - [x] ~~fix Races page~~
 - [x] ~~make background filters more useful~~
 - [ ] Add 5e.tools import/export functionality
     - [ ] Export Functionality
     - [ ] Import variant backgrounds
     - [ ] Import items
         - [X] ~~Import item details~~
         - [ ] More comprehensive item type importing
     - [ ] Import classes (will likely never be fully supported)
     - [ ] Import Entire Rulesets
 - [x] Make races page work with custom ability scores
 - [x] ~~Add support for multiple administrator rulesets~~
 - [ ] Idiotproofing
     - [ ] Add instructions
     - [ ] Communicate unsupported data
     - [ ] Input validation for imported text
 - [ ] Make flash messages dismissable
 - [ ] Item property and type templates
 - [ ] Hyperlinks
     - [ ] Correctly parse and reformat 5e tools markup
 - [ ] Filter URLs
 - [ ] Cache unsaved database entries if user input is invalid
 - [ ] GM Tools (tables, traps, etc)

## Usage

Wayfinder assumes that the the first user is the administrator. **All rulesets created by the administrator account are public.** It is preferable that you be the only one who can access the site at this stage, to prevent someone else from potentially creating the administrator account. From here, you can add the rules and such for the default ruleset and begin using the site. Once the default ruleset and administrator account are set up, you can allow external connections to the site.

## Acknowledgements

This software is licensed under the GNU Affero General Public License Version 3.

It utilizes the following works licensed under different terms:

 - Alpine.js, licensed under the MIT License
 - Showdown.js, licensed under the MIT License