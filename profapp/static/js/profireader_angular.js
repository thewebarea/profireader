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


angular.module('profireaderdirectives', ['ui.bootstrap', 'ui.bootstrap.tooltip', 'ajaxFormModule'])
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
    .service('objectTransformation', function () {
        var objectTransformation = {};

        objectTransformation.reverseKeyValue = function (objIn) {
            var objOut = {}, keys, i;
            keys = Object.keys($scope.data.PortalDivisionTags3);
            for (i = 0; i < objIn.length; i++) {
                objOut[objIn[keys[i]]] = keys[i];
            }
            return objOut;
        };

        objectTransformation.getValues1 = function (objList, key, unique) {
            var values = [], value;
            for (var i = 0; i < objList.length; i++) {
                value = objList[i][key];
                if (!unique || (values.indexOf(value) === -1)) {
                    values.push(value);
                }
            }
            return values;
        };

        objectTransformation.getValues2 = function (objList, key1, key2) {
            var resultObject = {}, key, value;
            for (var i = 0; i < objList.length; i++) {
                key = objList[i][key1];
                value = objList[i][key2];

                if (typeof resultObject[key] === 'undefined') {
                    resultObject[key] = [value]
                } else {
                    if (resultObject[key].indexOf(value) === -1) {
                        resultObject[key].push(value)
                    }
                }
            }
            return resultObject;
        };

        objectTransformation.getValues3 = function (objList, key1, key2, key2List) {
            var resultObject = {}, key, i, objFilledWithFalse = {};

            for (i = 0; i < key2List.length; i++) {
                objFilledWithFalse[key2List[i]] = false
            }

            for (i = 0; i < objList.length; i++) {
                key = objList[i][key1];
                if (typeof resultObject[key] === 'undefined') {
                    resultObject[key] = $.extend(true, {}, objFilledWithFalse);
                }
                resultObject[key][objList[i][key2]] = true;
            }

            return resultObject;
        };

        objectTransformation.getValues4 = function (objList, key1, key2, key2List) {
            var resultObject = {}, key, i, objFilledWithFalse = {}, lList, elem;

            lList = [];
            for (i = 0; i < objList.length; i++) {
                elem = objList[i][key1];
                if (lList.indexOf(elem) === -1) {
                    lList.push(elem);
                }
            }

            for (i = 0; i < lList.length; i++) {
                objFilledWithFalse[lList[i]] = false;
            }

            for (i = 0; i < key2List.length; i++) {
                resultObject[key2List[i]] = $.extend(true, {}, objFilledWithFalse);
            }

            for (i = 0; i < objList.length; i++) {
                key = objList[i];
                resultObject[key[key2]][key[key1]] = true;
            }

            return resultObject;
        };

        // substitution in keys is performed
        objectTransformation.subsInKey = function (objIn, objForSubstitution) {
            var keys, i, objOut;

            keys = Object.keys(objIn);
            objOut = {};

            for (i = 0; i < keys.length; i++) {
                objOut[objForSubstitution[keys[i]]] = objIn[keys[i]];
            }

            return objOut;
        };

        // substitution of list elements is performed
        objectTransformation.subsElemOfList = function (listIn, objForSubstitution) {
            var i, listOut;
            listOut = [];
            for (i = 0; i < listIn.length; i++) {
                listOut.push(objForSubstitution[listIn[i]])
            }
            return listOut;
        };

        return objectTransformation;
    })
    .directive('ngOk', ['$http', '$compile', '$ok', function ($http, $compile, $ok) {
        return {
            restrict: 'A',
            scope: {
                ngOnsubmit: '&',
                ngOnsuccess: '&',
                ngOnfail: '&',
                ngAction: '=',
                ngWatch: '@'
            },
            link: function (scope, iElement, iAttrs, ngModelCtrl) {





                //if (iAttrs['ngValidationResult']) {
                //    scope[iAttrs['ngValidationResult']] = {};
                //    var s = scope[iAttrs['ngValidationResult']];
                //
                //    s.checking = {};
                //    s.checked = {};
                //
                //    s.errors = {};
                //    s.warnings = {};
                //    s.dirty = true;
                //
                //    s.submitting = false;
                //    s.url = null;
                //    s.on_success_url = null;
                //}

                //iAttrs.$observe('ngAjaxAction', function(value) {
                //    s.url = value;
                //    });

                //iAttrs.$observe('ngOnSuccess', function(value) {
                //    s.on_success_url = value;
                //    });


                //$.each($('[name]', $(iElement)), function (ind, el) {
                //$newel = $(el).clone();
                //scope.data[$(el).attr('name')] = $(el).val();
                //$newel.attr('ng-model', 'data.' + $newel.attr('name'));
                //$(el).replaceWith($compile($newel)(scope))
                //});


                //s.getSignificantClass = function (index, one, onw, onn) {
                //
                //    if (s.errors && !areAllEmpty(s.errors[index])) {
                //        return one;
                //    }
                //    if (s.warnings && !areAllEmpty(s.warnings[index])) {
                //        return onw;
                //    }
                //    if (s.notices && !areAllEmpty(s.notices[index])) {
                //        return onn;
                //    }
                //    return '';
                //};
                //
                //s.getSignificantMessage = function (index) {
                //
                //    if (s.errors && !areAllEmpty(s.errors[index])) {
                //        return s.errors[index][0];
                //    }
                //    if (s.warnings && !areAllEmpty(s.warnings[index])) {
                //        return s.warnings[index][0];
                //    }
                //    if (s.notices && !areAllEmpty(s.notices[index])) {
                //        return s.notices[index][0]
                //    }
                //    return '';
                //};
                //
                //
                //s.refresh = function () {
                //    s.changed = getObjectsDifference(s.checked, s['data']);
                //    s.check();
                //};
                //
                //s.check = _.debounce(function (d) {
                //    if (areAllEmpty(s.checking)) {
                //        console.log('s.changed', s.changed);
                //        s.changed = getObjectsDifference(s.checked, scope['data']);
                //        if (!areAllEmpty(s.changed)) {
                //            s.checking = scope['data'];
                //
                //            $http.post($(iElement).attr('njAjaxAction'), s.checking)
                //                .then(function (fromserver) {
                //                    var resp = fromserver['data'];
                //                    if (areAllEmpty(getObjectsDifference(s.checking, scope['data']))) {
                //                        s.errors = $.extend(true, {}, resp['errors']);
                //                        s.warnings = $.extend(true, {}, resp['warnings']);
                //                        s.checked = $.extend(true, {}, s.checking);
                //                        s.changed = {};
                //                        s.checking = {};
                //                    }
                //                    else {
                //                        s.checking = {};
                //                        s.refresh();
                //                    }
                //                }, function () {
                //                    s.checking = {};
                //                    s.refresh();
                //                });
                //        }
                //    }
                //    else {
                //        s.refresh();
                //    }
                //}, 500);
                //console.log(iAttrs);
                //if (iAttrs['ngAjaxFormValidate'] !== undefined) {
                //    s.$watch('data', s.refresh, true);
                //    s.refresh();
                //}
                //            s.getTemp(iAttrs.ngCity);
            }
        }

    }])
    .directive('ngAjaxFormOld', ['$http', '$compile', '$ok', function ($http, $compile, $ok) {
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


                var enableSubmit = function (enablesubmit, enableinput) {
                    if (enablesubmit) {
                        $('*[ng-model]', $(iElement)).prop('disabled', false);
                    }
                    else {
                        $('*[ng-model]', $(iElement)).prop('disabled', true);
                    }
                }

                scope.$parent.$parent.__validation = false;
                scope.$parent.$parent.__validated = false;

                var sendValidation = _.debounce(function () {
                    if (scope.$parent.$parent.__validation) {
                        return false;
                    }
                    var dataToSend = scope['ngOnsubmit']()();
                    if (dataToSend) {
                        scope.$parent.$parent.__validation = dataToSend;
                        $ok(scope['ngAction'], $.extend({__validation: true}, dataToSend), function (resp) {
                            scope.$parent.$parent.__validated = resp;
                        }, function (resp) {
                            scope.$parent.$parent.__validated = false;
                        }).finally(function () {
                            scope.$parent.$parent.__validation = false;
                        });
                    }
                }, 500);

                if (scope['ngWatch']) {
                    scope, scope.$parent.$parent.$watch(scope['ngWatch'], sendValidation, true);
                }
                ;


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
                    var dataToSend = parameters['ngBefore'](default_data, validate, default_config, defaultparameters['ngBefore']);
                    console.log(dataToSend);

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

                if (scope['ngOnsubmit']) {
                    $(iElement).on('submit',
                        function () {
                            if (scope.$parent.$parent.__validation) {
                                return false;
                            }
                            enableSubmit(false);
                            scope.$apply(function () {
                                var dataToSend = scope['ngOnsubmit']()();
                                console.log(dataToSend);
                                if (dataToSend) {
                                    $ok(scope['ngAction'], dataToSend, function (resp) {
                                        if (scope.ngOnsuccess) {
                                            scope.ngOnsuccess()(resp)
                                        }
                                    }).finally(function () {
                                        enableSubmit(true);
                                    });
                                }
                            });
                            return false;
                        });
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

module = angular.module('Profireader', ['ui.bootstrap', 'profireaderdirectives', 'ui.tinymce', 'ajaxFormModule']);

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
        loadData: function (url, senddata, beforeload, afterload) {
            var scope = this;
            scope.loading = true;
            $ok(url ? url : '', senddata ? senddata : {}, function (data) {
                if (!beforeload) beforeload = function (d) {
                    return d;
                };
                scope.data = beforeload(data);
                scope.original_data = $.extend(true, {}, scope.data);
                if (afterload) afterload();

            }).finally(function () {
                scope.loading = false;
            });
        },
        areAllEmpty: areAllEmpty,

        tinymceImageOptions: {
            inline: false,
            plugins: 'advlist autolink link image lists charmap print preview paste',
            skin: 'lightgray',
            paste_as_text: false,
            width: '100%',
            height: '100%',
            theme: 'modern',
            //paste_postprocess1: function (plugin, args) {
            //    console.log('paste_postprocess', args);
            //},
            setup: function (editor) {
                console.log('setup', editor);
                editor.on('PreInit', function (event) {
                    editor.parser.addNodeFilter('img,p', function (nodes, name) {
                        console.log('addNodeFilter', nodes, name);
                    });
                    //editor.parser.addAttributeFilter('src,href', function (nodes, name) {
                    //    console.log('addAttributeFilter', nodes, name);
                    //    debugger;
                    //    });
                });
            },
            //init_instance_callback1: function () {
            //    console.log('init_instance_callback', arguments);
            //},
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
            },
            //valid_elements: Config['article_html_valid_elements'],
            //valid_elements: 'a[class],img[class|width|height],p[class],table[class|width|height],th[class|width|height],tr[class],td[class|width|height],span[class],div[class],ul[class],ol[class],li[class]',
            content_css: "/static/front/bird/css/article.css",
            style_formats: [
                {title: 'HEAD1', block: 'div', classes: 'h1'},
                {title: 'HEAD2', block: 'div', classes: 'h2'},
                {title: 'HEAD3', block: 'div', classes: 'h3'},
                {title: 'BIG', inline: 'span', classes: 'big'},
                {title: 'BIGGER', inline: 'span', classes: 'bigger'},
                {title: 'NORMAL', inline: 'span', classes: 'small'},
                {title: 'SMALLER', inline: 'span', classes: 'smaller'},
                {title: 'SMALL', inline: 'span', classes: 'small'}
            ],


            //paste_auto_cleanup_on_paste : true,
            //paste_remove_styles: true,
            //paste_remove_styles_if_webkit: true,
            //paste_strip_class_attributes: "all",

            //style_formats: [
            //    {title: 'Bold text', inline: 'b'},
            //    {title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
            //    {title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
            //
            //    {
            //        title: 'Image Left',
            //        selector: 'img',
            //        styles: {
            //            'float': 'left',
            //            'margin': '0 10px 0 10px'
            //        }
            //    },
            //    {
            //        title: 'Image Right',
            //        selector: 'img',
            //        styles: {
            //            'float': 'right',
            //            'margin': '0 0 10px 10px'
            //        }
            //    }
            //]
        }
    });
});

