#!/usr/bin/python3
# Interpreter 3.7 -> 3.11
# coding: utf-8

import tkvue
#import tkinter.ttk as ttk
#from tkinter import ttk
import tkinter

tkvue.configure_tk(theme="clam")


class RootDialog(tkvue.Component):
    template = """
<TopLevel title="TKVue Test" geometry="450x200">
    <Frame style="default.TFrame" pack-fill="both" pack-expand="1" padding="10">
        <Label text="Hello World!" style="H1.TLabel" pack-padx="25" pack-pady="25"/>
        <Frame style="default.TFrame" pack-fill="both" pack-expand="1" pack-padx="10" pack-pady="10">
            <Button style="default.TButton" text="Continue" pack-side="right" pack-padx="5"/>
            <Button style="default.TButton" text="Cancel" pack-side="right"/>
        </Frame>
    </Frame>
</TopLevel>
    """

    def __init__(self, master=None):
        super().__init__(master)
        s = tkinter.ttk.Style(master=self.root)
        s.configure('H1.TLabel', font=['Lato', '-60'], background='#ffffff')
        s.configure('default.TFrame', background='#ffffff')
        s.configure('default.TButton', foreground='#0E2933', background='#B6DDE2', bordercolor='#ACD1D6', darkcolor='#B6DDE2', lightcolor='#B6DDE2', focuscolor='#0E2933', )
        s.map('default.TButton', background=[('disabled', '#E9F4F6'), ('hover !disabled', '#9ABBC0'), ('pressed !disabled', '#88A5A9')], )


if __name__ == "__main__":
    dlg = RootDialog()
    dlg.mainloop()
