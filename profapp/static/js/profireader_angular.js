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
    .factory('$translate', ['$http', function ($http) {

        return function (text, dict) {
            return text.replace(/%\(([^)]*)\)s/g, function (g0, g1) {
                var indexes = g1.split('.')
                var d = dict;
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

        }
    }])


    .factory('$ok', ['$http', function ($http) {
        return function (url, data, ifok, iferror) {
            function error(result, error_code) {
                if (iferror) {
                    iferror(result, error_code)
                }
                else {
                    alert(result);
                }
            };

            return $http.post(url, data).then(
                function (resp) {
                    if (!resp || !resp['data'] || typeof resp['data'] !== 'object' || resp === null) {
                        return error('wrong response', -1);
                    }

                    resp = resp ['data'];

                    if (!resp['ok']) {
                        return error(resp['data'], resp['error_code']);
                    }

                    if (ifok) {
                        return ifok(resp['data']);
                    }

                },
                function () {
                    return error('wrong response', -1);
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
    .directive('ngAjaxAction', ['$http', '$compile', '$ok', '$timeout', function ($http, $compile, $ok, $timeout) {
//TODO: RP by OZ can you bind model to tag with this directivre? I want move ajax_action from code below to model binded by ng-bind
//<form ng-model="ajax_action" ng-ajax-action="url">
        return {
            restrict: 'A',
            scope: false,
            link: function (scope, iElement, iAttrs, ctrl) {

                scope.ajax_action = {};
                var s = scope.ajax_action;

                s.checking = {};
                s.checked = {};

                s.errors = {};
                s.warnings = {};
                s.dirty = true;

                s.submitting = false;
                s.url = null;
                s.on_success_url = null;

                iAttrs.$observe('ngAjaxAction', function(value) {
                    s.url = value;
                    });

                iAttrs.$observe('ngOnSuccess', function(value) {
                    s.on_success_url = value;
                    });


                $(iElement).on('submit',
                    function () {
                        scope.$apply(function () {
                            s.submitting = true;
                            $('input[type=submit]', $(iElement)).prop('disabled', true);
                            $('button[type=submit]', $(iElement)).prop('disabled', true);
                            $ok(s.url, scope['data'], function (resp) {
                                scope.data = resp;
                                if (s.on_success_url) {
                                    $timeout(function () {
                                        document.location.href = s.on_success_url;
                                    }, 1);
                                }
                            }).finally(function () {
                                $('input[type=submit]', $(iElement)).prop('disabled', false);
                                $('button[type=submit]', $(iElement)).prop('disabled', false);
                            });
                        });
                        return false;
                    });


                //$.each($('[name]', $(iElement)), function (ind, el) {
                //$newel = $(el).clone();
                //scope.data[$(el).attr('name')] = $(el).val();
                //$newel.attr('ng-model', 'data.' + $newel.attr('name'));
                //$(el).replaceWith($compile($newel)(scope))
                //});


                s.getSignificantClass = function (index, one, onw, onn) {

                    if (s.errors && !areAllEmpty(s.errors[index])) {
                        return one;
                    }
                    if (s.warnings && !areAllEmpty(s.warnings[index])) {
                        return onw;
                    }
                    if (s.notices && !areAllEmpty(s.notices[index])) {
                        return onn;
                    }
                    return '';
                };

                s.getSignificantMessage = function (index) {

                    if (s.errors && !areAllEmpty(s.errors[index])) {
                        return s.errors[index][0];
                    }
                    if (s.warnings && !areAllEmpty(s.warnings[index])) {
                        return s.warnings[index][0];
                    }
                    if (s.notices && !areAllEmpty(s.notices[index])) {
                        return s.notices[index][0]
                    }
                    return '';
                };


                s.refresh = function () {
                    s.changed = getObjectsDifference(s.checked, s['data']);
                    s.check();
                };

                s.check = _.debounce(function (d) {
                    if (areAllEmpty(s.checking)) {
                        console.log('s.changed', s.changed);
                        s.changed = getObjectsDifference(s.checked, scope['data']);
                        if (!areAllEmpty(s.changed)) {
                            s.checking = scope['data'];

                            $http.post($(iElement).attr('njAjaxAction'), s.checking)
                                .then(function (fromserver) {
                                    var resp = fromserver['data'];
                                    if (areAllEmpty(getObjectsDifference(s.checking, scope['data']))) {
                                        s.errors = $.extend(true, {}, resp['errors']);
                                        s.warnings = $.extend(true, {}, resp['warnings']);
                                        s.checked = $.extend(true, {}, s.checking);
                                        s.changed = {};
                                        s.checking = {};
                                    }
                                    else {
                                        s.checking = {};
                                        s.refresh();
                                    }
                                }, function () {
                                    s.checking = {};
                                    s.refresh();
                                });
                        }
                    }
                    else {
                        s.refresh();
                    }
                }, 500);
                console.log(iAttrs);
                if (iAttrs['ngAjaxFormValidate'] !== undefined) {
                    s.$watch('data', s.refresh, true);
                    s.refresh();
                }
                //            s.getTemp(iAttrs.ngCity);
            }
        };
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

