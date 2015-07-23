(function(angular) {
    "use strict";
    angular.module('FileManagerApp').constant("fileManagerConfig", {
        appName: "https://github.com/joni2back/angular-filemanager",
        defaultLang: "en",

        listUrl: "/filemanager",
        uploadUrl: "/filemanager",
        renameUrl: "/filemanager",
        copyUrl: "/filemanager",
        removeUrl: "/filemanager",
        editUrl: "/filemanager",
        getContentUrl: "/filemanager",
        createFolderUrl: "/filemanager",
        downloadFileUrl: "/filemanager",
        compressUrl: "/filemanager",
        extractUrl: "/filemanager",
        permissionsUrl: "/filemanager",

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
