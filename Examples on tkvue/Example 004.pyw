import tkvue


class RootDialog(tkvue.Component):
   template = """
      <TopLevel geometry="970x500" title="TKVue Test">
         <Frame pack-fill="both" pack-expand="true" padding="10">
             <Label text="Selection number of row to display:" />
             <Combobox values="{{ list(range(1, 100)) }}" textvariable="{{ count }}"/>
             <Frame pack-fill="both" pack-expand="1" pack-side="left">
                 <Label pack-fill="x" pack-expand="1" for="i in range(1, count)" text="{{ 'row %s' % i }}" />
             </Frame>
         </Frame>
      </TopLevel>
         """
   data = tkvue.Context({'count': 5})


if __name__ == "__main__":
   dlg = RootDialog()
   dlg.mainloop()
