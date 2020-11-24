# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MsdcClient
                                 QGIS plugin
 MSDC QGIS Client
                              -------------------
        begin                : 2019-10-17
        git sha              : $Format:%H$
        copyright            : (C) 2019 by RCMRD
        email                : rcmrd@rcmrd.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QMessageBox, QFileDialog, QListWidget

from qgis.core import QgsDataSourceUri
import db_manager.db_plugins.postgis.connector as pgconn

# Initialize Qt resources from file resources.py
from .resources import *

# import tools
from .tools import *

# Import the code for the DockWidget
from .msdc_client_dockwidget import MsdcClientDockWidget
from .login_diag import Ui_LoginDialog
from .import_diag import Ui_importDiag
from .exportdata_diag import Ui_exportdataDiag
from .imagery_diag import Ui_imageryDiag
import os.path



class MsdcClient:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MsdcClient_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MSDC Client')

        self.toolbar = self.iface.addToolBar(u'MsdcClient')
        self.toolbar.setObjectName(u'MsdcClient')

        #print "** INITIALIZING MsdcClient"

        self.pluginIsActive = False
        self.dockwidget = None
        self.logindiag = None
        self.importdiag = None
        self.exportdiag = None
        self.imagerydiag = None
        self.exportdir = None

        # default database settings
        self.username = "postgres"
        self.password = "postgres"
        self.host = "localhost"
        self.port = "5432"
        self.db = "msdc"

        self.workingdir = ":/plugins/msdc_client/data/"


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MsdcClient', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/msdc_client/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MSDC Client'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING MsdcClient"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD MsdcClient"

        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&MSDC Client'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def show_loginDiag(self):
        self.loginDialog.show()

    def show_importDiag(self):
        self.importDialog.show()

    def show_exportDiag(self):
        self.exportDialog.show()

    def login_action(self):
        self.username = self.logindiag.txtUsername.text()
        self.password = self.logindiag.txtPassword.text()
        self.host = self.logindiag.txtHost.text()
        self.port = self.logindiag.txtPort.text()
        self.db = self.logindiag.txtDb.text()

        try:
            uri = QgsDataSourceUri()
            #uri.setConnection("localhost", "5432", "stdm", "postgres", "postgres")
            uri.setConnection(self.host, self.port, self.db, self.username, self.password)
            conn = pgconn.PostGisDBConnector(uri)
            dbtables = conn.getTables()
            if len(dbtables) > 0:
                msg = QMessageBox()
                msg.setWindowTitle("Message")
                msg.setText("Login Successful")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.loginDialog.close()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Message")
                msg.setText("Login Error")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Message")
            msg.setText("Login Error")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def browse_imports(self):
        self.importfiles = QFileDialog.getOpenFileNames(self.importDialog,"Select Geojson Import files",self.workingdir, "Geojson files (*.geojson)")
        self.importdiag.importList.addItems(self.importfiles[0])
        self.importdiag.recordsFound.setText(str(self.importdiag.importList.count()))
        #if self.importdiag:
        #    self.importdiag.importDir.setText(self.importfile)

    def remove_selected(self):
        self.importdiag.importList.takeItem(self.importdiag.importList.currentRow())
        self.importdiag.recordsFound.setText(str(self.importdiag.importList.count()))

    def clear_export_list(self):
        if self.exportdiag.exportList.count() > 0:
            self.exportdiag.exportList.clear()
            self.exportdiag.recordSelected.setText("0")

    def clear_list(self):
        if self.importdiag.importList.count() > 0:
            self.importdiag.importList.clear()
            self.importdiag.recordsFound.setText(str(self.importdiag.importList.count()))

    def import_mobiledata(self):
        if self.importdiag.importList.count() > 0:
            import_files = []
            import_msg_list = []
            for i in range(self.importdiag.importList.count()):
                import_files.append(self.importdiag.importList.item(i))

            for _importfile in import_files:
                db_settings = {
                    "host": self.host,
                    "port": self.port,
                    "database": self.db,
                    "user": self.username,
                    "pass": self.password
                }
                import_msg = parse_geojson(self.plugin_dir, _importfile.text(), db_settings)
                import_msg_list.append(import_msg)

            msg = QMessageBox()
            msg.setWindowTitle("Message")
            #msg.setText("Tablet Data Imported")
            msg.setText(' '.join(map(str, import_msg_list)))
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

            self.clear_list()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Missing files to import")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def browse_exports(self):
        self.exportdir = QFileDialog.getExistingDirectory(self.exportDialog, "Select Directory to export files")
        if self.exportdir:
            self.exportdiag.destination.setText(self.exportdir)

    def export_mobiledata(self):
        if self.exportdir == None:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Export Directory not set")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        else:
            layer = self.iface.activeLayer()
            db_settings = {
                "host": self.host,
                "port": self.port,
                "database": self.db,
                "user": self.username,
                "pass": self.password
            }
            if layer:
                if layer.name() == 'parcels':
                    features = layer.selectedFeatures()
                    if len(features) > 0:
                        self.exportdiag.recordSelected.setText(str(len(features)))
                        for feature in features:
                            exported = export_feature(self.exportdir, self.plugin_dir, feature, db_settings)
                            self.exportdiag.exportList.addItem(exported)

                        msg = QMessageBox()
                        msg.setWindowTitle("Message")
                        msg.setText("Tablet Data Exported")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("No features selected")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setText("Parcel layer not loaded")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Parcel layer not active")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()



    def exit_logindiag(self):
        self.loginDialog.close()

    def exit_importdiag(self):
        self.importDialog.close()

    def exit_exportdiag(self):
        self.exportDialog.close()


    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING MsdcClient"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = MsdcClientDockWidget()

            self.dockwidget.loginBtn.clicked.connect(self.show_loginDiag)
            self.dockwidget.importBtn.clicked.connect(self.show_importDiag)
            self.dockwidget.exportBtn.clicked.connect(self.show_exportDiag)
            #self.dockwidget.imageryBtn.clicked.connect(self.showImageryDiag)

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            if self.logindiag == None:
                self.loginDialog = QDialog()
                self.logindiag = Ui_LoginDialog()
                self.logindiag.setupUi(self.loginDialog)

                self.loginbtn = self.logindiag.loginBtn2
                self.loginbtn.clicked.connect(self.login_action)

                self.exitBtn = self.logindiag.exitBtn2
                self.exitBtn.clicked.connect(self.exit_logindiag)

            if self.importdiag == None:
                self.importDialog = QDialog()
                self.importdiag = Ui_importDiag()
                self.importdiag.setupUi(self.importDialog)

                # browse button
                self.browsebtn = self.importdiag.browseBtn1
                self.browsebtn.clicked.connect(self.browse_imports)

                # exit button
                self.closeBtn = self.importdiag.closeBtn2
                self.closeBtn.clicked.connect(self.exit_importdiag)

                # remove selected button
                self.removeBtn = self.importdiag.removeBtn
                self.removeBtn.clicked.connect(self.remove_selected)

                # clear list button
                self.clearBtn = self.importdiag.clearBtn
                self.clearBtn.clicked.connect(self.clear_list)

                # import data button
                self.importBtn2 = self.importdiag.importBtn2
                self.importBtn2.clicked.connect(self.import_mobiledata)


            if self.exportdiag == None:
                self.exportDialog = QDialog()
                self.exportdiag = Ui_exportdataDiag()
                self.exportdiag.setupUi(self.exportDialog)

                # browse button
                self.browseExports = self.exportdiag.browseExports
                self.browseExports.clicked.connect(self.browse_exports)

                # exit button
                self.cancelBtn = self.exportdiag.cancelBtn
                self.cancelBtn.clicked.connect(self.exit_exportdiag)

                # clear list button
                self.clearExports = self.exportdiag.clearExports
                self.clearExports.clicked.connect(self.clear_export_list)

                # export data button
                self.exportBtn = self.exportdiag.exportBtn
                self.exportBtn.clicked.connect(self.export_mobiledata)

            if self.imagerydiag == None:
                self.imageryDialog = QDialog()
                self.imagerydiag = Ui_imageryDiag()
                self.imagerydiag.setupUi(self.imageryDialog)
