# 2ché

A very light layer on top of [Nina Stoessinger's Touche tool](https://github.com/ninastoessinger/Touche). This layer adds some additional keyboard shortcuts to the tool, making it a bit easier to navigate the clashing pairs list, and apply kerning changes without needing to touch the mouse. Sorry for the silly name.

Our modification changes Touche into a Windowed Plugin that retains focus while you're using it. As you click (or use arrow keys) to navigate the list of clashes, you can also kern the clashing pairs directly while the Touche window keeps focus. This allows you to seamlessly navighate the clash list while fixing clashes without needing to use the mouse.

Here's a list of the keyboard shorcuts 2che provides.

| action | key |
| ------ | --- |
| next clashing pair | `↓` |
| previous clashing pair | `↑` |
| increase kerning by default low increment | `→ ` |
| decrease kerning by default low increment | `←` |
| increase kerning by default high increment | `⌘` + `→ ` |
| decrease kerning by default high increment | `⌘` + `←` |

## Original Notes from Nina Stoessinger and Glyphs

Looking through your kerning, you try to catch them: _colliding glyph pairs_. But did you remember to check your i-diacritics against your superior numerals, ogoneks against brackets, the dcaron against the asterisk? Touché can take some guesswork out of things by listing the pairs whose black bodies touch, taking spacing and kerning into account.

![Touché RoboFont](/screenshotRoboFont.png)

Touché makes no assumptions about the relevance of pairs, or which ones need fixing; and it does not change your data. Among the specified set of input glyphs, *Touché checks all of your glyphs against all of your glyphs*, lists and shows the touching pairs that it finds, and leaves the decision on whether and how to fix them up to you. The resulting pairs can be exported as a text file that can directly be used as a pair list in Metrics Machine. (It should go without saying that this can supplement and perhaps expedite, but in no way replace careful manual checking of kerning in general.)

Up now is version 1.2 with a rewritten collision routine (thanks to Frederik Berlaen) that is much faster and more reliable than my previous version. Still, if you’re checking large numbers of glyphs, it can take a couple of minutes. You can also just check a subsection of glyphs, which should then be significantly faster.

![Touché Glyphs](/screenshotGlyphs.png)

It needs the latest version of Glyphs2 and please update the robofab wrapper (objectsGS and GSPen) from https://github.com/schriftgestalt/Glyphs-Scripts
