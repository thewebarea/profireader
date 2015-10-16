/**
 * Function calculates difference between two objects/arrays
 * return array or object depending on type of second argument
 * @param {type} a
 * @param {type} b
 * @param {type} notstrict - compare by == if true (if false/ommted by ===)
 * @returns {Array/Object} with elements different in a and b. also if index is present only in one object (a or b)
 * if returened element is array same object are reffered by 'undefined'
 */
function getObjectsDifference(a, b, setval, notstrict) {

    'use strict';

    if ((typeof a !== 'object') || (typeof b !== 'object')) {
        console.log('getObjectsDifference expects both arguments to be array or object');
        return null;
    }

    var ret = $.isArray(b) ? [] : {};

    $.each(a, function (ind, aobj) {
        if ((typeof aobj === 'object') && (typeof b[ind] === 'object')) {
            if ((aobj === null) && (b[ind] === null)) {
                return;
            }
            var nl = getObjectsDifference(aobj, b[ind], setval, notstrict);
            if (!$.isEmptyObject(nl)) {
                ret[ind] = nl;
            }
        }
        else {
            if ((notstrict && (a[ind] == b[ind])) || (!notstrict && (a[ind] === b[ind]))) {
                return;
            }
            ret[ind] = (setval === undefined) ? aobj : setval;
        }
    });
    $.each(b, function (ind, bobj) {
        if ((typeof bobj === 'object') && (typeof a[ind] === 'object')) {

        }
        else {
            if ((notstrict && (a[ind] == b[ind])) || (!notstrict && (a[ind] === b[ind]))) {
                return;
            }
            ret[ind] = (setval === undefined) ? bobj : setval;
        }
    });
    return ret;
}


angular.module('profireaderdirectives', ['ui.bootstrap', 'ui.bootstrap.tooltip'])
    .factory('$ok', ['$http', function ($http) {
        return function (url, data, ifok, iferror, config) {
            function error(result, error_code) {
                if (iferror) {
                    iferror(result, error_code)
                }
                else {
                    alert(result);
                }
            };


            return $http.post(url, data, config ? config : {}).then(
                function (response) {
                    if (!response || !response['data'] || typeof response['data'] !== 'object' || response === null) {
                        return error('wrong response', -1, response);
                    }

                    var resp = response['data'];

                    if (!resp['ok']) {
                        return error(resp['data'], resp['error_code'], response);
                    }

                    if (ifok) {
                        return ifok(resp['data'], 0, response);
                    }

                },
                function (response) {
                    return error('wrong response', -1, response);
                }
            );
        }
    }])
    .directive('dateTimestampFormat', function () {
        return {
            require: 'ngModel',
            link: function (scope, element, attr, ngModelCtrl) {
                ngModelCtrl.$formatters.unshift(function (timestamp) {
                    if (timestamp) {
                        var date = new Date(timestamp * 1000);
                        return date;
                    } else
                        return "";
                });
                ngModelCtrl.$parsers.push(function (date) {
                    if (date instanceof Date) {
                        var timestamp = Math.floor(date.getTime() / 1000)
                        return timestamp;
                    } else
                        return "";
                });
            }
        };
    })
    .directive('highlighter', ['$timeout', function ($timeout) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                scope.$watch(attrs.highlighter, function (nv, ov) {
                    if (nv !== ov) {
                        highlight($(element));
                    }
                });
            }
        };
    }])
    .directive('ngOk', ['$http', '$compile', '$ok', function ($http, $compile, $ok) {
        return {
            restrict: 'A',
            scope: {
                ngAfter: '&',
                ngBefore: '&',
                ngData: '@',
                ngState: '@'
            },
            link: function (scope, iElement, iAttrs, ngModelCtrl) {

                var parentscope = scope.$parent.$parent;

                var defaultparameters = {

                    ngData: 'data',

                    ngState: 'state',


                    ngBefore: function (data, validation, httpconfig, defaultfunc) {
                        //httpconfig['url'] = http://someurl
                        if (data) {
                            if (typeof parentscope[parameters['ngState']] === 'string') {
                                return false;
                            }
                            parentscope[parameters['ngState']] = validation ? 'validating' : 'sending';
                        }
                        else {
                            return false;
                        }
                    },

                    ngAfter: function (response, validation, httpresp, defaultfunc) {
                        if (!response) {
                            return false;
                        }
                        if (!validation && response && httpresp && httpresp['headers']('Location')) {
                            window.location.href = httpresp['headers']('Location');
                        }
                        return response;
                    },

                };

                var parameters = $.extend(defaultparameters, {
                    ngData: scope['ngData'],
                    ngBefore: scope['ngBefore'],
                    ngAfter: scope['ngAfter'],
                    ngState: scope['ngState']
                });

                var sendfunction = function (validate) {
                    var old_state = parentscope[parameters['ngState']];
                    var default_data = parentscope[parameters['ngData']];
                    var default_config = {url: iAttrs['action'] ? iAttrs['action'] : window.location.href};
                    if (validate) {
                        default_config['headers'] = {validation: 'true'};
                    }
                    var dataToSend = parameters['ngBefore']()(default_data, validate, default_config, defaultparameters['ngBefore']);

                    if (!dataToSend) {
                        return false;
                    }
                    var url = default_config['url'](dataToSend, true, defaultparameters['ngUrl']);
                    $ok(url, dataToSend,
                        function (resp, errorcode, httpresp) {
                            var ret = parameters['ngAfter']()(resp, true, defaultparameters['ngAfter'], errorcode, httpresp);
                            parentscope[parameters['ngState']] = ret ? ret : old_state;
                        },
                        function (resp, errorcode, httpresp) {
                            var ret = parameters['ngAfter']()(null, true, defaultparameters['ngAfter'], errorcode, httpresp);
                            parentscope[parameters['ngState']] = ret ? ret : old_state;
                        });
                }


                if (parameters['ngData']) {
                    parentscope.$watch(parameters['ngData'], _.debounce(function () {
                        sendfunction(true);
                    }, 500), true);
                }

                $(iElement).on('submit',
                    function () {
                        sendfunction(false);
                        return false;
                    });
            }
        }

    }]);


