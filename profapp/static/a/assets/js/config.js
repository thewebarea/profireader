(function(angular) {
    "use strict";
    angular.module('FileManagerApp').constant("fileManagerConfig", {
        appName: "https://github.com/joni2back/angular-filemanager",
        defaultLang: "en",

        listUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        uploadUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        renameUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        copyUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        removeUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        editUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        getContentUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        createFolderUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        downloadFileUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        compressUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        extractUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",
        permissionsUrl: "/angular-filemanager/bridges/python/ctrl_filemanager.py",

        allowedActions: {
            rename: true,
            copy: true,
            edit: true,
            changePermissions: true,
            compress: true,
            compressChooseName: true,
            extract: true,
            download: true,
            preview: true,
            remove: true
        },

        enablePermissionsRecursive: true,

        isEditableFilePattern: '\\.(txt|html|htm|aspx|asp|ini|pl|py|md|php|css|js|log|htaccess|htpasswd|json|sql|xml|xslt|sh|rb|as|bat|cmd|coffee|php[3-6]|java|c|cbl|go|h|scala|vb)$',
        isImageFilePattern: '\\.(jpg|jpeg|gif|bmp|png|svg|tiff)$',
        isExtractableFilePattern: '\\.(zip|gz|tar|rar|gzip)$'
    });
})(angular);
