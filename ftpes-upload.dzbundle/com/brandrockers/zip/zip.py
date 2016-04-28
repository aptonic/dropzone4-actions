"""
This class manage the zipping process.
"""
import errno
import os
import subprocess


class ZIP(object):
    """
    An array for all files which should be excludes from the zip file
    """
    ZIP_IGNORES = ['*.git', '*.svn', '*.DS_Store']

    def __init__(self, items=None, tmp_directory='/tmp', output_name=None):
        """
        Helper class for zipping local files.

        @param items: An array with all items to zip
        @type items: Array
        @param tmp_directory: The tmp directory of dropzone
        @type tmp_directory: String
        @param output_name: The name of the target zip file
        @type output_name: String
        """
        self._items = items
        self._tmp_directory = tmp_directory
        self._output_name = output_name
        self._full_output_name = os.path.join(self._tmp_directory, self._output_name)
        self._zip_ignores_as_string = ''

        for ignore in self.ZIP_IGNORES:
            self._zip_ignores_as_string += '-x "' + ignore + '" '

    def zip(self):
        """
        Zip all files into one zip.
        """

        if self._items is None or len(self._items) is 0:
            return False

        if os.path.isfile(self._full_output_name) is not True:

            for item in self._items:
                item_dirname = os.path.dirname(item)
                item_relname = item.replace(item_dirname, '.')
                command = ('cd "%s" && zip -q -r "%s" "%s" %s' % (
                    item_dirname, self._full_output_name, item_relname,
                    self._zip_ignores_as_string))

                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                process.wait()

                if process.returncode is not 0:
                    print "AN ERROR OCCURED!"
        else:
            raise OSError(errno.EEXIST, ('File "%s" already exists!' % self._full_output_name))

    def cleanup(self):
        """
        Delete the generated zip file from the tmp directory
        """
        try:
            if os.path.isfile(self._full_output_name):
                os.unlink(self._full_output_name)
        except Exception as exception:
            print exception.message

    @property
    def absolute_zipfile_path(self):
        """
        Get the absolute file path for the zip file.
        @return: The absolute file path of the zip file.
        @rtype: String
        """
        return self._full_output_name
