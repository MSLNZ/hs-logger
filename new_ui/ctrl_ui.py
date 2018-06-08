# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class ctrl_frame
###########################################################################

class ctrl_frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"msl-hs-logger", pos = wx.DefaultPosition, size = wx.Size( 387,174 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
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
		
		
		bSizer9.Add( bSizer28, 0, wx.EXPAND, 5 )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		self.jobs_label = wx.StaticText( self, wx.ID_ANY, u"Jobs", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.jobs_label.Wrap( -1 )
		bSizer29.Add( self.jobs_label, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		job_listboxChoices = []
		self.job_listbox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, job_listboxChoices, 0 )
		bSizer29.Add( self.job_listbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer29, 1, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.VERTICAL )
		
		self.inst_label = wx.StaticText( self, wx.ID_ANY, u"Instruments", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.inst_label.Wrap( -1 )
		bSizer30.Add( self.inst_label, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		inst_listboxChoices = []
		self.inst_listbox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, inst_listboxChoices, 0 )
		self.inst_listbox.Enable( False )
		
		bSizer30.Add( self.inst_listbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer9 )
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"<job_name>", pos = wx.DefaultPosition, size = wx.Size( 524,382 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
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
		self.points = wx.Panel( self.job_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_grid2 = wx.grid.Grid( self.points, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 5, 3 )
		self.m_grid2.EnableEditing( False )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.SetColSize( 0, 120 )
		self.m_grid2.SetColSize( 1, 120 )
		self.m_grid2.AutoSizeColumns()
		self.m_grid2.EnableDragColMove( True )
		self.m_grid2.EnableDragColSize( False )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelValue( 0, u"Latest" )
		self.m_grid2.SetColLabelValue( 1, u"Mean" )
		self.m_grid2.SetColLabelValue( 2, u"StdDev" )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.SetRowSize( 0, 19 )
		self.m_grid2.SetRowSize( 1, 19 )
		self.m_grid2.SetRowSize( 2, 19 )
		self.m_grid2.SetRowSize( 3, 19 )
		self.m_grid2.SetRowSize( 4, 41 )
		self.m_grid2.AutoSizeRows()
		self.m_grid2.EnableDragRowSize( False )
		self.m_grid2.SetRowLabelSize( 40 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer18.Add( self.m_grid2, 3, wx.ALL|wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.points_update = wx.Button( self.points, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.points_update, 0, wx.ALL, 5 )
		
		self.m_button17 = wx.Button( self.points, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_button17, 0, wx.ALL, 5 )
		
		self.m_button16 = wx.Button( self.points, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_button16, 0, wx.ALL, 5 )
		
		
		bSizer18.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		
		bSizer17.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.points.SetSizer( bSizer17 )
		self.points.Layout()
		bSizer17.Fit( self.points )
		self.job_book.AddPage( self.points, u"Points", True )
		
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
		
		self.graph_m = wx.Menu()
		self.add_graph_m = wx.MenuItem( self.graph_m, wx.ID_ANY, u"New Graph", wx.EmptyString, wx.ITEM_NORMAL )
		self.graph_m.Append( self.add_graph_m )
		
		self.m_menubar2.Append( self.graph_m, u"Graph" ) 
		
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.hide )
		self.start_b.Bind( wx.EVT_BUTTON, self.start_log )
		self.pause_b.Bind( wx.EVT_BUTTON, self.pause_log )
		self.resume_b.Bind( wx.EVT_BUTTON, self.resume_log )
		self.points_update.Bind( wx.EVT_BUTTON, self.update_table )
		self.Bind( wx.EVT_MENU, self.add_graph, id = self.add_graph_m.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def hide( self, event ):
		event.Skip()
	
	def start_log( self, event ):
		event.Skip()
	
	def pause_log( self, event ):
		event.Skip()
	
	def resume_log( self, event ):
		event.Skip()
	
	def update_table( self, event ):
		event.Skip()
	
	def add_graph( self, event ):
		event.Skip()
	

###########################################################################
## Class axes_dialog
###########################################################################

class axes_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 358,184 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"New Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer19.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer16.Add( ( 0, 0), 1, 0, 5 )
		
		self.label_name = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_name.Wrap( -1 )
		bSizer16.Add( self.label_name, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lable_text = wx.TextCtrl( self, wx.ID_ANY, u"new_label", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.lable_text, 4, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.x_label = wx.StaticText( self, wx.ID_ANY, u"X Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.x_label.Wrap( -1 )
		bSizer20.Add( self.x_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		x_choiceChoices = []
		self.x_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, x_choiceChoices, 0 )
		self.x_choice.SetSelection( 0 )
		bSizer20.Add( self.x_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		bSizer201 = wx.BoxSizer( wx.VERTICAL )
		
		self.y_lable = wx.StaticText( self, wx.ID_ANY, u"Y Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.y_lable.Wrap( -1 )
		bSizer201.Add( self.y_lable, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		y_choiceChoices = []
		self.y_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, y_choiceChoices, 0 )
		self.y_choice.SetSelection( 0 )
		bSizer201.Add( self.y_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer201, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer25, 1, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_b.Bind( wx.EVT_BUTTON, self.cancel_dialog )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_dialog( self, event ):
		event.Skip()
	

