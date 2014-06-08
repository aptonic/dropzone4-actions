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
- [Dragged Types](#dragged-types)
- [Providing Status Updates](#providing-status-updates)
  - [$dz.begin(message)](#dzbeginmessage)
  - [$dz.determinate(value)](#dzdeterminatevalue)
  - [$dz.percent(value)](#dzpercentvalue)
  - [$dz.finish(message)](#dzfinishmessage)
  - [$dz.url(url, title)](#dzurlurl-title)
  - [$dz.text(text)](#dztexttext)
  - [$dz.fail(message)](#dzfailmessage)
- [Showing Alerts and Errors](#showing-alerts-and-errors)
  - [$dz.alert(title, message)](#dzalerttitle-message)
  - [$dz.error(title, message)](#dzerrortitle-message)
- [CocoaDialog](#cocoadialog)
- [Saving and loading values](#saving-and-loading-values)
- [Temporary folder](#temporary-folder)
- [Bundling Ruby libs and executables](#bundling-ruby-libs-and-executables)
- [Customizing your actions icon](#customizing-your-actions-icon)
- [Action Metadata](#action-metadata)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introducing the Dropzone 3 API

![API Logo](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/dzbundle.png)

The general idea of a Dropzone action is that files or text will be dropped on the action and then the action will perform some useful function on the dropped items. This might be uploading the dropped files to a web service, renaming files, resizing images, zipping files etc. The possible uses are really only limited by your imagination. A Dropzone action also accepts a click event so when you click on it in the Dropzone grid it does something: Dor example the [Finder Path](https://aptonic.com/dropzone3/actions/install.php?bundle_name=Finder%20Path) action copies the currently selected item path in Finder to the clipboard. The API outlined below describes how you can easily develop your own actions to use with Dropzone and then share them with others. Dropzone actions are developed in Ruby so it's a good idea to learn a little Ruby first if you haven't coded in it before. There's an excellent introduction to the Ruby language at [http://www.codecademy.com/tracks/ruby]

There have been big changes to the Dropzone API since Dropzone 2. Actions listed in this repository will only work with Dropzone 3. Dropzone 2 actions (.dropzone files) can still be added to Dropzone 3 but it's best if you install the [Bundle Script](http://aptonic.com/dropzone3/actions/install.php?bundle_name=Bundle%20Script) action from [here](http://aptonic.com/dropzone3/actions/install.php?bundle_name=Bundle%20Script) to convert old Dropzone 2 scripts into updated Dropzone 3 action bundles.

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

### Copy and Edit an existing action

The other way you can develop a new action is by right clicking on an existing action in the grid and clicking 'Copy and Edit Script' - This will duplicate the underlying action bundle as a new User Action and open the duplicated script for editing. This is useful if you want to create an action with a similar purpose to an existing action but with some modifications.

![Copy & Edit](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/copy-and-edit.png)

## Debug Console

The debug console makes it quick and easy to view the output and environment of your action. To open the debug console, click on the Settings gear in the top right of the Dropzone grid and click 'Debug Console' - you can also open it by first clicking the Dropzone menu item so Dropzone gets keyboard focus and then press Cmd+Shift+D

![Open Debug Console](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/open-debug-console.png)

![Debug Console](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/debug-console.png)

The screenshot above shows the debug console after dropping two files onto the template action (the code for this is given in the [above section](#generated-template-action)). When a task is run, Dropzone creates a task description file that contains all the needed info to start the task. The runner.rb Ruby script (located inside the Dropzone.app application bundle at /Contents/Actions/lib/runner.rb) then reads this task description file, sets environment variables and then calls the appropriate method in your action.rb script. The task description file contents are output in the debug console when running a task.

In the above example, the task description file contents were:

```ruby
ACTION: "/Users/john/Library/Application Support/Dropzone 3/Actions/Custom Action.dzbundle"
EVENT: "dragged"
VARIABLE: "support_folder" "/Users/john/Library/Application Support/Dropzone 3"
VARIABLE: "dragged_type" "files"
ITEMS: "/Users/john/Desktop/Test2.jpeg" "/Users/john/Desktop/Test.jpeg"
```

The ACTION and EVENT fields are used by runner.rb to determine which action bundle to use and which method to call in your script. The VARIABLE fields can be accessed in your script using the ENV['variable_name'] global.

Note that output that was recognized and processed by Dropzone is shown in black (this is output that was generated from calling the $dz methods) while unrecognized output is shown in red. This is useful when debugging your script as if you use puts to output something for debugging purposes you can easily see it. Also, if your action causes a Ruby exception then the debug console will be shown automatically and the backtrace will be shown in red so you can fix the issue.

Clicking on the Edit Last button will open the last run action script in your text editor and clicking Rerun Last runs the last run task again with the same items, drag type and variables. This makes developing and debugging actions faster and easier.

## Dragged Types

If your action supports the dragged event, then you must specify the types of content your action can handle in the metadata as follows:

**Handle files only**
```ruby
# Handles: Files
```

**Handle strings of text only**
```ruby
# Handles: Text
```

**Handle both files and strings of text**
```ruby
# Handles: Files, Text
```

If you specify files then the user will only be allowed to drag files onto your action. If you specify text then the user will only be allowed to drag strings of text onto your action.
If you specify both types, then either type may be dragged and your action will need to determine the type as follows:

```ruby
case ENV['dragged_type']
  when 'files'
  # Code to handle dragged files goes here
  # $items is an array of the dragged filenames
  when 'text'
  # Code to handle dragged text goes here
  # $items[0] is the dragged string of text
end
```

## Providing Status Updates

Your action can optionally call API methods to provide status updates to Dropzone so that the user can monitor the progress of your action using the in grid progress bars and text - For example if your action uploaded data to a server then you can call the below methods to inform the user about the progression of the upload. You can provide these status updates by calling methods on the $dz global which is an instance of the Dropzone class. This global is setup for you when Dropzone calls your script. The methods for providing status updates from your script are outlined below:

### $dz.begin(message)

Tells Dropzone to show a new task status progress bar in the grid and to set the label above the progress bar to the specified message.
You can call this method multiple times as your action runs to update the displayed text.

**Example**

```ruby
$dz.begin("Running task...")
```

### $dz.determinate(value)

Value may be either true or false. Determinate mode (true) indicates that you will be providing progress information to Dropzone from your script as a percent and indeterminate mode (false) means that no progress information will be provided.

You can switch between determinate and indeterminate modes as your script executes. For example, you might choose to resize some images and then upload them to a server - you may not be able to provide progress information as the images are resized, but you can provide progress information while uploading them to a server. Therefore you would tell Dropzone to use indeterminate mode initially and then switch to determinate mode once you begin uploading. You should use determinate mode and provide progress information when possible.

**Examples**

```ruby
$dz.begin("Running task...")
$dz.determinate(false)
```

![Determinate False](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/determinate-false.png)

```ruby
$dz.begin("Running task...")
$dz.determinate(true)
$dz.percent(50)
```

![Determinate False](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/determinate-true.png)

### $dz.percent(value)

Value is an integer value between 0 and 100. Dropzone updates the task progress bar to reflect this value.
You only need to call this method when in determinate mode.

**Example**

```ruby
$dz.percent(50)
```

### $dz.finish(message)

Shows a notification center notification that the task is finishing with the given message. To actually end the task and remove the task status bar from the grid you have to call $dz.url after this.

**Example**

```ruby
$dz.finish("Task Complete")
```

![Finish Notification](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/finish-notification.png)

### $dz.url(url, title)

Sets a URL to be placed on the pasteboard. This is useful for writing actions that result in content being made available at a URL so a user can quickly paste the URL into other applications. You can optionally provide a title for the URL that will be shown in the Recently Shared popup menu. If you don't specify a title then the first dragged filename will be used or the truncated text if text was dragged.

If you do not wish to specify a URL, you must still call this method with false as the argument. Calling this method causes the task status bar to be removed from the grid and the task resources to be cleaned up. You should only call this method once and it should be the last method your action calls. 

**Examples**

The following would result in the URL http://aptonic.com being placed on the pasteboard:

```ruby
$dz.url("http://aptonic.com")
```

You can use the following if you do not wish to provide a URL:

```ruby
$dz.url(false)
```

You can optionally provide a title for the URL for the Recently Shared popup menu:
```ruby
$dz.url("http://aptonic.com", "Aptonic")
```

### $dz.text(text)

You can use this in place of $dz.url. It behaves exactly the same except that it does not attempt to encode the argument as a URL so you can place raw strings of text on the pasteboard.

**Example**

The following would result in the raw string 'This is a test string that will not be URL encoded' being placed on the pasteboard:

```ruby
$dz.text("This is a test string that will not be URL encoded")
```

### $dz.fail(message)

Shows a notification center notification that the task failed. Also terminates the task and makes a cross show in the status item to indicate task failure. If you call this you don't need to call $dz.url or $dz.text after.

**Example**

```ruby
$dz.fail("Error uploading file")
```

![Failed Notification](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/fail-notification.png)

## Showing Alerts and Errors

### $dz.alert(title, message)

Shows a popup alert box with the given title and message.

**Example**

```ruby
$dz.alert("Alert Title", "Some informative text...")
```

![Alert](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/alert.png)

### $dz.error(title, message)

Shows a popup error box with the given title and message.

**Example**

```ruby
$dz.error("Error Title", "An error occurred...")
```

![Error](https://raw.githubusercontent.com/aptonic/dropzone3-actions/master/docs/error.png)

Note that calling $dz.error results in your script terminating immediately while calling $dz.alert allows you to display a message and then continue execution of your script.

## CocoaDialog

CocoaDialog is an application bundled with Dropzone that allows the use of common UI controls such as file selectors, text input, yes/no confirmations and more. You can learn more about how to use CocoaDialog [here.](http://mstratman.github.io/cocoadialog/#documentation) CocoaDialog has many possible uses in a Dropzone action, for example, the 'Save Text' action that ships with Dropzone uses CocoaDialog to popup a dialog box to get the desired filename.

You can launch CocoaDialog by calling $dz.cocoa_dialog(arguments) where arguments is a string with the arguments to be passed to the CocoaDialog command line tool.

**Examples**

The below example prompts the user for a filename and outputs the entered filename to the debug console. It also handles the case where the user clicks the cancel button:

```ruby
output = $dz.cocoa_dialog('standard-inputbox --title "Save to File" --e --informative-text "Enter Filename:"')
button, filename = output.split("\n")

$dz.fail("Cancelled") if button == "2"

puts filename
```

The below example gets a yes or no answer from the user and then outputs the result to the debug console:

```ruby
output = $dz.cocoa_dialog('yesno-msgbox --no-cancel --text "Are you sure you want to delete this file?"')
if output == "1\n"
  puts "Yes was clicked" 
else
  puts "No was clicked"
end
```

## Saving and loading values

Your action can store string values in the Dropzone database by calling $dz.save_value(value_name, value). This is useful for storing configuration for your action - e.g. when your action first runs you could use CocoaDialog to prompt for a setting and then store the result. When your action is next run, all saved values are set as environment variables and can be accessed using ENV['stored_value_name']. You can see which variables were set in the [debug console](#debug-console) each time your action is run. If the user has multiple instances of your action setup in the grid, the stored values are unique to each instance.

Example

Saving the value:

```ruby
$dz.save_value('username', 'john')
```

Outputting the saved value to the debug console:

```ruby
puts ENV['username']
```

## Temporary folder

If your action needs to store files in a temporary location you can use $dz.temp_folder to get return a path that is writeable by both the sandboxed and unsandboxed versions of Dropzone.

Example

```ruby
puts $dz.temp_folder
```

Would output /Users/john/Library/Application Support/Dropzone 3/Temp to the debug console. The output path will be different on your system.

## Bundling Ruby libs and executables

You can include Ruby libs needed by your action by placing them inside your action bundle. Before running your action, runner.rb changes the working directory to the inside of your action bundle. This means you can do require 'libname' where libname is the name of a .rb file inside your action bundle. There is an example of this in the [Flickr Upload](https://github.com/aptonic/dropzone3-actions/tree/master/Flickr%20Upload.dzbundle) bundle. The Flickr Upload action also demonstrates how to launch an application or command line tool bundled with your action. 

## Customizing your actions icon

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