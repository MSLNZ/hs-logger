# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 10 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MyFrame7
###########################################################################

class BasicFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,402 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
        
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_menubar1 = wx.MenuBar( 0 )
        self.file_menu = wx.Menu()
        self.file_new = wx.MenuItem( self.file_menu, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
        self.file_menu.Append( self.file_new )
        
        self.file_open = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.file_menu.Append( self.file_open )
        
        self.file_save = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.file_menu.Append( self.file_save )
        
        self.file_menu.AppendSeparator()
        
        self.file_exit = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.file_menu.Append( self.file_exit )
        
        self.m_menubar1.Append( self.file_menu, u"File" ) 
        
        self.edit_menu = wx.Menu()
        self.m_menubar1.Append( self.edit_menu, u"Edit" ) 
        
        self.view_menu = wx.Menu()
        self.m_menuItem2 = wx.MenuItem( self.view_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_CHECK )
        self.view_menu.Append( self.m_menuItem2 )
        
        self.m_menubar1.Append( self.view_menu, u"View" ) 
        
        self.tools_menu = wx.Menu()
        self.m_menubar1.Append( self.tools_menu, u"Tools" ) 
        
        self.about_menu = wx.Menu()
        self.m_menubar1.Append( self.about_menu, u"About" ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        bSizer67 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter3.SetSashGravity( 0.1 )
        self.m_splitter3.SetSashSize( 40 )
        self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
        
        self.logger_panel = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer48 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        bSizer48.Add( ( 5, 0), 0, wx.EXPAND, 5 )
        
        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.logger_panel, wx.ID_ANY, u"Logger" ), wx.VERTICAL )
        
        self.logger_start = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.logger_start.Enable( False )
        
        sbSizer3.Add( self.logger_start, 0, wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        self.logger_stop = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.logger_stop.Enable( False )
        #self.logger_stop.Hide()
        
        sbSizer3.Add( self.logger_stop, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.logger_pause = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.logger_pause.Enable( False )
        
        sbSizer3.Add( self.logger_pause, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.logger_resume = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Resume", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.logger_resume.Enable( False )
        #self.logger_resume.Hide()
        
        sbSizer3.Add( self.logger_resume, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.logger_details = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Details", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.logger_details.Enable( False )
        
        sbSizer3.Add( self.logger_details, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer48.Add( sbSizer3, 1, wx.EXPAND, 5 )
        
        
        bSizer48.Add( ( 5, 0), 0, wx.EXPAND, 5 )
        
        
        self.logger_panel.SetSizer( bSizer48 )
        self.logger_panel.Layout()
        bSizer48.Fit( self.logger_panel )
        self.logger_panel1 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_notebook4 = wx.Notebook( self.logger_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.job_page = wx.Panel( self.m_notebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer2 = wx.FlexGridSizer( 8, 2, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText3 = wx.StaticText( self.job_page, wx.ID_ANY, u"Job Name: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_staticText10 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        fgSizer2.Add( self.m_staticText10, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self.job_page, wx.ID_ANY, u"author :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        fgSizer2.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_staticText17 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )
        fgSizer2.Add( self.m_staticText17, 0, wx.ALL, 5 )
        
        self.m_staticText6 = wx.StaticText( self.job_page, wx.ID_ANY, u"Date :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        fgSizer2.Add( self.m_staticText6, 0, wx.ALL, 5 )
        
        self.m_staticText18 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )
        fgSizer2.Add( self.m_staticText18, 0, wx.ALL, 5 )
        
        self.m_staticText5 = wx.StaticText( self.job_page, wx.ID_ANY, u"Instruments :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        fgSizer2.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        bSizer13 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText19 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )
        bSizer13.Add( self.m_staticText19, 0, wx.ALL, 5 )
        
        self.m_staticText23 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )
        bSizer13.Add( self.m_staticText23, 0, wx.ALL, 5 )
        
        
        fgSizer2.Add( bSizer13, 1, wx.EXPAND, 5 )
        
        self.m_staticText7 = wx.StaticText( self.job_page, wx.ID_ANY, u"Time Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        fgSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.m_staticText20 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )
        fgSizer2.Add( self.m_staticText20, 0, wx.ALL, 5 )
        
        self.m_staticText8 = wx.StaticText( self.job_page, wx.ID_ANY, u"Log Interval :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        fgSizer2.Add( self.m_staticText8, 0, wx.ALL, 5 )
        
        self.m_staticText21 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )
        fgSizer2.Add( self.m_staticText21, 0, wx.ALL, 5 )
        
        self.m_staticText9 = wx.StaticText( self.job_page, wx.ID_ANY, u"Log Operations :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        fgSizer2.Add( self.m_staticText9, 0, wx.ALL, 5 )
        
        self.m_staticText22 = wx.StaticText( self.job_page, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )
        fgSizer2.Add( self.m_staticText22, 0, wx.ALL, 5 )
        
        
        self.job_page.SetSizer( fgSizer2 )
        self.job_page.Layout()
        fgSizer2.Fit( self.job_page )
        self.m_notebook4.AddPage( self.job_page, u"Job", False )
        self.log_pannel = wx.Panel( self.m_notebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_textCtrl1 = wx.TextCtrl( self.log_pannel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        bSizer9.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.log_pannel.SetSizer( bSizer9 )
        self.log_pannel.Layout()
        bSizer9.Fit( self.log_pannel )
        self.m_notebook4.AddPage( self.log_pannel, u"Log", True )
        self.m_panel14 = wx.Panel( self.m_notebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_notebook4.AddPage( self.m_panel14, u"a page", False )
        
        bSizer10.Add( self.m_notebook4, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.logger_panel1.SetSizer( bSizer10 )
        self.logger_panel1.Layout()
        bSizer10.Fit( self.logger_panel1 )
        self.m_splitter3.SplitVertically( self.logger_panel, self.logger_panel1, 130 )
        bSizer67.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer67 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_MENU, self.file_openOnMenuSelection, id = self.file_open.GetId() )
        self.logger_start.Bind( wx.EVT_BUTTON, self.logger_startOnButtonClick )
        self.logger_stop.Bind( wx.EVT_BUTTON, self.logger_stopOnButtonClick )
        self.logger_pause.Bind( wx.EVT_BUTTON, self.logger_pauseOnButtonClick )
        self.logger_resume.Bind( wx.EVT_BUTTON, self.logger_resumeOnButtonClick )
        self.logger_details.Bind( wx.EVT_BUTTON, self.logger_detailsOnButtonClick )

    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def file_openOnMenuSelection( self, event ):
        event.skip()
        
    
    def logger_startOnButtonClick( self, event ):
        event.Skip()
    
    def logger_pauseOnButtonClick( self, event ):
        event.Skip()
    
    def logger_detailsOnButtonClick( self, event ):
        event.Skip()

    def logger_stopOnButtonClick( self, event ):
        event.Skip()

    def logger_resumeOnButtonClick( self, event ):
        event.Skip()
    
    def m_splitter3OnIdle( self, event ):
        self.m_splitter3.SetSashPosition( 130 )
        self.m_splitter3.Unbind( wx.EVT_IDLE )
    

class Error_dialog ( wx.Dialog ):
    
    def __init__( self, parent , details):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer8 = wx.BoxSizer( wx.VERTICAL )
        
        self.error_text = wx.StaticText( self, wx.ID_ANY, details, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.error_text.Wrap( -1 )
        bSizer8.Add( self.error_text, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.m_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_ok, 0, wx.ALL, 5 )
        
        
        self.SetSizer( bSizer8 )
        self.Layout()
        bSizer8.Fit( self )
        
        self.Centre( wx.BOTH )
    
        self.m_ok.Bind( wx.EVT_BUTTON, self.m_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def m_okOnButtonClick( self, event ):
        self.Destroy()


def main():
    app = wx.App()
    frame = BasicFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

