angular.module("FileManagerApp").run(["$templateCache", function($templateCache) {$templateCache.put("assets/templates/current-folder-breadcrumb.html","<ol class=\"breadcrumb mb0\">\n    <!--<li>\n        <a href=\"\" data-ng-click=\"fileNavigator.goTo(-1)\">\n            <i class=\"glyphicon glyphicon-folder-open mr2\"></i>\n        </a>\n    </li>-->\n    <li data-ng-repeat=\"(key, item) in fileNavigator.breadCrumbs track by key\" data-ng-class=\"{\'active\':$last}\" class=\"animated fast fadeIn\">\n        <a href=\"\" data-ng-click=\"fileNavigator.goTo(key)\">\n            <i class=\"glyphicon glyphicon-folder-open mr2\"></i> {{item.model.name}}\n        </a>\n    </li>\n    <li><button class=\"btn btn-primary btn-xs\" data-ng-click=\"fileNavigator.upDir()\">&crarr;</button></li>\n</ol>");
$templateCache.put("assets/templates/index.html","<div data-ng-controller=\"FileManagerCtrl\">\n    <div ng-include=\"config.tplPath + \'/navbar.html\'\"></div>\n\n    <div class=\"container-fluid\">\n        <div class=\"row\">\n\n            <div class=\"col-sm-3 col-md-2 sidebar file-tree\" ng-include=\"config.tplPath + \'/sidebar.html\'\"></div>\n            <div class=\"col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main\">\n                <div ng-include=\"config.tplPath + \'/current-folder-breadcrumb.html\'\"></div>\n                <div ng-include=\"config.tplPath + \'/\' + viewTemplate\" class=\"main-navigation\"></div>\n            </div>\n        </div>\n    </div>\n\n    <div ng-include=\"config.tplPath + \'/modals.html\'\"></div>\n    <div ng-include=\"config.tplPath + \'/item-context-menu.html\'\"></div>\n</div>");
$templateCache.put("assets/templates/item-context-menu.html","<div id=\"context-menu\" class=\"dropdown clearfix animated fast fadeIn\">\n    <ul class=\"dropdown-menu dropdown-right-click\" role=\"menu\" aria-labelledby=\"dropdownMenu\" style=\"\">\n        <li data-ng-show=\"config.allowedActions.rename && (temp.model.actions.indexOf(\'rename\')>-1)\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#rename\"><i class=\"glyphicon glyphicon-edit\"></i> {{\'rename\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.copy && !temp.isFolder() && (temp.model.actions.indexOf(\'copy\')>-1)\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#copy\"><i class=\"glyphicon glyphicon-log-out\"></i> {{\'copy\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.edit && temp.isEditable()\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#edit\" data-ng-click=\"temp.getContent();\"><i class=\"glyphicon glyphicon-pencil\"></i> {{\'edit\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.changePermissions\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#changepermissions\"><i class=\"glyphicon glyphicon-lock\"></i> {{\'permissions\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.compress && temp.isCompressible()\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#compress\"><i class=\"glyphicon glyphicon-compressed\"></i> {{\'compress\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.extract && temp.isExtractable()\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#extract\" data-ng-click=\"temp.tempModel.name=\'\'\"><i class=\"glyphicon glyphicon-export\"></i> {{\'extract\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.download && !temp.isFolder() && (temp.model.actions.indexOf(\'download\')>-1)\"><a href=\"\" tabindex=\"-1\" data-ng-click=\"temp.download()\"><i class=\"glyphicon glyphicon-download\"></i> {{\'download\' | translate}}</a></li>\n        <li data-ng-show=\"config.allowedActions.preview && temp.isImage()\"><a href=\"\" tabindex=\"-1\" data-ng-click=\"temp.preview()\"><i class=\"glyphicon glyphicon-picture\"></i> {{\'view_item\' | translate}}</a></li>\n        <li class=\"divider\"></li>\n        <li data-ng-show=\"config.allowedActions.remove && (temp.model.actions.indexOf(\'delete\')>-1)\"><a href=\"\" tabindex=\"-1\" data-toggle=\"modal\" data-target=\"#delete\"><i class=\"glyphicon glyphicon-trash\"></i> {{\'remove\' | translate}}</a></li>\n    </ul>\n</div>");
$templateCache.put("assets/templates/item-toolbar.html","<div data-ng-show=\"!item.inprocess\">\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#rename\" data-ng-show=\"config.allowedActions.rename && (item.model.actions.indexOf(\'rename\')>-1)\" data-ng-click=\"touch(item)\" title=\"{{\'rename\' | translate}}\">\n        <i class=\"glyphicon glyphicon-edit\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#copy\" data-ng-show=\"config.allowedActions.copy && !item.isFolder() && (item.model.actions.indexOf(\'copy\')>-1)\" data-ng-click=\"touch(item)\" title=\"{{\'copy\' | translate}}\">\n        <i class=\"glyphicon glyphicon-log-out\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#edit\" data-ng-show=\"config.allowedActions.edit && item.isEditable()\" data-ng-click=\"item.getContent(); touch(item)\" title=\"{{\'edit\' | translate}}\">\n        <i class=\"glyphicon glyphicon-pencil\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#changepermissions\" data-ng-show=\"config.allowedActions.changePermissions\" data-ng-click=\"touch(item)\" title=\"{{\'permissions\' | translate}}\">\n        <i class=\"glyphicon glyphicon-lock\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#compress\" data-ng-show=\"config.allowedActions.compress && item.isCompressible()\" data-ng-click=\"touch(item)\" title=\"{{\'compress\' | translate}}\">\n        <i class=\"glyphicon glyphicon-compressed\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-toggle=\"modal\" data-target=\"#extract\" data-ng-show=\"config.allowedActions.extract && item.isExtractable()\" data-ng-click=\"touch(item); item.tempModel.name=\'\'\" title=\"{{\'extract\' | translate}}\">\n        <i class=\"glyphicon glyphicon-export\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-ng-show=\"config.allowedActions.download && !item.isFolder() && (item.model.actions.indexOf(\'download\')>-1)\" data-ng-click=\"item.download()\" title=\"{{\'download\' | translate}}\">\n        <i class=\"glyphicon glyphicon-cloud-download\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-default\" data-ng-show=\"config.allowedActions.preview && item.isImage()\" data-ng-click=\"item.preview()\" title=\"{{\'view_item\' | translate}}\">\n        <i class=\"glyphicon glyphicon-picture\"></i>\n    </button>\n    <button class=\"btn btn-sm btn-danger\" data-toggle=\"modal\" data-target=\"#delete\" ng-show=\"config.allowedActions.remove && (item.model.actions.indexOf(\'delete\')>-1)\" data-ng-click=\"touch(item)\" title=\"{{\'remove\' | translate}}\">\n        <i class=\"glyphicon glyphicon-trash\"></i>\n    </button>\n</div>\n<div data-ng-show=\"item.inprocess\">\n    <button class=\"btn btn-sm\" style=\"visibility: hidden\">&nbsp;</button><span class=\"label label-warning\">{{\"wait\" | translate}} ...</span>\n</div>");
$templateCache.put("assets/templates/main-icons.html","<div class=\"iconset\">\n    <div class=\"col-120\" data-ng-repeat=\"item in fileNavigator.fileList | filter: query | orderBy: orderProp\" data-ng-show=\"!fileNavigator.requesting && !fileNavigator.error\">\n        <a href=\"\" class=\"thumbnail text-center\" data-ng-click=\"smartClick(item)\" ng-right-click=\"smartRightClick(item)\" title=\"{{item.model.name}} ({{item.model.sizeKb()}}kb)\">\n            <div class=\"item-icon\">\n                <i class=\"glyphicon glyphicon-folder-open\" data-ng-show=\"item.model.type === \'dir\'\"></i>\n                <i class=\"glyphicon glyphicon-file\" data-ng-show=\"item.model.type === \'file\'\"></i>\n            </div>\n            {{item.model.name | strLimit : 11 }}\n        </a>\n    </div>\n    <div class=\"alert alert-warning\" data-ng-show=\"fileNavigator.requesting\">\n        {{\"loading\" | translate}}...\n    </div>\n    <div class=\"alert alert-warning\" data-ng-show=\"!fileNavigator.requesting && fileNavigator.fileList.length < 1 && !fileNavigator.error\">\n        {{\"no_files_in_folder\" | translate}}...\n    </div>\n    <div class=\"alert alert-danger\" data-ng-show=\"!fileNavigator.requesting && fileNavigator.error\">\n        {{ fileNavigator.error }}\n    </div>\n</div>");
$templateCache.put("assets/templates/main-table-modal.html","<table class=\"table table-striped table-hover mb0 table-files\">\n    <thead>\n        <tr>\n            <th>{{\"name\" | translate}}</th>\n            <th class=\"hidden-sm hidden-xs\">{{\"date\" | translate}}</th>\n            <th class=\"text-right\">{{\"actions\" | translate}}</th>\n        </tr>\n    </thead>\n    <tbody class=\"file-item\">\n        <tr data-ng-show=\"fileNavigator.requesting\">\n            <td colspan=\"3\">\n                {{\"loading\" | translate}}...\n            </td>\n        </tr>\n        <tr data-ng-show=\"!fileNavigator.requesting && !fileNavigator.listHasFolders() && !fileNavigator.error\">\n            <td colspan=\"2\">\n                {{\"no_folders_in_folder\" | translate}}...\n            </td>\n            <td class=\"text-right\">\n                <button class=\"btn btn-sm btn-default\" data-ng-click=\"fileNavigator.upDir()\">{{\"go_back\" | translate}}</button>\n            </td>\n        </tr>\n        <tr data-ng-show=\"!fileNavigator.requesting && fileNavigator.error\">\n            <td colspan=\"3\">\n                {{ fileNavigator.error }}\n            </td>\n        </tr>\n        <tr data-ng-repeat=\"item in fileNavigator.fileList | orderBy: orderProp\" data-ng-show=\"!fileNavigator.requesting && item.model.type === \'dir\'\">\n            <td>\n                <a href=\"\" data-ng-click=\"fileNavigator.folderClick(item)\" title=\"{{item.model.name}} ({{item.model.sizeKb()}}kb)\">\n                    <i class=\"glyphicon glyphicon-folder-close\"></i>\n                    {{item.model.name | strLimit : 32}}\n                </a>\n            </td>\n            <td class=\"hidden-sm hidden-xs\">\n                {{item.model.date.toString()}}\n            </td>\n            <td class=\"text-right\">\n                <button class=\"btn btn-sm btn-default\" data-ng-click=\"select(item, temp)\"><i class=\"glyphicon glyphicon-hand-up\"></i> {{\"select_this\" | translate}}</button>\n            </td>\n        </tr>\n    </tbody>\n</table>");
$templateCache.put("assets/templates/main-table.html","<table class=\"table table-striped table-hover mb0 table-files\">\n    <thead>\n        <tr>\n            <th>{{\"name\" | translate}}</th>\n            <th class=\"hidden-xs\">{{\"size\" | translate}}</th>\n            <th class=\"hidden-sm hidden-xs\">{{\"date\" | translate}}</th>\n            <th class=\"hidden-sm hidden-xs\">{{\"chosen\" | translate}}</th>\n            <th class=\"hidden-sm hidden-xs\">{{\"permissions\" | translate}}</th>\n            <th class=\"text-right\">{{\"actions\" | translate}}</th>\n        </tr>\n    </thead>\n    <tbody class=\"file-item\">\n        <tr data-ng-show=\"fileNavigator.requesting\">\n            <td colspan=\"5\">\n                {{\"loading\" | translate}}...\n            </td>\n        </tr>\n        <tr data-ng-show=\"!fileNavigator.requesting && fileNavigator.mainList.length < 1 && !fileNavigator.error\">\n            <td colspan=\"5\">\n                {{\"no_files_in_folder\" | translate}}...\n            </td>\n        </tr>\n        <tr data-ng-show=\"!fileNavigator.requesting && fileNavigator.error\">\n            <td colspan=\"5\">\n                {{ fileNavigator.error }}\n            </td>\n        </tr>\n        <tr data-ng-repeat=\"item in fileNavigator.mainList | filter: query | orderBy: orderProp\" data-ng-show=\"!fileNavigator.requesting\">\n            <td>\n                <a href=\"\" data-ng-click=\"smartClick(item)\" ng-right-click=\"smartRightClick(item)\" title=\"{{item.model.name}} ({{item.model.sizeKb()}}kb)\">\n                    <i class=\"glyphicon glyphicon-folder-close\" data-ng-show=\"item.model.type === \'dir\'\"></i>\n                    <i class=\"glyphicon glyphicon-file\" data-ng-show=\"item.model.type === \'file\'\"></i>\n                    {{item.model.name | strLimit : 64}}\n                </a>\n            </td>\n            <td class=\"hidden-xs\">\n                {{item.model.sizeKb()}}kb\n            </td>\n            <td class=\"hidden-sm hidden-xs\">\n                {{item.model.date.toString()}}\n            </td>\n            <td class=\"hidden-sm hidden-xs\">\n                <input type=\"checkbox\" data-ng-model=\"item.model.chosen\" data-ng-click=\"fileNavigator.choose(item)\" />\n            </td>\n            <td class=\"hidden-sm hidden-xs\">\n                {{item.model.perms.toCode(item.model.type === \'dir\'?\'d\':\'-\')}}\n            </td>\n            <td class=\"text-right\">\n                <div ng-include=\"config.tplPath + \'/item-toolbar.html\'\"></div>\n            </td>\n        </tr>\n    </tbody>\n</table>");
$templateCache.put("assets/templates/modals.html","<div class=\"modal animated fadeIn\" id=\"delete\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n    <form data-ng-submit=\"remove(temp)\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n            <span aria-hidden=\"true\">&times;</span>\n            <span class=\"sr-only\">{{\"close\" | translate}}</span>\n        </button>\n        <h4 class=\"modal-title\">{{\"confirm\" | translate}}</h4>\n      </div>\n      <div class=\"modal-body\">\n        {{\'sure_to_delete\' | translate}} <b>{{temp.model.name}}</b> ?\n        <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n        <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\" autofocus=\"autofocus\">{{\"remove\" | translate}}</button>\n      </div>\n      </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"rename\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"rename(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'change_name_move\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <label class=\"radio\">{{\'enter_new_name_for\' | translate}} <b>{{temp.model.name}}</b></label>\n              <input class=\"form-control\" data-ng-model=\"temp.tempModel.name\" autofocus=\"autofocus\">\n\n              <div data-ng-include data-src=\"\'path-selector\'\" class=\"clearfix\"></div>\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n              <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">{{\'rename\' | translate}}</button>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"copy\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"copy(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'copy_file\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <label class=\"radio\">{{\'enter_new_name_for\' | translate}} <b>{{temp.model.name}}</b></label>\n              <input class=\"form-control\" data-ng-model=\"temp.tempModel.name\" autofocus=\"autofocus\">\n\n              <div data-ng-include data-src=\"\'path-selector\'\" class=\"clearfix\"></div>\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n              <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">Copy</button>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"compress\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"compress(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'compress\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <div ng-show=\"temp.success\">\n                  <div class=\"label label-success error-msg\">{{\'compression_started\' | translate}}</div>\n              </div>\n              <div ng-hide=\"temp.success\">\n                  <div ng-hide=\"config.allowedActions.compressChooseName\">\n                    {{\'sure_to_start_compression_with\' | translate}} <b>{{temp.model.name}}</b> ?\n                  </div>\n                  <div ng-show=\"config.allowedActions.compressChooseName\">\n                    <label class=\"radio\">{{\'enter_folder_name_for_compression\' | translate}} <b>{{fileNavigator.currentPath.join(\'/\')}}/{{temp.model.name}}</b></label>\n                    <input class=\"form-control\" data-ng-model=\"temp.tempModel.name\" autofocus=\"autofocus\">\n                  </div>\n              </div>\n\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <div ng-show=\"temp.success\">\n                  <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"close\" | translate}}</button>\n              </div>\n              <div ng-hide=\"temp.success\">\n                  <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n                  <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">{{\'compress\' | translate}}</button>\n              </div>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"extract\" ng-init=\"temp.emptyName()\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"extract(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'extract_item\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <div ng-show=\"temp.success\">\n                  <div class=\"label label-success error-msg\">{{\'extraction_started\' | translate}}</div>\n              </div>\n              <div ng-hide=\"temp.success\">\n                  <label class=\"radio\">{{\'enter_folder_name_for_extraction\' | translate}} <b>{{temp.model.name}}</b></label>\n                  <input class=\"form-control\" data-ng-model=\"temp.tempModel.name\" autofocus=\"autofocus\">\n                  <div data-ng-include data-src=\"\'path-selector\'\" class=\"clearfix\"></div>\n              </div>\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <div ng-show=\"temp.success\">\n                  <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"close\" | translate}}</button>\n              </div>\n              <div ng-hide=\"temp.success\">\n                  <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n                  <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">{{\'extract\' | translate}}</button>\n              </div>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"edit\" data-ng-class=\"{\'modal-fullscreen\': fullscreen}\">\n  <div class=\"modal-dialog modal-lg\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"edit(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <button type=\"button\" class=\"close mr5\" data-ng-click=\"fullscreen=!fullscreen\">\n                  <span>&loz;</span>\n                  <span class=\"sr-only\">{{\'toggle_fullscreen\' | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'edit_file\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n                <label class=\"radio\">{{\'file_content\' | translate}}</label>\n                <span class=\"label label-warning\" data-ng-show=\"temp.inprocess\">{{\'loading\' | translate}} ...</span>\n                <textarea class=\"form-control code\" data-ng-model=\"temp.tempModel.content\" data-ng-show=\"!temp.inprocess\" autofocus=\"autofocus\"></textarea>\n                <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n              <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">{{\'edit\' | translate}}</button>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"newfolder\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"createFolder(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'create_folder\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <label class=\"radio\">{{\'folder_name\' | translate}}</label>\n              <input class=\"form-control\" data-ng-model=\"temp.tempModel.name\" autofocus=\"autofocus\">\n                <input class=\"form-control\" data-ng-model=\"temp.tempModel.description\">\n                <input class=\"form-control\" data-ng-model=\"temp.tempModel.description\">\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"cancel\" | translate}}</button>\n              <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"temp.inprocess\">{{\'create\' | translate}}</button>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"uploadfile\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"uploadFiles()\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\"upload_file\" | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <label class=\"radio\">{{\"files_will_uploaded_to\" | translate}} <b>{{fileNavigator.currentPath.join(\'/\')}}</b></label>\n              <input type=\"file\" class=\"form-control\" data-ng-file=\"$parent.uploadFileList\" autofocus=\"autofocus\" multiple=\"multiple\"/>\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <div data-ng-show=\"!fileUploader.requesting\">\n                  <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\">{{\"cancel\" | translate}}</button>\n                  <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"!uploadFileList.length || fileUploader.requesting\">{{\'upload\' | translate}}</button>\n              </div>\n              <div data-ng-show=\"fileUploader.requesting\">\n                  <span class=\"label label-warning\">{{\"uploading\" | translate}} ...</span>\n              </div>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"changepermissions\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n        <form data-ng-submit=\"changePermissions(temp)\">\n            <div class=\"modal-header\">\n              <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n                  <span aria-hidden=\"true\">&times;</span>\n                  <span class=\"sr-only\">{{\"close\" | translate}}</span>\n              </button>\n              <h4 class=\"modal-title\">{{\'change_permissions\' | translate}}</h4>\n            </div>\n            <div class=\"modal-body\">\n              <table class=\"table table-striped table-bordered table-hover mb0\">\n                  <thead>\n                      <tr>\n                          <th>{{\'permissions\' | translate}}</th>\n                          <th class=\"col-xs-1 text-center\">{{\'exec\' | translate}}</th>\n                          <th class=\"col-xs-1 text-center\">{{\'read\' | translate}}</th>\n                          <th class=\"col-xs-1 text-center\">{{\'write\' | translate}}</th>\n                      </tr>\n                  </thead>\n                  <tbody>\n                      <tr data-ng-repeat=\"(permTypeKey, permTypeValue) in temp.tempModel.perms\">\n                          <td>{{permTypeKey | translate}}</td>\n                          <td data-ng-repeat=\"(permKey, permValue) in permTypeValue\" class=\"col-xs-1 text-center\" ng-click=\"main()\">\n                              <label class=\"col-xs-12\">\n                                <input type=\"checkbox\" ng-model=\"temp.tempModel.perms[permTypeKey][permKey]\">\n                              </label>\n                          </td>\n                      </tr>\n                </tbody>\n              </table>\n              <div class=\"checkbox\" ng-show=\"config.enablePermissionsRecursive && temp.model.type === \'dir\'\">\n                <label>\n                  <input type=\"checkbox\" ng-model=\"temp.tempModel.recursive\"> {{\'recursive\' | translate}}\n                </label>\n              </div>\n              <div class=\"clearfix mt10\">\n                  <span class=\"badge pull-left\">\n                    {{\'original\' | translate}}: {{temp.model.perms.toCode(temp.model.type === \'dir\'?\'d\':\'-\')}} ({{temp.model.perms.toOctal()}})\n                  </span>\n                  <span class=\"badge pull-right\">\n                    {{\'changes\' | translate}}: {{temp.tempModel.perms.toCode(temp.model.type === \'dir\'?\'d\':\'-\')}} ({{temp.tempModel.perms.toOctal()}})\n                  </span>\n              </div>\n              <div data-ng-include data-src=\"\'error-bar\'\" class=\"clearfix\"></div>\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\">{{\"cancel\" | translate}}</button>\n              <button type=\"submit\" class=\"btn btn-sm btn-primary\" data-ng-disabled=\"\">{{\'change\' | translate}}</button>\n            </div>\n        </form>\n    </div>\n  </div>\n</div>\n\n<div class=\"modal animated fadeIn\" id=\"selector\" data-ng-controller=\"ModalFileManagerCtrl\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close\" data-dismiss=\"modal\">\n            <span aria-hidden=\"true\">&times;</span>\n            <span class=\"sr-only\">{{\"close\" | translate}}</span>\n        </button>\n        <h4 class=\"modal-title\">{{\"select_destination_folder\" | translate}}</h4>\n      </div>\n      <div class=\"modal-body\">\n        <div>\n            <div ng-include=\"config.tplPath + \'/current-folder-breadcrumb.html\'\"></div>\n            <div ng-include=\"config.tplPath + \'/main-table-modal.html\'\"></div>\n        </div>\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-sm btn-default\" data-dismiss=\"modal\" data-ng-disabled=\"temp.inprocess\">{{\"close\" | translate}}</button>\n      </div>\n    </div>\n  </div>\n</div>\n\n<script type=\"text/ng-template\" id=\"path-selector\">\n    <div class=\"panel panel-primary mt10 mb0\">\n      <div class=\"panel-heading\">\n        <h3 class=\"panel-title\">{{\'details\' | translate}}</h3>\n      </div>\n      <div class=\"panel-body\">\n          <div class=\"detail-sources\">\n            <code class=\"mr5\"><b>{{\"source\" | translate}}:</b> {{temp.model.fullPath()}}</code>\n          </div>\n          <div class=\"detail-sources\">\n            <code class=\"mr5\"><b>{{\"destination\" | translate}}:</b>{{temp.tempModel.fullPath()}}</code>\n            <span class=\"badge badge-warning pointer\" data-ng-click=\"openNavigator(temp)\">{{\'change\' | translate}}</span>\n          </div>\n      </div>\n    </div>\n</script>\n<script type=\"text/ng-template\" id=\"error-bar\">\n    <div class=\"label label-danger error-msg pull-left animated fadeIn\" data-ng-show=\"temp.error\">\n      <i class=\"glyphicon glyphicon-remove-circle\"></i> {{temp.error}}\n    </div>\n</script>\n");
$templateCache.put("assets/templates/navbar.html","<nav class=\"navbar navbar-inverse navbar-fixed-top\">\n  <div class=\"container-fluid\">\n    <div class=\"navbar-header\">\n      <button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">\n        <span class=\"sr-only\">Toggle</span>\n        <span class=\"icon-bar\"></span>\n        <span class=\"icon-bar\"></span>\n        <span class=\"icon-bar\"></span>\n      </button>\n      <a class=\"navbar-brand hidden-xs\" href=\"\" data-ng-click=\"fileNavigator.goTo(-1)\">{{appName}}</a>\n    </div>\n    <div id=\"navbar\" class=\"navbar-collapse collapse\">\n      <div class=\"navbar-form navbar-right\">\n        <!--<input type=\"text\" class=\"form-control input-sm\" placeholder=\"{{\'search\' | translate}}...\" ng-model=\"$parent.query\">-->\n        <button class=\"btn btn-success btn-sm\" data-toggle=\"modal\" data-target=\"#newfolder\" data-ng-click=\"touch()\">\n            <i class=\"glyphicon glyphicon-plus\"></i> {{\"create_folder\" | translate}}\n        </button>\n        <button class=\"btn btn-success btn-sm\" data-toggle=\"modal\" data-target=\"#uploadfile\" data-ng-click=\"touch()\">\n            <i class=\"glyphicon glyphicon-upload\"></i> {{\"upload_file\" | translate}}\n        </button>\n\n        <button class=\"btn btn-danger btn-sm dropdown-toggle\" type=\"button\" id=\"dropDownMenuCompany\" data-toggle=\"dropdown\" aria-expanded=\"true\">\n            <i class=\"glyphicon glyphicon-globe\"></i> {{\"company\" | translate}} <span class=\"caret\"></span>\n        </button>\n        <ul class=\"dropdown-menu\" role=\"menu\" aria-labelledby=\"dropDownMenuCompany\">\n            <li  data-ng-repeat=\"(rootfolderid, rootfolder) in library\"><a style=\"background-image: url({{rootfolder.icon}});\n             background-size: contain;\n            background-position: left; background-repeat: no-repeat;\" href=\"#\" data-ng-click=\"fileNavigator.chroot(rootfolderid)\">{{rootfolder.name}}</a></li>\n        </ul>\n\n        <button class=\"btn btn-danger btn-sm\" data-ng-click=\"$parent.setTemplate(\'main-icons.html\')\" data-ng-show=\"$parent.viewTemplate !== \'main-icons.html\'\" title=\"{{\'icons\' | translate}}\">\n            <i class=\"glyphicon glyphicon-th-large\"></i>\n        </button>\n        <button class=\"btn btn-danger btn-sm\" data-ng-click=\"$parent.setTemplate(\'main-table.html\')\" data-ng-show=\"$parent.viewTemplate !== \'main-table.html\'\" title=\"{{\'list\' | translate}}\">\n            <i class=\"glyphicon glyphicon-th-list\"></i>\n        </button>\n\n      </div>\n    </div>\n  </div>\n</nav>");
$templateCache.put("assets/templates/sidebar.html","<ul class=\"nav nav-sidebar file-tree-root\">\n    <li ng-repeat=\"item in fileNavigator.history\" ng-include=\"\'folder-branch-item\'\" ng-class=\"{\'active\': item.id == fileNavigator.activeId}\"></li>\n</ul>\n\n<script type=\"text/ng-template\" id=\"folder-branch-item\">\n    <a href=\"\" ng-click=\"fileNavigator.folderClick(item)\" class=\"animated fast fadeInDown\">\n        <i class=\"glyphicon glyphicon-folder-close mr2\" ng-show=\"!fileNavigator.itemsById[item.id].opened\"></i>\n        <i class=\"glyphicon glyphicon-folder-open mr2\" ng-show=\"fileNavigator.itemsById[item.id].opened\"></i>\n        {{ (item.model.name.split(\'/\').pop() || \'/\') | strLimit : 24 }}<!--item.model.id=={{item.model.id}}-->\n    </a>\n    <ul class=\"nav nav-sidebar\">\n        <li ng-repeat=\"item in item.nodes_a | orderBy: orderProp \" ng-include=\"\'folder-branch-item\'\" ng-class=\"{\'active\': item.id == fileNavigator.activeId}\"></li>\n    </ul>\n</script><!--<br/><br/><br/>root={{fileNavigator.root}}<br/>\nfileNavigator.activeId=<br/>{{fileNavigator.activeId}}<br/>-->\n");}]);