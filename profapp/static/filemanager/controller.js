(function(window, angular, $) {
    "use strict";
    angular.module('FileManagerApp').controller('FileManagerCtrl', [
    '$scope', '$translate', '$cookies', 'fileManagerConfig', 'item', 'fileNavigator', 'fileUploader',
    function($scope, $translate, $cookies, fileManagerConfig, Item, FileNavigator, fileUploader) {

        $scope.config = fileManagerConfig;
        $scope.appName = fileManagerConfig.appName;
        $scope.orderProp = ['model.type', 'model.name'];
        $scope.query = '';
        $scope.temp = new Item();
        $scope.fileNavigator = new FileNavigator(_.keys(library)[0], file_manager_called_for);
        $scope.fileUploader = fileUploader;
        $scope.uploadFileList = [];
        $scope.viewTemplate = $cookies.viewTemplate || 'main-table.html';
        $scope.error = error;
        $scope.rootdirs = library;
        $scope.file_manager_called_for = file_manager_called_for;
        $scope.file_manager_on_action = file_manager_on_action;
        $scope.root_id = '';
        $scope.root_name = '';

        $scope.setTemplate = function(name) {
            $scope.viewTemplate = $cookies.viewTemplate = name;
        };

        $scope.changeRoot = function (root_id, root_name) {
            $scope.fileNavigator.setRoot(root_id);
            $scope.root_name = root_name;
        };

        $scope.touch = function(item) {
            item = item instanceof Item ? item : new Item();
            item.revert && item.revert();
            $scope.temp = item;
        };

        $scope.smartClick = function(item) {
            if (item.isFolder()) {
                return $scope.fileNavigator.folderClick(item);
            }
            if (item.isImage()) {
                return item.preview();
            }
            if (item.isEditable()) {
                item.getContent();
                $scope.touch(item);
                $('#edit').modal('show');
                return;
            }
        };

        $scope.isInThisPath = function(path) {
            var currentPath = $scope.fileNavigator.currentPath.join('/');
            return currentPath.indexOf(path) !== -1;
        };

        $scope.edit = function(item) {
            item.edit(function() {
                $('#edit').modal('hide');
            });
        };

        $scope.changePermissions = function(item) {
            item.changePermissions(function() {
                $('#changepermissions').modal('hide');
            });
        };

        $scope.copy = function(item) {
            var samePath = item.tempModel.path.join() === item.model.path.join();
            if (samePath && $scope.fileNavigator.fileNameExists(item.tempModel.name)) {
                item.error = $translate.instant('error_invalid_filename');
                return false;
            }
            item.copy(function() {
                $scope.fileNavigator.refresh();
                $('#copy').modal('hide');
            });
        };

        $scope.compress = function(item) {
            item.compress(function() {
                item.success = true;
                $scope.fileNavigator.refresh();
            }, function() {
                item.success = false;
            });
        };

        $scope.extract = function(item) {
            item.extract(function() {
                item.success = true;
                $scope.fileNavigator.refresh();
            }, function() {
                item.success = false;
            });
        };

        $scope.remove = function(item) {
            item.remove(function() {
                $scope.fileNavigator.refresh();
                $('#delete').modal('hide');
            });
        };

        $scope.rename = function(item) {
            var samePath = item.tempModel.path.join() === item.model.path.join();
            if (samePath && $scope.fileNavigator.fileNameExists(item.tempModel.name)) {
                item.error = $translate.instant('error_invalid_filename');
                return false;
            }
            item.rename(function() {
                $scope.fileNavigator.refresh();
                $('#rename').modal('hide');
            });
        };

        $scope.createFolder = function(item) {
            var name = item.tempModel.name && item.tempModel.name.trim();
            item.tempModel.type = 'dir';
            item.tempModel.path = $scope.fileNavigator.currentPath;
            item.tempModel.root_id = $scope.fileNavigator.root_id;
            item.tempModel.folder_id = $scope.fileNavigator.getCurrentFolder();

            if (name && !$scope.fileNavigator.fileNameExists(name)) {
                item.createFolder(function() {
                    $scope.fileNavigator.refresh();
                    $('#newfolder').modal('hide');
                });
            } else {
                $scope.temp.error = $translate.instant('error_invalid_filename');
                return false;
            }
        };

        $scope.take_action = function(item, actionname) {
            if ($scope.file_manager_on_action[actionname]) {
                try {
                    eval($scope.file_manager_on_action[actionname] + '(item);');
                }
                catch(e) {

                }
            }
        };

        $scope.can_action = function(item, actionname, defaultpermited) {
            if (actionname === 'paste') {
            if (defaultpermited === true) {
                return ($scope.copied_files.length > 0)
                }
            }
            return defaultpermited
            };

        $scope.uploadFiles = function() {
            $scope.fileUploader.upload($scope.uploadFileList, $scope.fileNavigator.currentPath,
                $scope.fileNavigator.root_id, $scope.fileNavigator.getCurrentFolder()).success(function() {
                $scope.fileNavigator.refresh();
                $('#uploadfile').modal('hide');
            }).error(function(data) {
                var errorMsg = data.result && data.result.error || $translate.instant('error_uploading_files');
                $scope.temp.error = errorMsg;
            });
        };


        $scope.getQueryParam = function(param) {
            var found;
            window.location.search.substr(1).split("&").forEach(function(item) {
                if (param ===  item.split("=")[0]) {
                    found = item.split("=")[1];
                    return false;
                }
            });
            return found;
        };
        $scope.dis = "cursor: default;pointer-events: none;color: gainsboro;"
        $scope.isDisable = function(){
          return $scope.fileManagerConfig.disabled;
        };

        $scope.err = function(){
            if ($scope.error == 'False' && $scope.rootdirs.length != 0){
                return false;
            }else{
                return true;
            }
        };

        $scope.changeRoots = function(){
            if(error == 'False'){
                $scope.changeRoot(_.keys($scope.rootdirs)[0], _.values($scope.rootdirs)[0]['name'])
            }else{
                $scope.changeRoot('','')
            }
        };

        $scope.errMsg = "You do not belong to any company!";
        $scope.changeRoots();//(_.keys($scope.rootdirs)[0], _.values($scope.rootdirs)[0]['name']);
        $scope.isWindows = $scope.getQueryParam('server') === 'Windows';
        $scope.fileNavigator.refresh();

    }]);
})(window, angular, jQuery);