function cleanup_html(html) {
    normaltags = '^(span|a|br|div|table)$'
    common_attributes = {
        whattr: {'^(width|height)$': '^([\d]+(.[\d]*)?)(em|px|%)$'}
    }

    allowed_tags = {
        '^table$': {allow: '^(tr)$', attributes: {whattr: true}},
        '^tr$': {allow: '^(td|th)$', attributes: {}},
        '^td$': {allow: normaltags, attributes: {whattr: true}},
        '^a$': {allow: '^(span)$', attributes: {'^href$': '.*'}},
        '^img$': {allow: false, attributes: {'^src$': '.*'}},
        '^br$': {allow: false, attributes: {}},
        '^div$': {allow: normaltags, attributes: {}}
    }

    $.each(allowed_tags, function (tag, properties) {
        var attributes = properties.attributes ? properties.attributes : {}
        $.each(attributes, function (attrname, allowedvalus) {
            if (allowedvalus === true) {
                allowed_tags[tag].attributes[attrname] = common_attributes[attrname] ? common_attributes[attrname] : '.*';
            }
        });
    });

    var tags = html.split(/<[^>]*>/)

    $.each(tags, function (tagindex, tag) {
        console.log(tagindex, tag);
    })

    return html;
}


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
    return 'http://file' + server + '.profireader.com/' + id + '/'
}


function cloneObject(o) {
    return (o === null || typeof o !== 'object') ? o : $.extend(true, {}, o);
}

