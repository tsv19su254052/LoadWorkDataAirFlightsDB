import tkvue


class RootDialog(tkvue.Component):
   template = """
<TopLevel title="TKVue Test">
   <Frame pack-fill="both" pack-expand="1" pack-padx="10" pack-pady="10">
       <Label text="Available values: " width="20" pack-side="left"/>
       <ComboBox pack-side="left" pack-expand="1" values="{{myvalues}}" textvariable="{{var1}}" />
   </Frame>
   <Frame pack-fill="both" pack-expand="1" pack-padx="10" pack-pady="10">
       <Label text="{{'Available values:' + var1 }}" />
   </Frame>
</TopLevel>
   """
   data = tkvue.Context({"myvalues": ["zero", "one", "two", "three"], "var1": ""})


dlg = RootDialog()
dlg.mainloop()
