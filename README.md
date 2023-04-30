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
     - [X] ~~Import race features~~
     - [X] ~~Import race flavor text~~
     - [ ] Import background features
     - [ ] Import background flavor text
     - [ ] Import feats
     - [ ] Import classes
     - [ ] Import actions
     - [ ] Import items
     - [ ] Import languages
     - [ ] Import spells
     - [ ] Import recipes
     - [X] ~~Import skills~~
     - [ ] Import tables and other non-plaintext features/flavor
     - [ ] Import Entire Rulesets
     - [ ] Correctly parse and reformat 5e tools markup
 - [ ] Make races page work with custom ability scores
 - [ ] Improve race ASI filtering
 - [x] ~~Add support for multiple administrator rulesets~~
 - [ ] Add armor stealth disadvantage
 - [ ] Add armor strength minimum
 - [ ] Idiotproofing
     - [ ] Add instructions
 - [ ] Make flash messages dismissable
 - [ ] Item property and type templates
 - [ ] Hyperlinks

## Usage

Clone the repository.

```git clone https://github.com/BlackHat-Magic/Wayfinder```

Install dependencies.

```pip install requirements.txt```

Deploy website.

```I actually forgot how to deploy a production flask application. Just google it.```

Wayfinder assumes that the the first user is the administrator. **All rulesets created by the administrator account are public.** It is preferable that you be the only one who can access the site at this stage, to prevent someone else from potentially creating the administrator account. From here, you can add the rules and such for the default ruleset and begin using the site. Once the default ruleset and administrator account are set up, you can allow external connections to the site.

## Acknowledgements

This software is licensed under the GNU Affero General Public License Version 3.

It utilizes the following works licensed under different terms:

 - Alpine.js, licensed under the MIT License
 - Showdown.js, licensed under the MIT License