#-*- coding:utf-8 -*-
#----------------------------------------
# Purpose: 简单功能实现，与控件耦合
#  Author: puwow
#   CDate: 2017.11.05
#----------------------------------------

import os
import bs4
from bs4 import BeautifulSoup

class SimpleMaven( object ):
    #简单Maven类，对Maven公共信息的封装
    def __init__( self, mavenHome=None ):
        self._mavenHome = mavenHome
    def isInstallMaven( self ):
        #判断系统是否安装了Maven
        return os.environ.get("MAVEN_HOME") is not None \
                or os.environ.get("M2_HOME") is not None
    def getMavenHome( self ):
        #返回Maven的安装目录
        if self.isInstallMaven():
            return os.environ.get("MAVEN_HOME",os.environ.get("M2_HOME",None))
        return None
    def parseTree( self, controls, xmlFile=None ):
        if xmlFile is None and controls is not None:
            root = controls.AddRoot("Maven")
            phase = ['创建项目', '编译', '测试', '打包', '发布']
            for item in phase:
                controls.AppendItem( root, item )
        else:
            if os.path.exists(xmlFile):
                soup = BeautifulSoup( open(xmlFile).read(), 'lxml' )
                root = controls.AddRoot(soup.root['name'], data=soup.root.get('desc'))
                for phase in soup.root.children:
                    if type(phase) is bs4.Tag:
                        phase_node = controls.AppendItem( root, phase['name'], data=phase.get('desc') )
                        for plugin in phase.plugins.children:
                            if type(plugin) is bs4.Tag:
                                plugin_node = controls.AppendItem( phase_node, plugin['name'], data=plugin.get('desc') )
                                for goal in plugin.goals.children:
                                    if type(goal) is bs4.Tag:
                                        goal_node = controls.AppendItem( plugin_node, goal['name'], data=goal.get('desc') )
                controls.Expand(root)
