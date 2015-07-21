(function(angular) {
    "use strict";
    angular.module('FileManagerApp').constant("fileManagerConfig", {
        appName: "https://github.com/joni2back/angular-filemanager",
        defaultLang: "en",

        listUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        uploadUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        renameUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        copyUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        removeUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        editUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        getContentUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        createFolderUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        downloadFileUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        compressUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        extractUrl: "/filemanager/bridges/python/ctrl_filemanager.py",
        permissionsUrl: "/filemanager/bridges/python/ctrl_filemanager.py",

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
