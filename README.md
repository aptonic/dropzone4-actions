# Dropzone 3 Actions

This repository contains a bunch of add-on actions that work with Dropzone 3. You can quick install most of these actions from a [list of featured](http://aptonic.com/dropzone3/actions) actions on our website [here](http://aptonic.com/dropzone3/actions) or alternatively you can clone this repository and double click on bundles to add them.

This repository works in conjunction with the [dropzone3-actions-zipped](https://github.com/aptonic/dropzone3-actions-zipped) repository which contains zipped versions of these actions (auto updated nightly). The zipped versions are better if you want to download only specific actions or need to provide a link to an action. The API documentation for Dropzone 3 is provided below.

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Introducing the Dropzone 3 API](#introducing-the-dropzone-3-api)
- [Developing an Action](#developing-an-action)
  - [Generated Template Action](#generated-template-action)
- [Copy and Edit an existing action](#copy-and-edit-an-existing-action)
- [Debug Console](#debug-console)
- [Customizing your Actions Icon](#customizing-your-actions-icon)
- [Action Metadata](#action-metadata)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introducing the Dropzone 3 API

![API Logo](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/dzbundle.png)

There have been big changes to the Dropzone API since Dropzone 2. Actions listed in this repository will only work with Dropzone 3. Dropzone 2 actions (.dropzone files) can still be added to Dropzone 3 but it's best if you install the [Bundle Script](http://aptonic.com/dropzone3/actions/install.php?bundle_name=Bundle%20Script) action from [here](http://aptonic.com/dropzone3/actions/install.php?bundle_name=Bundle%20Script) to convert old Dropzone 2 scripts into shiny new Dropzone 3 action bundles.

A Dropzone 3 action bundle is simply a directory with a .dzbundle extension. It must contain an action.rb script and an icon.png file that contains the default icon for the action. The bundle can also optionally contain other resources such as Ruby libraries or executables. The action.rb file must have certain metadata at the top. Dropzone parses this metadata when you add the action. 

## Developing an Action

The easiest way to develop a new Dropzone 3 action is to click the white plus in the top left of the grid and choose the 'Develop Action...' item. 

![Develop Action](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/develop-action.png)
<br>

This will bring up the 'Develop Action' dialog shown below which allows you to configure your action:

![Develop Dialog](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/develop-dialog.png)

The values entered here will be used to generate the metadata section at the top of action.rb. When you've chosen values appropriate for your action, click Create Action. This will open your default text editor with the newly generated action.rb file and add the action to your Dropzone grid. The generated action.rb file provides template code so you can easily get started. The template is given below.

### Generated Template Action

```ruby
# Dropzone Action Info
# Name: Custom Action
# Description: Describes what your action will do.
# Handles: Files
# Creator: Your name
# URL: http://yoursite.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  puts $items.inspect

  $dz.begin("Starting some task...")
  $dz.determinate(true)
  
  # Below lines tell Dropzone to update the progress bar display
  $dz.percent(10)
  sleep(1)
  $dz.percent(50)
  sleep(1)
  $dz.percent(100)
  
  # The below line tells Dropzone to end with a notification center notification with the text "Task Complete"
  $dz.finish("Task Complete")
  
  # You should always call $dz.url or $dz.text last in your script. The below $dz.text line places text on the clipboard.
  # If you don't want to place anything on the clipboard you should still call $dz.url(false)
  $dz.text("Here's some output which will be placed on the clipboard")
end
 
def clicked
  # This method gets called when a user clicks on your action
  $dz.finish("You clicked me!")
  $dz.url(false)
end
```

At the top of the file is the generated metadata. The purpose of each metadata option is described in the [Action Metadata](#action-metadata) section.

In the template action you will notice that two Ruby methods have been created for you. The dragged method is called by Dropzone when items are dragged onto your action and the clicked method is called when your action is clicked on in the grid.

## Copy and Edit an existing action

The other way you can create a new action is by right clicking on an existing action in the grid and clicking 'Copy and Edit Script' - This will duplicate the underlying action bundle as a new User Action and open the duplicated script for editing. This is useful if you want to create an action with a similar purpose to an existing action but with some modifications.

![Copy & Edit](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/copy-and-edit.png)

## Debug Console

The debug console makes it quick and easy to view the output and environment of your action. To open the debug console, click on the Settings gear in the top right of the Dropzone grid and click 'Debug Console' - you can also open it by first clicking the Dropzone menu item so Dropzone gets keyboard focus and then press Cmd+Shift+D

![Open Debug Console](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/open-debug-console.png)

![Debug Console](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/debug-console.png)

The screenshot above shows the output in the debug console after dropping two files onto the template action (the code for this is given in the [above section](#generated-template-action)). When a task is run, Dropzone creates a task description file that contains all the needed info to start the task. The runner.rb Ruby script (located inside the Dropzone.app application bundle at /Contents/Actions/lib/runner.rb) then reads this task description file, sets environment variables and then calls the appropriate method in your action.rb script.

## Customizing your Actions Icon

There needs to be an icon.png file inside your action bundle. This icon is used as the default action icon when your action is added to the grid. This icon should ideally be at least 300x300px in size. The maximum size action icons can be displayed in the grid is 150x150 but when in retina display modes this is doubled to 300x300. You can change the icon for your action by going into the Dropzone preferences, opening the User Actions tab and clicking the Reveal button to show your Action bundle in the Finder. You then right click the bundle and click 'Show Package Contents' and drag a new icon.png into the bundle. This is illustrated below:

![Reveal](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/reveal.png)
<br>
![Show Package Contents](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/show-package-contents.png)
<br><br><br>
![Replace Icon](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/replace-icon.png)

## Action Metadata

At the top of your action.rb file is the metadata section that was generated when you clicked 'Create Action'

The metadata block must begin with the line:
```ruby
# Dropzone Action Info
```
And this must be the first thing at the top of the file.

All recognised metadata options are described below:

<table>
	<th width="240">
		Field
	</th>
	<th>
		Explanation
	</th>
	<th width="100">
		Required
	</th>
	<tr>
		<td>Name</td>
		<td>Provides the name for your action.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>Description</td>
		<td>Describes what your action does.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>Handles</td>
		<td>Can be either "Files" or "Text" or "Files, Text" to handle both files and text.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>Events</td>
		<td>Can be either "Dragged" or "Clicked" or "Dragged, Clicked" to handle both clicks and drags.<br/>
			If not specified then defaults to handling both clicks and drags.</td>
		<td>No</td>
	</tr>
	<tr>
		<td>Creator</td>
		<td>Your name or company which will be shown when adding the action.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>URL</td>
		<td>Your URL which will be shown and linked to when adding the action.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>OptionsNIB</td>
		<td>A optional configuration panel that can be shown when adding the action to collect needed info such as a username, password or API key<br/>
			Currently available OptionsNIBs are: Login, ExtendedLogin, APIKey, UsernameAPIKey, ChooseFolder and ChooseApplication<br/>
			See the OptionsNIBs section further down for an explanation of how to use these.</td>
		<td>No</td>
	</tr>
	<tr>
		<td>SkipConfig</td>
		<td>If your action doesn't use an OptionsNIB then it's best to set this to Yes. It makes your action get added directly to the grid without showing the configuration panel first. The configuration panel is shown by default if this option is not specified.</td>
		<td>No</td>
	</tr>
	<tr>
		<td>RunsSandboxed</td>
		<td>If your action does things that are incompatible with OS X sandboxing (such as running AppleScript or writing to arbitrary directories) then set this to No. Users of the non-Mac App Store version of Dropzone 3 will be able to run your action as normal but users of the Mac App Store version of Dropzone 3 will be prompted to install a special helper app that runs your action unsandboxed on behalf of the parent app.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>Version</td>
		<td>The version number of your action. Dropzone uses this to see if a newer version of your action is available and if it is then it prompts the user to upgrade. Increment this before sending a pull request to this repository with your latest action.</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td>MinDropzoneVersion</td>
		<td>As Dropzone gets updated new API and features will be added so you may need to specify a minimum compatible version of Dropzone that your action works with. The user will be prompted to update Dropzone if they are using a version behind what your action supports. You can leave this out or set it to 3.0 initially.</td>
		<td>No</td>
	</tr>
	<tr>
		<td>KeyModifiers</td>
		<td>A comma separated list of key modifiers your action supports. When the user drags a file onto your action they can hold a particular modifier key including Command, Option, Control or Shift. The held modifier will be passed to your script in the ENV['KEY_MODIFIERS'] variable and you can modify the behaviour of your action based on the held key. A example of valid values for this field would be "Option" or "Command, Option, Control, Shift" (without quotes).</td>
		<td>No</td>
	</tr>
	<tr>
		<td>LoginTitle</td>
		<td>The Login, APIKey and UsernameAPIKey OptionsNIBs allow you to specify an optional title above the fields. You can provide a string for this such as "Service Login Details". If not specified then it defaults to 'Login Details'</td>
		<td>No</td>
	</tr>
	<tr>
		<td>UseSelectedItemNameAndIcon</td>
		<td>If your action uses the ChooseFolder OptionsNIB then this specifies whether you want the label and icon to be set to the chosen folders after selecting the folder. Defaults to No.</td>
		<td>No</td>
	</tr>
</table>