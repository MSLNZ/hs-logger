# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class ctrl_frame
###########################################################################

class ctrl_frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"msl-hs-logger", pos = wx.DefaultPosition, size = wx.Size( 416,185 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		wSizer5 = wx.WrapSizer( wx.HORIZONTAL )
		
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		self.new_job_b = wx.Button( self, wx.ID_ANY, u"New Job", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.new_job_b.Enable( False )
		
		bSizer28.Add( self.new_job_b, 0, wx.ALL, 5 )
		
		self.open_job_b = wx.Button( self, wx.ID_ANY, u"Open Job", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.open_job_b, 0, wx.ALL, 5 )
		
		self.open_inst_b = wx.Button( self, wx.ID_ANY, u"Open Inst", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.open_inst_b.Enable( False )
		
		bSizer28.Add( self.open_inst_b, 0, wx.ALL, 5 )
		
		self.stop_all = wx.Button( self, wx.ID_ANY, u"Stop All", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stop_all.Enable( False )
		
		bSizer28.Add( self.stop_all, 0, wx.ALL, 5 )
		
		
		wSizer5.Add( bSizer28, 1, wx.EXPAND, 5 )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		self.jobs_label = wx.StaticText( self, wx.ID_ANY, u"Jobs", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.jobs_label.Wrap( -1 )
		bSizer29.Add( self.jobs_label, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		job_listboxChoices = []
		self.job_listbox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, job_listboxChoices, 0 )
		bSizer29.Add( self.job_listbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		wSizer5.Add( bSizer29, 0, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.VERTICAL )
		
		self.inst_label = wx.StaticText( self, wx.ID_ANY, u"Instruments", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.inst_label.Wrap( -1 )
		bSizer30.Add( self.inst_label, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		inst_listboxChoices = [ u"inst1" ]
		self.inst_listbox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, inst_listboxChoices, 0 )
		self.inst_listbox.Enable( False )
		
		bSizer30.Add( self.inst_listbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		wSizer5.Add( bSizer30, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( wSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnCloseFrame )
		self.open_job_b.Bind( wx.EVT_BUTTON, self.file_open )
		self.job_listbox.Bind( wx.EVT_LISTBOX_DCLICK, self.switchToJob )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnCloseFrame( self, event ):
		event.Skip()
	
	def file_open( self, event ):
		event.Skip()
	
	def switchToJob( self, event ):
		event.Skip()
	

###########################################################################
## Class exit_dialog
###########################################################################

class exit_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 314,113 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.exit_test = wx.StaticText( self, wx.ID_ANY, u"are you sure you want to close the logger all active jobs will be stopped", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.exit_test.Wrap( -1 )
		bSizer57.Add( self.exit_test, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer58 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer58.Add( self.cancel_b, 0, wx.ALL, 5 )
		
		self.close_b = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer58.Add( self.close_b, 0, wx.ALL, 5 )
		
		
		bSizer57.Add( bSizer58, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer57 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_b.Bind( wx.EVT_BUTTON, self.cancel_close )
		self.close_b.Bind( wx.EVT_BUTTON, self.confirm_close )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_close( self, event ):
		event.Skip()
	
	def confirm_close( self, event ):
		event.Skip()
	

###########################################################################
## Class job_frame
###########################################################################

class job_frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"<job_name>", pos = wx.DefaultPosition, size = wx.Size( 407,271 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer59 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer60 = wx.BoxSizer( wx.VERTICAL )
		
		self.start_b = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.start_b, 0, wx.ALL, 5 )
		
		self.pause_b = wx.Button( self, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.pause_b, 0, wx.ALL, 5 )
		
		self.resume_b = wx.Button( self, wx.ID_ANY, u"Resume", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.resume_b, 0, wx.ALL, 5 )
		
		
		bSizer59.Add( bSizer60, 0, wx.EXPAND, 5 )
		
		self.job_book = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.log_panel = wx.Panel( self.job_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.job_disp_log = wx.TextCtrl( self.log_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer61.Add( self.job_disp_log, 1, wx.EXPAND, 5 )
		
		
		self.log_panel.SetSizer( bSizer61 )
		self.log_panel.Layout()
		bSizer61.Fit( self.log_panel )
		self.job_book.AddPage( self.log_panel, u"log", False )
		
		bSizer59.Add( self.job_book, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer59 )
		self.Layout()
		self.m_statusBar2 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar2 = wx.MenuBar( 0 )
		self.m_menu4 = wx.Menu()
		self.save_m = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.save_m )
		
		self.save_as_m = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Save as", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.save_as_m )
		
		self.m_menu4.AppendSeparator()
		
		self.close_m = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.close_m )
		
		self.m_menubar2.Append( self.m_menu4, u"File" ) 
		
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.hide )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def hide( self, event ):
		event.Skip()
	

