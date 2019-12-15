# OctoPrint-PrusaLevelingGuide

**Start here**
[Bed Leveling without Wave Springs](https://github.com/PrusaOwners/prusaowners/wiki/Bed_Leveling_without_Wave_Springs)

**IMPORTANT:** The guide mentions a firmware modification for modifying the G81 response to use relative values.  This plugin only works if you **do not** use this modification.  This plugin will calculate the relative values for you.

This plugin is to help guide you through the fine adjustments of the nylock bed leveling method for Prusa MK3 printers, which is described in the above guide.  Make sure you start there and already have the nylocks applied to your bed before beginning.  This plugin allows you to select a profile for preheating, then begin adjustment.  For each round of adjustment, the plugin will send the configured mesh level code and gcode for retrieving values (generally G80; G81).  Once values are received, you can view how to adjust your bed in a number of ways.  You click continue to proceed with another round of leveling or click finish to finish up.

*TODO: Allow configuration of a 'target bed variance' and alert whenever the bed is higher than the target variance - will only work if you configure your print start/print finish gcode to include G81*

You have the option of viewing the values in a table view or overlayed on a photo of the heatbed.  You can also customize whether you view raw values, degrees, decimal turns, or factional turns.

**Table View**
![Table view](table.png)


**Bed View**
![Bed view](bed.png)

## Inspirations

- [Bed Leveling without Wave Springs](https://github.com/PrusaOwners/prusaowners/wiki/Bed_Leveling_without_Wave_Springs) obviously I would not have written this plugin without this awesome mod/guide
- [OctoPrint-PrusaMeshMap](https://github.com/PrusaOwners/OctoPrint-PrusaMeshMap) This is the plugin I used previously to adjust my bed.  It works, but I wanted something a little more automated.  Some of the code for detecting g81 response was used from this plugin.
- [g81_level_guide](https://gitlab.com/gnat.org/g81_level_guide) I like the idea of this script because it automates the process, but I didn't like that it clears my preheat when connecting and that it was a pain to get running on a pi.  The idea inspired me to write this plugin.
- [g81_relative](https://github.com/pcboy/g81_relative) This is the site I originally used for converting my g81 values to relative numbers.  This is what inspired me to add all the different calculation types.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/scottrini/OctoPrint-PrusaLevelingGuide/archive/master.zip


## Configuration

The configuration tab allows you to customize the gcode for mesh leveling similar to the PrusaMeshMap plugin.

![Configuration](settings.png)

## G81 Output Handler

Just like the PrusaMeshMap plugin, this plugin has a handler that is watching output received from the printer **at all times**. This means you can place a G81 in octoprint's or your slicer's start or stop gcode and the plugin will update its values after every print.

## Adjusting your bed

Once your nylocks are on your bed and you're ready to adjust using this plugin, pull up the tab in your octoprint instance.  Decide if you want to preheat the bed while making adjustments.  Preheating isn't absolutely necessary for your initial adjustments, but really fine tuning the bed should be done preheated, as the values will change when things are heated.

So select your profile and whether to preheat, then click begin adjusting.  The plugin will:
- Preheat (if enabled)
- Send the mesh level command and G81 to retrieve results
- Wait for the command to complete
- Send gcode to move the bed and extruder out of the way
- Update the UI with the values

Once the UI is updated, the status will change to *Waiting for continue*.  This is your opportunity to adjust the screws.  The raw value view does not provide the direction to turn the screws.  If it's a negative value, loosen the screw.  If it's positive, tighten the screw.

All of the other views will disable an arrow next to the value to show which direction to rotate the screw.  Once you've made your adjustments, click continue to start another mesh check and update the UI with the new values.  If you've gotten your bed to a variance you're happy with, click **Finished**.  If the printer was preheated, this will disable the preheating.