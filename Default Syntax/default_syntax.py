


import sublime
import sublime_plugin


class DefaultSyntaxCommand(sublime_plugin.EventListener):

	def on_new(self, view):

		view.set_syntax_file("Packages/C++/C++.tmLanguage")



class CopyScopeToClipboardCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    syntax_name = self.view.scope_name(self.view.sel()[0].begin())
    print(syntax_name)
    self.view.set_status("Scope",syntax_name)
    sublime.set_clipboard(syntax_name)



class GetScopeAlwaysTextCommand( sublime_plugin.TextCommand ):

	def run( self, edit ):

		# status = self.view.get_status( "scope_always" )
		status = sublime.active_window().active_view().get_status( "scope_always" )
		print( status )



class ForceRewriteSublimeSettingsCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        sublime.save_settings('Preferences.sublime-settings')



isNotSyncedSideBarEnabled = True

class SyncedSideBarRevealInSideBarCommand(sublime_plugin.TextCommand):

    global isNotSyncedSideBarEnabled

    def run(self, edit):

        self.view.window().run_command ("reveal_in_side_bar")


    def is_visible(self):

        #print( 'isNotSyncedSideBarEnabled: ' + str( isNotSyncedSideBarEnabled ) )
        return isNotSyncedSideBarEnabled



def plugin_loaded():

    global isNotSyncedSideBarEnabled

    userSettings           = sublime.load_settings('SyncedSideBar.sublime-settings')
    packageControlSettings = sublime.load_settings('Package Control.sublime-settings')

    def updateIsSyncedSideBarEnabled():

        #print('    updateIsSyncedSideBarEnabled!!!!')

        isIgnored = False
        isIgnored = False
        
        ignoredPackages   = userSettings.get( "ignored_packages" )
        installedPackages = packageControlSettings.get( "installed_packages" )

        if( ignoredPackages != None ):

            isIgnored = any( "SyncedSideBar" in package for package in ignoredPackages )

        if( installedPackages != None ):

            isInstalled = any( "SyncedSideBar" in package for package in installedPackages )

        updateGlobalData( isIgnored, isInstalled )

        #print( 'isIgnored: ' + str( isIgnored ) )
        #print( 'isInstalled: ' + str( isInstalled ) )


    def updateGlobalData( isIgnored, isInstalled ):

        global isNotSyncedSideBarEnabled

        if isIgnored:

            isNotSyncedSideBarEnabled = True

        else:

            if isInstalled:

                isEnabled = userSettings.get( "reveal-on-activate" )
                isNotSyncedSideBarEnabled = not isEnabled

            else:

                isNotSyncedSideBarEnabled = True

        #print( 'isNotSyncedSideBarEnabled: ' + str( isNotSyncedSideBarEnabled ) )


    def read_pref_async():

        #print('READ_PREF_ASYNC!!!!')
        updateIsSyncedSideBarEnabled()


    def read_pref_package():

        #print('READ_PREF_PACKAGE!!!!')
        packageControlSettings = sublime.load_settings('Package Control.sublime-settings')
        updateIsSyncedSideBarEnabled()


    def read_pref_preferences():

        #print('READ_PREF_PREFERENCES!!!!')
        userSettings = sublime.load_settings('SyncedSideBar.sublime-settings')
        updateIsSyncedSideBarEnabled()


    # read initial setting, after all packages being loaded
    sublime.set_timeout_async( read_pref_async, 10000 )

    # listen for changes
    userSettings.add_on_change( "SyncedSideBar", read_pref_preferences )
    packageControlSettings.add_on_change( "Package Control", read_pref_package )

    #print( userSettings.get( "ignored_packages" ) )
    #print( packageControlSettings.get( "installed_packages" ) )




