import wx

class CredentialsPanel(wx.Panel):
    """
    Panel for supplying credentials (e.g. username and password) for
    interacting with XNAT database
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        username_panel = wx.Panel(self)
        username_panel_sizer= wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(username_panel, wx.ID_ANY, label="Username:")
        username_panel_sizer.Add(username_label, 0, wx.ALIGN_CENTER_VERTICAL, 50)
        username_text = wx.TextCtrl(username_panel, wx.ID_ANY)
        username_panel_sizer.Add(username_text, 1, wx.ALIGN_CENTER_VERTICAL, 50)

        username_panel.SetSizer(username_panel_sizer)

        sizer.Add(username_panel, 0, wx.ALIGN_CENTER, 50)

        self.SetSizer(sizer)

class LaunchPanel(wx.Panel):
    """
    Panel for launching pipelines
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        txtOne = wx.TextCtrl(self, wx.ID_ANY, "hello")
        sizer.Add(txtOne, 0, wx.ALL, 5)

        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "there")
        sizer.Add(txtTwo, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class StatusPanel(wx.Panel):
    """
    Panel to determine the status of various pipeline 
    processing jobs
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "somebody")
        sizer.Add(txtOne, 0, wx.ALL, 5)

        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "new")
        sizer.Add(txtTwo, 0, wx.ALL, 5)

        self.SetSizer(sizer)




class PipelineControlCenterNotebook(wx.Notebook):
    """
    Notebook (tabbed panel) containing a tab for each 'aspect' of the 
    PipelineControlCenter application
    """

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

        # Create the launch panel and add it to the notebook
        credentials_panel = CredentialsPanel(self)
        self.AddPage(credentials_panel, "Credentials")

        launch_panel = LaunchPanel(self)
        self.AddPage(launch_panel, "Launch")

        status_panel = StatusPanel(self)
        self.AddPage(status_panel, "Status")


class PipelineControlCenterFrame(wx.Frame):
    """
    Main frame for PipelineControlCenter application
    Contains a single panel which contains the Notebook (tabbed panel) with a 
    tab for each 'aspect' of the application.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "PipelineControlCenter", size=(600,400))

        panel = wx.Panel(self)
        notebook = PipelineControlCenterNotebook(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()


# Main functionality

# Create the PipelineControlCenter frame as the main window of an application

if __name__ == "__main__":
    app = wx.App()
    frame = PipelineControlCenterFrame()
    app.MainLoop()


