(function (angular) {
    'use strict';
    if (!angular) {
        throw 'No angular found';
    }
    var directiveId = 'ngAjaxValidator',

        AppendParameter = function (url, var_val) {
            return url + (url.match(/\?/) ? '&' : '?') + var_val;
        },

        cloneIfExists = function (cloneto, defaultparams, params) {
            $.each(defaultparams, function (ind, val) {
                cloneto[ind] = ((typeof params['ind'] === 'undefined') ? val : params['ind']);
            });
            return cloneto;
        },

        SetIfEmpty = function (params, name, def, get_from_parent_scope) {
            if (params[name] !== '' && get_from_parent_scope) {
                params[name] = scope.$parent.$parent[name]
                return;
            }
            if (params[name] === '')
                params[name] = def;
        },

        setVariable = function (name, data) {
            if (params[name]) {
                $scope[params[name]] = data;
            }
        },
        getVariable = function (name) {
            return params[name] ? $scope[params[name]] : null;
        },

        ajaxValidator = function ($ok, $compile) {

            return {
                restrict: 'A',
                //require: ['ngModel'],
                //scope: {
                //    //ngAjaxForm: '&',
                //    //
                //    //ngModel: '&',
                //    //
                //    //ngValidateUrl: "&",
                //    //ngValidateRequesting: '&',
                //    //ngValidateResponsed: '&',
                //    //ngValidateResponse: 'validation',
                //    //ngValidateBefore: '',
                //    //ngValidateAfter: '',
                //    //ngValidateWatch: ""
                //    //ngValidate-debounce: "500"
                //    //
                //    //ngLoad-url: ""
                //    //ngLoad-variable-requesting: 'loading'
                //    //ngLoad-variable-responded: ''
                //    //ngLoad-variable-response: 'original_data'
                //    //ngLoad-before: ""
                //    //ngLoad-after: ""
                //    //
                //    //ngLoad-url: ""
                //    //ngSave-variable-requesting: 'saving'
                //    //ngSave-variable-responded: 'saved'
                //    //ngSave-variable-response: ''
                //    //ngSave-before: ""
                //    //ngSave-after: ""
                //    //
                //    //
                //    //
                //    //
                //    //ngAfter: '&',
                //    //ngBefore: '&',
                //    //ngData: '@',
                //    //ngState: '@'
                //},
                scope: true,
                link: function (scope, el, attrs, ctrls) {


                    var $scope = scope.$parent;
                    var $data_var = 'data';

                    var params = {};

                    // variables! remove this!!! hardcode in default callbacks and pass default callbacks to REAL callbacks
                    cloneIfExists(params, {
                        //ngData: 'data',
                        //ngLoadedData: 'loaded_data',
                        //ngValidatedData: 'validated_data',
                        //ngValidatedAnswer: 'validation',
                        //ngSavedData: 'saved_data',
                        //ngValidatedAnswer: 'validation',


                        //ngLoadRequesting: 'loading',
                        //ngLoadResponded: false,
                        //ngLoadResponse: 'original_data',
                        //
                        //ngValidateRequesting: 'validating',
                        //ngValidateResponsed: 'validated',
                        //ngValidateResponse: 'validation',
                        //
                        //ngSaveRequesting: 'saving',
                        //ngSaveResponded: 'saved',
                        //ngSaveResponse: false
                    }, attrs);

                    // validation watch params
                    cloneIfExists(params, {
                        ngValidateWatch: '',
                        ngValidateDebounce: '500'
                    }, attrs);

                    SetIfEmpty(params, 'ngValidateWatch', params['ngData']);
                    params['ngValidateDebounce'] = parseInt(params['ngValidateDebounce']);


                    // url builders
                    var defaultCallbacks = {
                        ngUrl: function (default_function) {
                            return window.location.href;
                        },
                        ngLoadUrl: function (default_function) {
                            return AppendParameter(params['ngUrl'](), 'action=load');
                        },
                        ngValidateUrl: function (default_function) {
                            return AppendParameter(params['ngUrl'](), 'action=validate');
                        },
                        ngSaveUrl: function (default_function) {
                            return AppendParameter(params['ngUrl'](), 'action=save');
                        },
                        ngLoadBefore: function (default_function) {
                            // return true if you need load model
                            return $scope.hasOwnProperty('data') ? false : {};
                        },
                        ngLoadAfter: function (resp, default_function) {
                            // save loaded model
                            $scope['data'] = cloneObject(resp);
                            $scope['original_data'] = cloneObject(resp);
                            console.log($scope);
                            return true;
                        },

                        ngValidateBefore: function (default_function) {
                            // return something != undefined if you need load model
                            return $scope['data'];
                        },


                        ngValidateAfter: function (resp, default_function) {
                            $scope['validation'] = cloneObject(resp);
                            return resp;
                        },

                        ngSaveBefore: function (default_function) {
                            return $scope['data'];
                        },


                        ngSaveAfter: function (resp, default_function) {
                            return resp;
                        }

                        //ngBefore: function (data, validation, httpconfig, defaultfunc) {
                        //    //httpconfig['url'] = http://someurl
                        //    if (data) {
                        //        if (typeof parentscope[params['ngState']] === 'string') {
                        //            return false;
                        //        }
                        //        parentscope[params['ngState']] = validation ? 'validating' : 'sending';
                        //    }
                        //    else {
                        //        return false;
                        //    }
                        //},
                        //
                        //ngAfter: function (response, validation, httpresp, defaultfunc) {
                        //    if (!response) {
                        //        return false;
                        //    }
                        //    if (!validation && response && httpresp && httpresp['headers']('Location')) {
                        //        window.location.href = httpresp['headers']('Location');
                        //    }
                        //    return response;
                        //},

                    };
                    cloneIfExists(params, defaultCallbacks, attrs);

                    function callCallback() {
                        var args = Array.prototype.slice.call(arguments);
                        var callbackkey = args.shift();
                        args.push(defaultCallbacks[callbackkey])
                        return params[callbackkey].apply($scope, args);
                        }

                    var loadurl = callCallback('ngLoadUrl');
                    var loaddata = callCallback('ngLoadBefore');
                    if (loadurl, loaddata) {
                        $scope['state'] = 'loading';
                        $ok(loadurl, loaddata, function (resp) {
                            $scope['state'] = 'clean';
                            callCallback('ngLoadAfter', resp);
                        });
                    }


                    //SetIfEmpty('ngUrl', window.location.href);
                    //SetIfEmpty('ngLoadUrl', AppendParameter(params['ngUrl'], 'action=load'));
                    //SetIfEmpty('ngValidateUrl', AppendParameter(params['ngUrl'], 'action=validate'));
                    //SetIfEmpty('ngSaveUrl', AppendParameter(params['ngUrl'], 'action=save'));

                    //SetIfEmpty('ngLoadBefore', function () {
                    //    return {}
                    //}, true);
                    //SetIfEmpty('ngLoadResponded', null);

                    //if (params['ngUrl'] === '') params['ngUrl']


                    //var enableSubmit = function (enablesubmit, enableinput) {
                    //    if (enablesubmit) {
                    //        $('*[ng-model]', $(iElement)).prop('disabled', false);
                    //    }
                    //    else {
                    //        $('*[ng-model]', $(iElement)).prop('disabled', true);
                    //    }
                    //}

                    //$scope['state'] = false;
                    //scope.$parent.$parent.__validated = false;

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
                    }                    ;


                    //var params = $.extend(defaultparams, {
                    //    ngData: scope['ngData'],
                    //    ngBefore: scope['ngBefore'],
                    //    ngAfter: scope['ngAfter'],
                    //    ngState: scope['ngState']
                    //});

                    var sendfunction = function () {
                        var old_state = $scope['state'];

                        var dataToSend = callCallback('ngSaveBefore');
                        var url = callCallback('ngSaveUrl');
                        if (!dataToSend || !url) {
                            return false;
                        }

                        $scope['state'] = 'saving';
                        $ok(url, dataToSend,
                            function (resp, errorcode, httpresp) {
                                callCallback('ngSaveAfter', resp);
                                $scope['state'] = 'clean';
                            },
                            function (resp, errorcode, httpresp) {
                                $scope['state'] = old_state;
                            });
                    }

                    $scope.save = sendfunction;


                    //if (params['ngData']) {
                    //    parentscope.$watch(params['ngData'], _.debounce(function () {
                    //        sendfunction(true);
                    //    }, 500), true);
                    //}

                    //if (scope['ngOnsubmit']) {
                    //    $(iElement).on('submit',
                    //        function () {
                    //            if (scope.$parent.$parent.__validation) {
                    //                return false;
                    //            }
                    //            enableSubmit(false);
                    //            scope.$apply(function () {
                    //                var dataToSend = scope['ngOnsubmit']()();
                    //                console.log(dataToSend);
                    //                if (dataToSend) {
                    //                    $ok(scope['ngAction'], dataToSend, function (resp) {
                    //                        if (scope.ngOnsuccess) {
                    //                            scope.ngOnsuccess()(resp)
                    //                        }
                    //                    }).finally(function () {
                    //                        enableSubmit(true);
                    //                    });
                    //                }
                    //            });
                    //            return false;
                    //        });
                    //}
                    //
                    //$(iElement).on('submit',
                    //    function () {
                    //        sendfunction();
                    //        return false;
                    //    });
                }
            };

        }

    angular.module('ajaxValidator', [])
        //.constant('MODULE_VERSION', '##_version_##')
        .directive(directiveId, ['$ok', '$compile', ajaxValidator]);

})(this.angular);
