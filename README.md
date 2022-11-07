# Wayfinder

A website used to store rulesets for tabletop roleplaying games. Primarily designed for 5h edition Dungeons and Dragons. On paper, storing rulesets for almost any TTRPG should be possible with minimal changes to the website.

Powered by AlpineJS, ShowdownJS, and Flask.
Licensed under AGPL-v3.0

## Todo list

In no particular order...

 - finish website
 - make mobile site less trash
 - make website pretty
 - add CSS animations
 - clean up CSS file
 - add edit functionality
 - add duplication functionality
 - unfuck Races page

## Usage

Clone the repository.

```git clone https://github.com/BlackHat-Magic/Wayfinder```

Install dependencies.

```pip install requirements.txt```

Deploy website. Ideally ensure that it is not publicly-facing yet (we'll get to why in a minute).

```I actually forgot how to deploy a production flask application. Just google it.```

Wayfinder assumes that the user with ID 1 is the administrator account. It also assumes that the ruleset with ID 1 is the one that unauthenticated users will see. In the top bar, where users change which ruleset they are viewing, this is called "5e SRD" by default. I might change this in the future, but I'm lazy, it's not that hard for you to change it yourself manually anyway, and this repo isn't really intended to be used by other people anyway, I just thought that would be a nice feature to include, so usability isn't at the top of my priority list.

Anyway, you'll want to create a user account with ID 1 to be used as the administrator account, and create a ruleset with ID 1 to be used as the default ruleset. Whichever ruleset and user are created first are the ones with ID 1, hence why it is preferable that you be the only one who can access the site at this stage. From here, you can add the rules and such for the default ruleset and begin using the site. Once the default ruleset and administrator account are set up, you can allow external connections to the site.
