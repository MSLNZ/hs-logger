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
		
		self.open_job_b = wx.Button( self, wx.ID_ANY, u"Open Job", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.open_job_b, 0, wx.ALL, 5 )
		
		self.open_inst_b = wx.Button( self, wx.ID_ANY, u"Open Inst", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.open_inst_b, 0, wx.ALL, 5 )
		
		
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
		bSizer30.Add( self.inst_listbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnCloseFrame )
		self.open_job_b.Bind( wx.EVT_BUTTON, self.job_open )
		self.open_inst_b.Bind( wx.EVT_BUTTON, self.inst_open )
		self.job_listbox.Bind( wx.EVT_LISTBOX_DCLICK, self.switchToJob )
		self.inst_listbox.Bind( wx.EVT_LISTBOX_DCLICK, self.switchToInst )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnCloseFrame( self, event ):
		event.Skip()
	
	def job_open( self, event ):
		event.Skip()
	
	def inst_open( self, event ):
		event.Skip()
	
	def switchToJob( self, event ):
		event.Skip()
	
	def switchToInst( self, event ):
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"<job_name>", pos = wx.DefaultPosition, size = wx.Size( 702,431 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer59 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer60 = wx.BoxSizer( wx.VERTICAL )
		
		self.start_b = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.start_b, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.pause_b = wx.Button( self, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.pause_b, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.resume_b = wx.Button( self, wx.ID_ANY, u"Resume", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.resume_b, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer611 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.reading_number = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.reading_number.Wrap( -1 )
		bSizer611.Add( self.reading_number, 1, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.countdown_number = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.countdown_number.Wrap( -1 )
		bSizer611.Add( self.countdown_number, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer60.Add( bSizer611, 0, wx.EXPAND, 5 )
		
		self.reading_text = wx.StaticText( self, wx.ID_ANY, u"Reading:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.reading_text.Wrap( -1 )
		bSizer60.Add( self.reading_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.current_reading = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.current_reading.Wrap( -1 )
		bSizer60.Add( self.current_reading, 0, wx.ALL, 5 )
		
		self.next_point_text = wx.StaticText( self, wx.ID_ANY, u"Next Point In:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.next_point_text.Wrap( -1 )
		bSizer60.Add( self.next_point_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.next_point_time = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.next_point_time.Wrap( 100 )
		bSizer60.Add( self.next_point_time, 0, wx.ALL, 5 )
		
		
		bSizer59.Add( bSizer60, 0, wx.EXPAND, 5 )
		
		self.job_book = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.job_book.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		self.job_book.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
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
		
		self.last_n = wx.Button( self.points, wx.ID_ANY, u"Last N", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.last_n, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.next_n = wx.Button( self.points, wx.ID_ANY, u"Next N", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.next_n, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer39 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.n_points_text = wx.StaticText( self.points, wx.ID_ANY, u"N =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.n_points_text.Wrap( -1 )
		bSizer39.Add( self.n_points_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.n_points_input = wx.TextCtrl( self.points, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer39.Add( self.n_points_input, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer19.Add( bSizer39, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.transformed = wx.CheckBox( self.points, wx.ID_ANY, u"Transformed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.transformed.SetValue(True) 
		bSizer19.Add( self.transformed, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.comment_text = wx.StaticText( self.points, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.comment_text.Wrap( -1 )
		bSizer19.Add( self.comment_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.comment_input = wx.TextCtrl( self.points, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.comment_input, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer18.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		
		bSizer17.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.points.SetSizer( bSizer17 )
		self.points.Layout()
		bSizer17.Fit( self.points )
		self.job_book.AddPage( self.points, u"Points", False )
		self.auto_profile = wx.Panel( self.job_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.auto_profile.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		self.auto_profile.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer171 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.grid_auto_profile = wx.grid.Grid( self.auto_profile, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.grid_auto_profile.CreateGrid( 50, 20 )
		self.grid_auto_profile.EnableEditing( True )
		self.grid_auto_profile.EnableGridLines( True )
		self.grid_auto_profile.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.grid_auto_profile.EnableDragGridSize( False )
		self.grid_auto_profile.SetMargins( 0, 0 )
		
		# Columns
		self.grid_auto_profile.AutoSizeColumns()
		self.grid_auto_profile.EnableDragColMove( True )
		self.grid_auto_profile.EnableDragColSize( False )
		self.grid_auto_profile.SetColLabelSize( 30 )
		self.grid_auto_profile.SetColLabelValue( 0, u"Point" )
		self.grid_auto_profile.SetColLabelValue( 1, u"Set" )
		self.grid_auto_profile.SetColLabelValue( 2, u"Soak" )
		self.grid_auto_profile.SetColLabelValue( 3, u"Assured Soak" )
		self.grid_auto_profile.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.grid_auto_profile.SetRowSize( 0, 21 )
		self.grid_auto_profile.SetRowSize( 1, 21 )
		self.grid_auto_profile.SetRowSize( 2, 21 )
		self.grid_auto_profile.SetRowSize( 3, 21 )
		self.grid_auto_profile.SetRowSize( 4, 21 )
		self.grid_auto_profile.EnableDragRowSize( False )
		self.grid_auto_profile.SetRowLabelSize( 30 )
		self.grid_auto_profile.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.grid_auto_profile.SetDefaultCellBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.grid_auto_profile.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer181.Add( self.grid_auto_profile, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer191 = wx.BoxSizer( wx.VERTICAL )
		
		self.next_point_btn = wx.Button( self.auto_profile, wx.ID_ANY, u"Next Point", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.next_point_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.move_to = wx.Button( self.auto_profile, wx.ID_ANY, u"Move to Selected", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.move_to, 0, wx.ALL, 5 )
		
		self.points_load = wx.Button( self.auto_profile, wx.ID_ANY, u"Load File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.points_load, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.new_set_btn = wx.Button( self.auto_profile, wx.ID_ANY, u"New Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.new_set_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.new_point_btn = wx.Button( self.auto_profile, wx.ID_ANY, u"New Point", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer191.Add( self.new_point_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer391 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.assured_error_text = wx.StaticText( self.auto_profile, wx.ID_ANY, u"Error <", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.assured_error_text.Wrap( -1 )
		self.assured_error_text.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer391.Add( self.assured_error_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.assured_error_input = wx.TextCtrl( self.auto_profile, wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer391.Add( self.assured_error_input, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer191.Add( bSizer391, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer392 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.assured_stdev_text = wx.StaticText( self.auto_profile, wx.ID_ANY, u"StDev <", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.assured_stdev_text.Wrap( -1 )
		self.assured_stdev_text.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer392.Add( self.assured_stdev_text, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.assured_stdev_input = wx.TextCtrl( self.auto_profile, wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer392.Add( self.assured_stdev_input, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer191.Add( bSizer392, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer181.Add( bSizer191, 0, wx.EXPAND, 7 )
		
		
		bSizer171.Add( bSizer181, 1, wx.EXPAND, 5 )
		
		
		self.auto_profile.SetSizer( bSizer171 )
		self.auto_profile.Layout()
		bSizer171.Fit( self.auto_profile )
		self.job_book.AddPage( self.auto_profile, u"Profile", True )
		
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
		self.add_graph_m = wx.MenuItem( self.graph_m, wx.ID_ANY, u"Add Graph", wx.EmptyString, wx.ITEM_NORMAL )
		self.graph_m.Append( self.add_graph_m )

		self.remove_graph_m = wx.MenuItem(self.graph_m, wx.ID_ANY, u"Remove Graph", wx.EmptyString, wx.ITEM_NORMAL)
		self.graph_m.Append(self.remove_graph_m)
		
		self.append_graph_m = wx.MenuItem( self.graph_m, wx.ID_ANY, u"Append Trace", wx.EmptyString, wx.ITEM_NORMAL )
		self.graph_m.Append( self.append_graph_m )
		
		self.detract_graph_m = wx.MenuItem( self.graph_m, wx.ID_ANY, u"Detract Trace", wx.EmptyString, wx.ITEM_NORMAL )
		self.graph_m.Append( self.detract_graph_m )

		
		self.m_menubar2.Append( self.graph_m, u"Graph" ) 
		
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.hide )
		self.start_b.Bind( wx.EVT_BUTTON, self.start_log )
		self.pause_b.Bind( wx.EVT_BUTTON, self.pause_log )
		self.resume_b.Bind( wx.EVT_BUTTON, self.resume_log )
		self.last_n.Bind( wx.EVT_BUTTON, self.take_last_n )
		self.next_n.Bind( wx.EVT_BUTTON, self.take_next_n )
		self.next_point_btn.Bind( wx.EVT_BUTTON, self.next_point_autoprofile )
		self.move_to.Bind( wx.EVT_BUTTON, self.move_to_selected )
		self.points_load.Bind( wx.EVT_BUTTON, self.load_autoprofile )
		self.new_set_btn.Bind( wx.EVT_BUTTON, self.new_profile_action )
		self.new_point_btn.Bind( wx.EVT_BUTTON, self.new_point_autoprofile )
		self.assured_error_input.Bind( wx.EVT_TEXT, self.update_table )
		self.assured_stdev_input.Bind( wx.EVT_TEXT, self.update_table )
		self.Bind( wx.EVT_MENU, self.add_graph, id = self.add_graph_m.GetId() )
		self.Bind( wx.EVT_MENU, self.append_graph, id = self.append_graph_m.GetId() )
		self.Bind( wx.EVT_MENU, self.detract_graph, id = self.detract_graph_m.GetId() )
		self.Bind( wx.EVT_MENU, self.remove_graph, id = self.remove_graph_m.GetId() )
	
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
	
	def take_last_n( self, event ):
		event.Skip()
	
	def take_next_n( self, event ):
		event.Skip()
	
	def next_point_autoprofile( self, event ):
		event.Skip()
	
	def move_to_selected( self, event ):
		event.Skip()
	
	def load_autoprofile( self, event ):
		event.Skip()
	
	def new_profile_action( self, event ):
		event.Skip()
	
	def new_point_autoprofile( self, event ):
		event.Skip()
	
	def update_table( self, event ):
		event.Skip()
	
	
	def add_graph( self, event ):
		event.Skip()
	
	def append_graph( self, event ):
		event.Skip()
	
	def detract_graph( self, event ):
		event.Skip()
	
	def remove_graph( self, event ):
		event.Skip()
	

###########################################################################
## Class add_graph_dialog
###########################################################################

class add_graph_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 596,256 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Add Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer19.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer16.Add( ( 0, 0), 1, 0, 5 )
		
		self.label_name = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_name.Wrap( -1 )
		bSizer16.Add( self.label_name, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.label_text = wx.TextCtrl( self, wx.ID_ANY, u"New Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.label_text, 4, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
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
		
		
		bSizer19.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class append_graph_dialog
###########################################################################

class append_graph_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 288,185 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.graph_lable = wx.StaticText( self, wx.ID_ANY, u"Append Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.graph_lable.Wrap( -1 )
		bSizer20.Add( self.graph_lable, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		graph_choiceChoices = []
		self.graph_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, graph_choiceChoices, 0 )
		self.graph_choice.SetSelection( 0 )
		bSizer20.Add( self.graph_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer15.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer201 = wx.BoxSizer( wx.VERTICAL )
		
		self.y_lable = wx.StaticText( self, wx.ID_ANY, u"New Y Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.y_lable.Wrap( -1 )
		bSizer201.Add( self.y_lable, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		y_choiceChoices = []
		self.y_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, y_choiceChoices, 0 )
		self.y_choice.SetSelection( 0 )
		bSizer201.Add( self.y_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer201, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class detract_graph_graph_dialog
###########################################################################

class detract_graph_graph_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 288,131 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Detract Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer19.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Graph_label = wx.StaticText( self, wx.ID_ANY, u"Choose Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Graph_label.Wrap( -1 )
		bSizer25.Add( self.Graph_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		graph_choiceChoices = []
		self.graph_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, graph_choiceChoices, 0 )
		self.graph_choice.SetSelection( 0 )
		bSizer20.Add( self.graph_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class detract_graph_axis_dialog
###########################################################################

class detract_graph_axis_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 288,131 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Detract Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer19.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.axis_label = wx.StaticText( self, wx.ID_ANY, u"Choose Axis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.axis_label.Wrap( -1 )
		bSizer25.Add( self.axis_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		axis_choiceChoices = []
		self.axis_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, axis_choiceChoices, 0 )
		self.axis_choice.SetSelection( 0 )
		bSizer20.Add( self.axis_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class remove_graph_dialog
###########################################################################

class remove_graph_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 288,125 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Remove Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer19.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		graph_choiceChoices = []
		self.graph_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, graph_choiceChoices, 0 )
		self.graph_choice.SetSelection( 0 )
		bSizer20.Add( self.graph_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer15.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class continue_dialog
###########################################################################

class continue_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 288,146 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.Message = wx.StaticText( self, wx.ID_ANY, u"Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Message.Wrap( -1 )
		bSizer19.Add( self.Message, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText81 = wx.StaticText( self, wx.ID_ANY, u"Continue?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		bSizer20.Add( self.m_staticText81, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer15.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_b = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.cancel_b, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.confirm_b = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.confirm_b, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
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
	

###########################################################################
## Class Load_profile_dialog
###########################################################################

class Load_profile_dialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer36 = wx.BoxSizer( wx.VERTICAL )
		
		self.profile_filePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer36.Add( self.profile_filePicker, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button27 = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer37.Add( self.m_button27, 1, wx.ALL, 5 )
		
		self.m_button28 = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer37.Add( self.m_button28, 1, wx.ALL, 5 )
		
		
		bSizer36.Add( bSizer37, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer36 )
		self.Layout()
		bSizer36.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class new_action_autoprofile_dlg
###########################################################################

class new_action_autoprofile_dlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 289,232 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.action_name_label = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.action_name_label.Wrap( -1 )
		bSizer35.Add( self.action_name_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.profile_name_ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.profile_name_ctrl, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer35, 0, wx.EXPAND, 5 )
		
		bSizer354 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText114 = wx.StaticText( self, wx.ID_ANY, u"Instrument", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText114.Wrap( -1 )
		bSizer354.Add( self.m_staticText114, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.profile_inst_ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer354.Add( self.profile_inst_ctrl, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer354, 0, wx.EXPAND, 5 )
		
		bSizer351 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText111.Wrap( -1 )
		bSizer351.Add( self.m_staticText111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.profile_set_ctrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer351.Add( self.profile_set_ctrl, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer351, 0, wx.EXPAND, 5 )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ocancel_new_profile_action = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.ocancel_new_profile_action, 0, wx.ALL, 5 )
		
		
		bSizer41.Add( ( 20, 0), 0, wx.EXPAND, 5 )
		
		self.ok_new_profile_action = wx.Button( self, wx.ID_OK, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.ok_new_profile_action, 0, wx.ALL, 5 )
		
		
		bSizer34.Add( bSizer41, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer34 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ocancel_new_profile_action.Bind( wx.EVT_BUTTON, self.cancel_dialog )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_dialog( self, event ):
		event.Skip()
	

###########################################################################
## Class inst_pannel
###########################################################################

class inst_pannel ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"<instrument>", pos = wx.DefaultPosition, size = wx.Size( 515,253 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel8 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Actions", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer26.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		bSizer47 = wx.BoxSizer( wx.HORIZONTAL )
		
		read_op_choiceChoices = []
		self.read_op_choice = wx.Choice( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, read_op_choiceChoices, 0 )
		self.read_op_choice.SetSelection( 0 )
		bSizer47.Add( self.read_op_choice, 1, wx.ALL, 5 )
		
		self.read_response_ctrl = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.read_response_ctrl, 1, wx.ALL, 5 )
		
		self.read_btn = wx.Button( self.m_panel8, wx.ID_ANY, u"READ", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.read_btn, 0, wx.ALL, 5 )
		
		
		bSizer26.Add( bSizer47, 0, wx.EXPAND, 5 )
		
		bSizer471 = wx.BoxSizer( wx.HORIZONTAL )
		
		write_op_choiceChoices = []
		self.write_op_choice = wx.Choice( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, write_op_choiceChoices, 0 )
		self.write_op_choice.SetSelection( 0 )
		bSizer471.Add( self.write_op_choice, 1, wx.ALL, 5 )
		
		self.write_text_ctrl = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer471.Add( self.write_text_ctrl, 1, wx.ALL, 5 )
		
		self.write_btn = wx.Button( self.m_panel8, wx.ID_ANY, u"WRITE", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer471.Add( self.write_btn, 0, wx.ALL, 5 )
		
		
		bSizer26.Add( bSizer471, 0, wx.EXPAND, 5 )
		
		bSizer4711 = wx.BoxSizer( wx.HORIZONTAL )
		
		action_choiceChoices = [ u"Stop", u"Purge", u"Generate" ]
		self.action_choice = wx.Choice( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, action_choiceChoices, 0 )
		self.action_choice.SetSelection( 1 )
		bSizer4711.Add( self.action_choice, 1, wx.ALL, 5 )
		
		self.action_btn = wx.Button( self.m_panel8, wx.ID_ANY, u"ACTION", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4711.Add( self.action_btn, 0, wx.ALL, 5 )
		
		
		bSizer26.Add( bSizer4711, 0, wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer26 )
		self.m_panel8.Layout()
		bSizer26.Fit( self.m_panel8 )
		self.m_splitter1.Initialize( self.m_panel8 )
		bSizer22.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer22 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.hide )
		self.read_btn.Bind( wx.EVT_BUTTON, self.read_op )
		self.write_btn.Bind( wx.EVT_BUTTON, self.write_op )
		self.action_btn.Bind( wx.EVT_BUTTON, self.action_op )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def hide( self, event ):
		event.Skip()
	
	def read_op( self, event ):
		event.Skip()
	
	def write_op( self, event ):
		event.Skip()
	
	def action_op( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

