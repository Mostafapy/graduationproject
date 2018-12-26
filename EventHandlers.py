# Event Handlers ======================================================================

import win32com.client
import sys
import codecs

class NktSpyMgrEvents:

        def OnProcessStarted(self, nktProcessAsPyIDispatch):
                nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
                print (nktProcess.Name,"is started ",'\n')

        def OnProcessTerminated(self, nktProcessAsPyIDispatch):
                nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
                print ("process name Terminated : ",nktProcess.Name,'\n')
                
        def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):

            nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
            nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
            nkthook = win32com.client.Dispatch(nktHookAsPyIDispatch)
            file_name = nktProcess.Name
            file_name =file_name.split('.')[0]+".txt"
            log_file = open(file_name,'a')
            if (nktHookCallInfo.IsPreCall):
                Params = nktHookCallInfo.Params()
                name=nkthook.FunctionName
              
                paramters=""
                for i in range(0,Params.Count):
                     try:
                       p = Params.GetAt(i)
                       paramters=str(paramters)+str(p)
                       if(i < Params.Count - 1 and str(p)!=""):
                        paramters=paramters+","
 
                     except Exception as e:
                       paramters=paramters+""

                     
                if(Params.Count== 0):
                 log_file.write(name+",\n")

                elif(Params.Count  != 0):
                 try:       
                  st =name + ','+ paramters +','
                  log_file.write(str(st + '\n'))
                 except Exception as e:
                   print("")                 
                log_file.close()


