# Dropzone Action Info
# Name: FTPES Upload
# Description: Provides an action to upload your files to a FTPES Server
# Handles: Files
# Creator: Tino Wehe
# URL: https://github.com/pixel-shock/dropzone-ftpes-upload.git
# Events: Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0.1
# MinDropzoneVersion: 3.5
# OptionsNIB: ExtendedLogin
# UniqueID: f3d989b9-a5a5-4697-9c32-c81efa7a4ee6

# pylint: disable=missing-docstring

import ftplib
import os
import socket
import uuid

# pylint: disable=relative-import
from com.brandrockers.ftpes.ftpes import FTPES
from com.brandrockers.zip.zip import ZIP


# pylint: enable=relative-import

def create_random_filename(string_length=12):
    # Convert UUID format to a Python string
    """
    Create a random UUI for secure filename.
    @param string_length: The length of the filename
    @type string_length: Integer
    @return: A String with the random filename
    @rtype: String
    """
    random = str(uuid.uuid4())
    # Remove the UUID '-'
    random = random.replace("-", "")
    # Return the random string.
    return random[0:string_length]


def handle_upload_state(progress, ftpes_instance, do_update):
    """
    Handle the upload progress of the FTPES class.

    @param progress: The current upload progress in percent.
    @type progress: Integer
    @param ftpes_instance: An instance of the FTPES class.
    @type ftpes_instance: Object
    @param do_update: A boolean that determines if the upload handler should update the progress
    state of dropzone.
    @type do_update: Boolean
    """
    # this is due the animation delay time of the menubar icon,
    # so it should not trigger the process event too often
    if do_update is True:
        # pylint: disable=undefined-variable
        dz.percent(progress)
        # pylint: enable=undefined-variable

    if progress >= 100:
        tmp_root_path = ''

        if os.environ.get('root_url') is not None:
            tmp_root_path = os.environ.get('root_url')

        upload_path = os.path.join(tmp_root_path, ftpes_instance.upload_path)
        # pylint: disable=undefined-variable
        dz.finish('FTPES upload for "%s" done!' % upload_path)
        dz.url(upload_path)
        # pylint: enable=undefined-variable


def dragged():
    """
    The handler which will be called from dropzone if the user drags files onto the icon.
    """
    #
    # Save all dropzone vars
    #
    host = os.environ.get('server')
    port = os.environ.get('port')
    username = os.environ.get('username')
    password = os.environ.get('password')
    remote_path = os.environ.get('remote_path')
    # pylint: disable=undefined-variable
    # pylint: disable=line-too-long
    tmp_directory = dz.temp_folder()
    secure_output = dz.cocoa_dialog(
        'yesno-msgbox --no-cancel --title "Are you want to make the filename secure?" --text '
        '"This will create a filename like: QW23trU.zip"')
    secure_output = int(secure_output.strip())

    if secure_output is 2:
        output_name = dz.inputbox("Please enter the filename for the zip file!",
                                  "Filename:").replace('.zip', '') + '.zip'
    else:
        output_name = create_random_filename() + '.zip'
    # pylint: enable=line-too-long
    # pylint: enable=undefined-variable

    if host is None:
        # pylint: disable=undefined-variable
        dz.error("Error", "You must specify a hostname!")
        # pylint: enable=undefined-variable

    try:
        # pylint: disable=undefined-variable
        # set begin state for dropzone
        dz.begin('Running FTPES Task for "%s"!' % output_name)
        # set determinate to false, because the zipping process has no progress
        dz.determinate(False)
        # pylint: enable=undefined-variable
        # create a new ZIP instance
        # pylint: disable=undefined-variable
        zipper = ZIP(items, tmp_directory, output_name)
        # pylint: enable=undefined-variable
        # try to zip all files
        zipper.zip()
        # create a new FTPES instance
        ftpes = FTPES(host, port, username, password, remote_path, zipper.absolute_zipfile_path)
        try:
            # try to connect to the FTP server
            ftpes.connect()
            try:
                # Try to login to the FTP server
                ftpes.login()
                try:
                    # Try to change the working directory
                    ftpes.cwd()
                    # set determinate to True to set progress updates for dropzone
                    # pylint: disable=undefined-variable
                    dz.determinate(True)
                    # pylint: enable=undefined-variable
                    # Try to upload the zip file
                    ftpes.upload(handle_upload_state)
                    # Delete the zip file from dropzones tmp directory
                    zipper.cleanup()
                except ftplib.error_perm, msg:
                    # Delete the zip file from dropzones tmp directory
                    zipper.cleanup()
                    # throw the error to dropzone
                    # pylint: disable=undefined-variable
                    dz.error("Error", msg)
                    # pylint: enable=undefined-variable
            except ftplib.error_perm, msg:
                # Delete the zip file from dropzones tmp directory
                zipper.cleanup()
                # throw the error to dropzone
                # pylint: disable=undefined-variable
                dz.error("Error", msg)
                # pylint: enable=undefined-variable
        except socket.gaierror, msg:
            # Delete the zip file from dropzones tmp directory
            zipper.cleanup()
            # throw the error to dropzone
            # pylint: disable=undefined-variable
            dz.error("Error", msg)
            # pylint: enable=undefined-variable
    except OSError as exception:
        # throw the error to dropzone
        # pylint: disable=undefined-variable
        dz.error("Error", exception.strerror)
        # pylint: enable=undefined-variable
