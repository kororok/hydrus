import ClientGUICommon
import HydrusGlobals as HG
import wx

class FileDropTarget( wx.PyDropTarget ):
    
    def __init__( self, parent, filenames_callable = None, url_callable = None, page_callable = None ):
        
        wx.PyDropTarget.__init__( self )
        
        self._parent = parent
        
        self._filenames_callable = filenames_callable
        self._url_callable = url_callable
        self._page_callable = page_callable
        
        self._receiving_data_object = wx.DataObjectComposite()
        
        self._hydrus_media_data_object = wx.CustomDataObject( 'application/hydrus-media' )
        self._hydrus_page_tab_data_object = wx.CustomDataObject( 'application/hydrus-page-tab' )
        self._file_data_object = wx.FileDataObject()
        self._text_data_object = wx.TextDataObject()
        
        self._receiving_data_object.Add( self._hydrus_media_data_object, True )
        self._receiving_data_object.Add( self._hydrus_page_tab_data_object )
        self._receiving_data_object.Add( self._file_data_object )
        self._receiving_data_object.Add( self._text_data_object )
        
        self.SetDataObject( self._receiving_data_object )
        
    
    def OnData( self, x, y, result ):
        
        if self.GetData():
            
            received_format = self._receiving_data_object.GetReceivedFormat()
            
            received_format_type = received_format.GetType()
            
            if received_format_type == wx.DF_FILENAME and self._filenames_callable is not None:
                
                paths = self._file_data_object.GetFilenames()
                
                wx.CallAfter( self._filenames_callable, paths ) # callafter to terminate dnd event now
                
                result = wx.DragNone
                
            elif received_format_type in ( wx.DF_TEXT, wx.DF_UNICODETEXT ) and self._url_callable is not None:
                
                text = self._text_data_object.GetText()
                
                wx.CallAfter( self._url_callable, text ) # callafter to terminate dnd event now
                
                result = wx.DragCopy
                
            else:
                
                try:
                    
                    format_id = received_format.GetId()
                    
                except:
                    
                    format_id = None
                    
                
                if format_id == 'application/hydrus-media':
                    
                    result = wx.DragCancel
                    
                
                if format_id == 'application/hydrus-page-tab' and self._page_callable is not None:
                    
                    page_key = self._hydrus_page_tab_data_object.GetData()
                    
                    wx.CallAfter( self._page_callable, page_key ) # callafter to terminate dnd event now
                    
                    result = wx.DragMove
                    
                
            
        
        return result
        
    
    def OnDrop( self, x, y ):
        
        drop_tlp = ClientGUICommon.GetXYTopTLP( x, y )
        my_tlp = ClientGUICommon.GetTLP( self._parent )
        
        if drop_tlp == my_tlp:
            
            return True
            
        else:
            
            return False
            
        
    
    # setting OnDragOver to return copy gives Linux trouble with page tab drops with shift held down
