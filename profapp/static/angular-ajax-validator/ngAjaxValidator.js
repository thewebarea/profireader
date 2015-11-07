(function (angular) {
    'use strict';
    if (!angular) {
        throw 'No angular found';
    }

    var AppendParameter = function (url, var_val) {
        return url + (url.match(/\?/) ? '&' : '?') + var_val;
    };

    var cloneIfExists = function (cloneto, defaultparams, passed) {
        $.each(defaultparams, function (ind, val) {
            if (typeof passed[ind] === 'string') cloneto[ind] = passed[ind];
            if (typeof passed[ind] === 'function') {
                var ret = passed[ind]();
                cloneto[ind] = ((typeof ret === 'undefined') ? val : ret);
                };
        });
        return cloneto;
    };

    var SetIfEmpty = function (params, name, def, get_from_parent_scope) {
        if (params[name] !== '' && get_from_parent_scope) {
            params[name] = scope.$parent.$parent[name]
            return;
        }
        if (params[name] === '')
            params[name] = def;
    };

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
            return 'clean';
        },

        ngValidateBefore: function (default_function) {
            // return something != undefined if you need load model
            return $scope['data'];
        },


        ngValidateAfter: function (resp, default_function) {
            if ($scope.state !== 'validating') return false;
            $scope['validation'] = cloneObject(resp);
            return (!resp || !$.isEmptyObject(resp['errors'])) ? 'invalid' : 'valid';
        },

        ngSaveBefore: function (default_function) {
            return $scope['data'];
        },


        ngSaveAfter: function (resp, default_function) {
            $scope['original_data'] = cloneObject(resp);
            return resp ? 'clean' : 'saving_failed';
        }

    };


    angular.module('ajaxFormModule', []).factory('$ajaxForm', ['$http', function ($http) {


        var ret = {};
        ret.save = function () {
        };
        ret.load = function () {
        };
        ret.validate = function () {
        };
        return ret;

    }]).directive('ngAf', ['$ajaxForm', '$http', function ($ajaxForm, $http) {

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
            scope: {
                ngAf: '&',
                ngAfLoadUrl: '&',
                ngAfValidateUrl: '&',
                ngAfSaveUrl: '&'
            },
            require: ['ngModel'],
            link: function (scope, el, attrsibutes, ngModelCtrl,aaa) {

                console.log(scope, el, attrsibutes, ngModelCtrl,aaa);


                var $scope = scope;
                var $data_var = 'data';

                var params = {};

                // variables! remove this!!! hardcode in default callbacks and pass default callbacks to REAL callbacks


        //        ng-af=""
        //
        //ng-af-load-url=""
        //ng-af-save-url=""
        //ng-af-validate-url=""
        //
        //ng-af-before-load=""
        //ng-af-after-load=""
        //
        //ng-af-before-save=""
        //ng-af-after-save=""
        //
        //ng-af-before-validation=""
        //ng-af-after-validation=""
        //
        //ng-af-load-result="data_original"
        //ng-af-validation-result="data_validation"
        //ng-af-save-result="data_save"
        //
        //ng-af-watch=""
        //ng-af-debounce=""

                cloneIfExists(params, {ngAf: window.location.href}, scope);

                cloneIfExists(params, {
                    ngAfLoadUrl: AppendParameter(params['ngAf'], 'action=load'),
                    ngAfValidateUrl: AppendParameter(params['ngAf'], 'action=validate'),
                    ngAfSaveUrl: AppendParameter(params['ngAf'], 'action=save')
                }, scope);

                // validation watch params
                cloneIfExists(params, {
                    ngValidateWatch: '',
                    ngValidateDebounce: '500'
                }, attrs);

                SetIfEmpty(params, 'ngValidateWatch', params['ngData']);
                params['ngValidateDebounce'] = parseInt(params['ngValidateDebounce']);


                cloneIfExists(params, defaultCallbacks, attrs);

                function callCallback() {
                    var args = Array.prototype.slice.call(arguments);
                    var callbackkey = args.shift();
                    args.push(defaultCallbacks[callbackkey]);
                    return params[callbackkey].apply($scope, args);
                }


                var func1 = function (action, statebefore, stateonsuccess, stateonfail) {
                    var old_state = $scope['state'];

                    var dataToSend = callCallback('ng' + action + 'Before');
                    var url = callCallback('ng' + action + 'Url');
                    if (!dataToSend || !url) {
                        return false;
                    }

                    $scope['state'] = statebefore;
                    $ok(url, dataToSend,
                        function (resp, errorcode, httpresp) {
                            var ret = callCallback('ng' + action + 'After', resp);
                            if (ret) {
                                $scope['state'] = ret;
                            }
                            else {
                                $scope['state'] = stateonfail ? stateonfail : old_state;
                            }
                        },
                        function (resp, errorcode, httpresp) {
                            $scope['state'] = stateonfail ? stateonfail : old_state;
                        });

                    return true;
                }


                $scope['state'] = 'init';

                $scope.load = function () {
                    if ($scope.isActionAllowed('load')) func1('Load', 'loading', 'clean', 'loading_failed')
                };

                $scope.validate = function () {
                    if ($scope.isActionAllowed('validate')) func1('Validate', 'validating', 'valid', 'invalid')
                };

                $scope.save = function () {
                    if ($scope.isActionAllowed('save')) func1('Save', 'saving', 'clean', 'saving_failed')
                };

                var save_states = ['init', 'clean', 'saving_failed', 'valid', 'loading_failed'];
                var validate_or_load_states = save_states.slice(0);
                validate_or_load_states.push('invalid', 'dirty')
                $scope.isActionAllowed = function (action) {
                    if (action === 'load') {
                        return validate_or_load_states.indexOf($scope.state) !== -1
                    }
                    if (action === 'validate') {
                        return validate_or_load_states.indexOf($scope.state) !== -1
                    }
                    if (action === 'save') {
                        return save_states.indexOf($scope.state) !== -1
                    }
                }

                $scope.load();

                var debouncedvalidate = _.debounce(function () {
                    $scope.validate();
                }, 500);

                $scope.$watch('data', function () {
                    $scope['state'] = 'dirty';
                    debouncedvalidate();
                }, true);


            }
        };


    }]);


})(this.angular);
