# Interpreter 3.7 -> 3.11

# Copyright (C) 2021 IKUS Software inc. All rights reserved.
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA


import os
import tkvue
# DOM
from xml.dom import minidom  # минимальная реализация
from xml.etree import ElementTree  # полная реализация, меньше объем исходников
# SAX
from xml.dom import pulldom  # вытягивающий анализатор для построения фрагментов DOM <-> SAX
from xml.sax import handler, make_parser
from lxml import etree, html, sax  # самый быстрый парсер
from lxml.isoschematron import Schematron
from bs4 import BeautifulSoup
import configparser


inifile = 'demo_conf.ini'
xmlfile = 'demo_conf.xml'
sourcexmlfile = 'AirCraftRegistrationXMLSource_VP-BUY.xml'  # для экспериментов
Choice = 5  # в работе


class RootDialog(tkvue.Component):
    # 0 - встроенный XML внутри скрипта,
    if Choice == 0:
        template = """
            <TopLevel geometry="970x500" title="TKVue Test">
                <Frame pack-fill="both" pack-expand="true" padding="10">
                    <Frame pack-fill="y" pack-side="left">
                        <Button style="{{'primary.TButton' if active_view == 'list' else 'secondary.TButton'}}"
                            command="set_active_view('list')" pack-fill="x" pack-padx="4" pack-pady="2" width="22" text="Dynamic list"
                            cursor="hand2" />
                        <Button style="{{'primary.TButton' if active_view == 'widgets' else 'secondary.TButton'}}"
                            command="set_active_view('widgets')" pack-fill="x" pack-padx="4" pack-pady="2" width="22" text="Widgets"
                            cursor="hand2" />
                    </Frame>
                    <Frame pack-fill="both" pack-side="right" pack-expand="1" pack-padx="3">
                        <Frame pack-fill="both" pack-expand="1" visible="{{active_view == 'list'}}">
                            <Frame pack-fill="x">
                                <Frame pack-fill="x" for="p in people" pack-expand="1">
                                    <Label text="{{p}}" pack-side="left">
                                        <ToolTip text="{{len(p)}}" />
                                    </Label>
                                    <Button text="Del" command="delete_people(p)" pack-side="right"/>
                                </Frame>
                                <Frame pack-fill="x">
                                    <Entry textvariable="{{new_people_name}}" pack-side="left" pack-expand="1" pack-fill="x" />
                                    <Button text="Add" command="add_people(new_people_name)" pack-side="right"/>
                                </Frame>
                                <Frame pack-fill="x">
                                    <Label text="New Value:" pack-side="left"/>
                                    <Label text="{{new_people_name}}" pack-side="left"/>
                                </Frame>
                            </Frame>
                        </Frame>
                        <Frame pack-fill="both" pack-expand="1" visible="{{active_view == 'widgets'}}">
                            <Frame pack-fill="x" >
                                <Label text="{{text_password}}" pack-side="left" />
                                <Entry show="•" textvariable="{{text_password}}" pack-side="left"/>
                            </Frame>
                            <Separator pack-fill="x" pack-expand="1" />
                            <Frame pack-fill="x" >
                                <ComboBox textvariable="{{style_variable}}" values="primary secondary info warning danger"/>
                                <Radiobutton variable="{{style_variable}}" style="primary.TRadiobutton" value="primary" text="primary"/>
                                <Radiobutton variable="{{style_variable}}" style="secondary.TRadiobutton" value="secondary" text="secondary"/>
                                <Radiobutton variable="{{style_variable}}" style="info.TRadiobutton" value="info" text="info"/>
                                <Radiobutton variable="{{style_variable}}" style="warning.TRadiobutton" value="warning" text="warning"/>
                                <Radiobutton variable="{{style_variable}}" style="danger.TRadiobutton" value="danger" text="danger"/>
                                <Label text="{{style_variable}}" pack-side="bottom" style="{{style_variable + '.TLabel'}}"/>
                            </Frame>
                            <Separator pack-fill="x" pack-expand="1" />
                            <Frame pack-fill="x" >
                                <Checkbutton variable="{{on_off_variable}}" pack-side="top" style="primary.TCheckbutton" text="primary.TCheckbutton"/>
                                <Checkbutton variable="{{on_off_variable}}" pack-side="top" style="info.Toolbutton" text="info.Toolbutton" />
                                <Checkbutton variable="{{on_off_variable}}" pack-side="top" style="warning.Roundtoggle.Toolbutton" text="warning.Roundtoggle.Toolbutton" />
                                <Checkbutton variable="{{on_off_variable}}" pack-side="top" text="danger.Squaretoggle.Toolbutton" />
                            </Frame>
                            <Separator pack-fill="x" pack-expand="1" />
                            <Label text="Label with wrap=1, Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." wrap="1" />
                            <Separator pack-fill="x" pack-expand="1" />
                            <ScrolledFrame pack-fill="x" pack-expand="1">
                                <Label pack-fill="x" pack-expand="1" for="i in range(1,100)" text="{{i}}" />
                            </ScrolledFrame>
                        </Frame>
                    </Frame>
                </Frame>
            </TopLevel>
            """
        print(" template = " + str(template))
    # fixme читает внешний XML-ный файл и перегоняем его в текст - работает
    elif Choice == 1:
        with open(xmlfile, mode='r') as XMLfile:
            template = XMLfile.read()
    # fixme DOM - парсим внешний XML-ный файл как DOM и раскладываем в сложный словарь - выдает ошибки
    elif Choice == 2:
        with minidom.parse(xmlfile) as template_from_XMLfile_as_a_DOM_by_xml_minidom:
            template = template_from_XMLfile_as_a_DOM_by_xml_minidom  # .Document - сложный словарь с корневым тэгом

        template_from_SourceXMLFile = minidom.parse(sourcexmlfile)
        root_tag = template_from_SourceXMLFile.documentElement  # становимся на корневой тэг

    # fixme SAX - вытягиваем часть внешнего XML-ного файла, начиная с указанного тэга - пока сложно, непонятно, неудобно - не работает
    elif Choice == 3:
        parser = make_parser()
        parser.setFeature(handler.feature_external_ges, True)
        template_from_XMLfile_as_a_SAX_by_xml_pulldom = pulldom.parse(stream_or_string=xmlfile, parser=parser)
        template = template_from_XMLfile_as_a_SAX_by_xml_pulldom

        template_from_SourceXMLFile = pulldom.parse(stream_or_string=sourcexmlfile, parser=parser)

    # fixme SAX - читает внешний XML-ный файл и анализируем xml как SAX - не удобно
    elif Choice == 4:
        #XMLfile = open(xmlfile, 'r')
        #XMLfile.close()
        with open(xmlfile, mode='r') as XMLfile:
            template = XMLfile.read()
        template_from_XMLfile = pulldom.parse(xmlfile)

    # fixme SAX - парсим внешний XML-ный файл, можно читать и писать XML, много документации, фабрика элементов, события - работает
    elif Choice == 5:
        tree_from_XMLfile_as_a_SAX_by_using_xml = ElementTree.parse(xmlfile)  # указатель на XML-ную структуру
        root_tag = tree_from_XMLfile_as_a_SAX_by_using_xml.getroot()  # становимся на корневой тэг
        template = ElementTree.tostring(root_tag, method='xml')  # XML-ная строка
        print(" template = " + str(template))

        tree_from_SourceXMLFile = ElementTree.parse(sourcexmlfile)  # указатель на XML-ную структуру
        source_root_tag = tree_from_SourceXMLFile.getroot()  # становимся на корневой тэг
        source = ElementTree.tostring(source_root_tag, method='xml')  # XML-ная строка
        sourceroot_tag = source_root_tag.tag  # имя корневого тэга
        sourceroot_attr = source_root_tag.attrib  # аттрибут(ы) корневого тэга в виде словаря
        #source = sourceroot.findall(".")

    # fixme SAX парсим внешний XML-ный файл как SAX - работает
    elif Choice == 6:
        template_from_XMLfile_as_a_DOM_by_using_lxml = etree.parse(xmlfile)
        template = etree.tostring(template_from_XMLfile_as_a_DOM_by_using_lxml.getroot(), pretty_print=True, method="xml")
    # SAX
    # fixme SAX парсим внешний XML-ный файл как SAX и перепаковывает в сложный словарь - выдает ошибки
    elif Choice == 7:
        template_from_XMLfile_as_a_SAX_by_using_lxml = etree.parse(xmlfile)  # сложный список с именем файла и именем корневого тэга
        template = template_from_XMLfile_as_a_SAX_by_using_lxml.getroot()  # то же и корневой аттрибут

        template_from_SourceXMLFile_by_lxml_as_SAX = etree.parse(sourcexmlfile)
        sourceroot = template_from_SourceXMLFile_by_lxml_as_SAX.getroot()
        handler = pulldom.SAX2DOM()
        sax.saxify(template_from_SourceXMLFile_by_lxml_as_SAX, handler)

    # fixme парсим внешний XML-ный файл - пока не понятно
    elif Choice == 8:
        with open(xmlfile, "r") as template_from_XMLfile_as_a_by_using_BS4:
            template = template_from_XMLfile_as_a_by_using_BS4.read()
        parsed = BeautifulSoup(template, features="lxml")  # по умолчанию lxml
        tag_Frame = parsed.TopLevel.Frame
        tags_Button = parsed.find_all('Button')
        #new_tag = y.new_tag("h1")
        #y.mail.insert(2, new_tag)
        #f = open("demo_conf_new.xml", "w")
        #f.write(y.prettify())
    # все остальное - читаем внешний INI-шный файл с помощью ConfigParser
    # fixme выдает ошибки, пока не делал файл *.ini
    else:
        # todo Обернуть в обработку исключения
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_directory, inifile)
        template_from_XMLfile_via_INI = configparser.ConfigParser()
        template_from_XMLfile_via_INI.read(config_file_path)
        template = template_from_XMLfile_via_INI.getint("1", "11")

    data = tkvue.Context({"active_view": "list",
                          "new_people_name": "",
                          "text_entry": "value",
                          "text_password": "password",
                          "people": ["Patrik", "Anna", "Michael", "Shannon", "Patrice", "Kate"],
                          "style_variable": "primary",
                          "on_off_variable": "on", })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_active_view(self, name):
        assert name in ["list", "styles", "widgets"]
        self.data.active_view = name

    def delete_people(self, name):
        people = self.data.people.copy()
        people.remove(name)
        self.data.people = people

    def add_people(self, name):
        people = self.data.people.copy()
        people.append(name)
        self.data.people = people
        self.data.new_people_name = ""


if __name__ == "__main__":
    dlg = RootDialog()
    dlg.mainloop()