areAllEmpty = function () {
    var are = true;
    $.each(arguments, function (ind, object) {
        if (are) {
            var ret = true;
            if ($.isArray(object)) {
                ret = object.length ? false : true;
            }
            else if ($.isPlainObject(object) && $.isEmptyObject(object)) {
                ret = true;
            }
            else {
                ret = ((object === undefined || object === false || object === null || object === 0) ? true : false);
            }
            are = ret;
        }
    });
    return are;
}

function file_choose(selectedfile) {
    var args = top.tinymce.activeEditor.windowManager.getParams();
    var win = (args.window);
    var input = (args.input);
    win.document.getElementById(input).value = selectedfile['url'];
    top.tinymce.activeEditor.windowManager.close();
}

module = angular.module('Profireader', ['ui.bootstrap', 'profireaderdirectives', 'ui.tinymce']);

module.config(function ($provide) {
    $provide.decorator('$controller', function ($delegate) {
        return function (constructor, locals, later, indent) {
            if (typeof constructor === 'string' && !locals.$scope.controllerName) {
                locals.$scope.controllerName = constructor;
            }
            return $delegate(constructor, locals, later, indent);
        };
    });
});

module.controller('filemanagerCtrl', ['$scope', '$modalInstance', 'file_manager_called_for', 'file_manager_on_action',
    function ($scope, $modalInstance, file_manager_called_for, file_manager_on_action) {

//TODO: SW fix this pls

        closeFileManager = function () {
            $scope.$apply(function () {
                $modalInstance.dismiss('cancel')
            });
        }

        $scope.close = function () {
            $modalInstance.dismiss('cancel');
        }

        $scope.src = '/filemanager/';
        var params = {};
        if (file_manager_called_for) {
            params['file_manager_called_for'] = file_manager_called_for;
        }
        if (file_manager_on_action) {
            params['file_manager_on_action'] = angular.toJson(file_manager_on_action);
        }
        $scope.src = $scope.src + '?' + $.param(params);
    }]);

module.run(function ($rootScope, $ok) {
    angular.extend($rootScope, {
        _: function (phrase, dict) {
            var scope = this;
            try {
                return phrase.replace(/%\(([^)]*)\)s/g, function (g0, g1) {
                    var indexes = g1.split('.')
                    var d = dict ? dict : scope;
                    for (var i in indexes) {
                        if (typeof d[indexes[i]] !== undefined) {
                            d = d[indexes[i]];
                        }
                        else {
                            return g1;
                        }
                    }
                    return d;
                });
            } catch (a) {
                return phrase
            }
        },
        loadData: function (url, senddata, onok) {
            var scope = this;
            scope.loading = true;
            $ok(url ? url : '', senddata ? senddata : {}, function (data) {
                scope.data = data;
                scope.original_data = $.extend(true, {}, data);
                if (onok) onok();
            }).finally(function () {
                scope.loading = false;
            });
        },
        areAllEmpty: areAllEmpty,
        tinymceImageOptions: {
            inline: false,
            plugins: 'advlist autolink link image lists charmap print preview',
            skin: 'lightgray',
            theme: 'modern',
            file_browser_callback: function (field_name, url, type, win) {
                var cmsURL = '/filemanager/?file_manager_called_for=file_browse_' + type +
                    '&file_manager_on_action=' + encodeURIComponent(angular.toJson({choose: 'parent.file_choose'}));
                tinymce.activeEditor.windowManager.open({
                        file: cmsURL,
                        title: 'Select an Image',
                        width: 950,  // Your dimensions may differ - toy around with them!
                        height: 700,
                        resizable: "yes",
                        //inline: "yes",  // This parameter only has an effect if you use the inlinepopups plugin!
                        close_previous: "yes"
                    }
                    ,
                    {
                        window: win,
                        input: field_name
                    }
                )
                ;
            }
        }
    })
});


None = null;
False = false;
True = true;


//TODO: RP by OZ:   pls rewrite this two functions as jquery plugin

function scrool($el, options) {
    $.smoothScroll($.extend({
        scrollElement: $el.parent(),
        scrollTarget: $el
    }, options ? options : {}));
}

function highlight($el) {
    $el.addClass('highlight');
    setTimeout(function () {
        $el.removeClass('highlight');
    }, 500);
}

function angularControllerFunction(controller_attr, function_name) {
    var el = $('[ng-controller=' + controller_attr + ']');
    if (!el && !el.length) return function () {
    };
    var func = angular.element(el[0]).scope()[function_name];
    var controller = angular.element(el[0]).controller();
    if (func && controller) {
        return func
    }
    else return function () {
    };

}

function fileUrl(id) {
    if (!id) return '';
    var server = id.replace(/^[^-]*-[^-]*-4([^-]*)-.*$/, "$1");
    return 'http://file' + server + '.profi.ntaxa.com/' + id + '/'
}